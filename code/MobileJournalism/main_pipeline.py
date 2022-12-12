from __future__ import division
import matplotlib.pyplot as plt
import os
import re
import sys
import time
from google.cloud import speech
import pyaudio
from six.moves import queue
import heapq
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import spacy
import re
import unidecode
import yake
from difflib import SequenceMatcher
from tools_init import return_elements
import warnings

warnings.filterwarnings("ignore")

nlp = spacy.load("el_core_news_lg")

# Audio recording params
STREAMING_LIMIT = 240000  # 4 mins
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'

wordcloud, stoplist, custom_kw_extr = return_elements()
# sentence_model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
# my_loaded_topic_model = BERTopic.load("C:\\Python\\myNewsScraper\\omilies_model", embedding_model=sentence_model)

omilies_model = BERTopic.load("C:\\Python\\torchidis\\omilies_model2", embedding_model="lighteternal/stsb-xlm-r-greek-transfer")
arthra_model = BERTopic.load("C:\\Python\\torchidis\\arthra_model", embedding_model="lighteternal/stsb-xlm-r-greek-transfer")

with open('C:\\Users\\Panagiotis\\Desktop\\omilies_labels.txt', encoding='utf8') as f:
    lines = f.readlines()

for m in range(len(lines)):
    omilies_model.set_topic_labels({m: str(lines[m])})

cur_speech = []
text_array = []


def get_current_time():
    return int(round(time.time() * 1000))


def most_frequent(lst):
    return max(set(lst), key=lst.count, default='')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def process_topic(tp):
    tp = tp.replace('_', ' ')
    tp = re.sub(r'[0-9]', '', tp)
    words = [word for word in tp.split(' ') if word not in stoplist]
    words = list(dict.fromkeys(words))

    trash_words = []
    for i in range(len(words) - 1):
        similarities = []
        for j in range(i + 1, len(words)):
            sml = similar(unidecode.unidecode(words[i]), unidecode.unidecode(words[j]))
            if sml >= 0.75:
                if len(words[i]) <= len(words[j]):
                    trash_words.append(words[j])
                else:
                    trash_words.append(words[i])

    words = [x for x in words if x not in trash_words or trash_words.remove(x)]
    tp = ' '.join(words)
    return tp


def preprocess_text(txt, method=None):
    # remove stopwords and blanks
    txt = txt.replace("  ", " ")
    txt = txt.replace(",", "")
    txt = txt.replace("«", "")
    txt = txt.replace("»", "")
    txt = txt.replace(":", "")
    txt = [word for word in txt.split(" ") if word not in stoplist]
    txt = " ".join(txt)
    """
    doc = nlp(text)
    clean_txt = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"]]
    text = " ".join(clean_txt)
    """
    return txt


def preprocess_sentence(txt):
    # keep only NOUNS, ADJ, VERBS (POS tagging)
    doc = nlp(txt)
    clean_txt = [token.text for token in doc if token.pos_ in ["NOUN"]]
    sent = " ".join(clean_txt)
    return sent


def find_ner(txt):
    txt = preprocess_text(txt)
    doc = nlp(txt)
    final = []
    for elem in doc.ents:
        ste = str(elem)
        if ste not in final:
            final.append(ste)
    similarities = []
    final_ents = []
    for n in range(len(final)):
        similarities.append([])
        for k in range(n + 1, len(final), 1):
            simil = similar(str(final[n]), str(final[k]))
            similarities[n].append(simil)
            if simil >= 0.80:
                if len(final[n]) < len(final[k]):
                    final_ents.append(final[k])
                else:
                    final_ents.append(final[n])
    else:
        for elem in similarities:
            # print(elem)
            pass
    for elem in final_ents:
        if elem in final:
            final.pop(final.index(elem))
    return final


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""

        while not self.closed:
            data = []

            if self.new_stream and self.last_audio_input:

                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)

                if chunk_time != 0:

                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round(
                        (self.final_request_end_time - self.bridging_offset)
                        / chunk_time
                    )

                    self.bridging_offset = round(
                        (len(self.last_audio_input) - chunks_from_ms) * chunk_time
                    )

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses, stream):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    for response in responses:

        if get_current_time() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = get_current_time()
            break

        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        result_seconds = 0
        result_micros = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_micros = result.result_end_time.microseconds

        stream.result_end_time = int((result_seconds * 1000) + (result_micros / 1000))

        corrected_time = (
                stream.result_end_time
                - stream.bridging_offset
                + (STREAMING_LIMIT * stream.restart_counter)
        )
        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.

        if result.is_final:

            sys.stdout.write(GREEN)
            '''
            sys.stdout.write("\033[K")
            sys.stdout.write(str(corrected_time) + ": " + transcript + "\n")
            '''
            text = transcript
            # ----------------------------------------------------------------------------------------------------
            # text = transcript
            print(text)

            par_topics = []
            ents = find_ner(text)
            # Extract keywords
            keywords2 = custom_kw_extr.extract_keywords(preprocess_sentence(text))
            keywords2 = [i[0] for i in keywords2]
            keywords2.extend(ents)

            topics, probs = omilies_model.transform(str(text).lower())

            if topics == [-1]:
                pass
            else:
                anathesi = omilies_model.get_topic_info(topics[0])['CustomName'][0]
                anathesi = anathesi.replace('\n', '')
                anathesi = anathesi.split("_")
                thema = anathesi[0]
                katigoria = anathesi[1]
                print(thema)

                kws = " ".join(keywords2)
                try:
                    wordcloud.generate(kws)
                    plt.figure(figsize=(10, 5), dpi=80, edgecolor='b')
                    # plt.title(f"{label}\n", fontdict={'fontsize': 30, 'fontweight': 15})
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis("off")
                    plt.savefig("C:\\Users\\Panagiotis\\Desktop\\results\\photos\\" + str(corrected_time) + ".png")

                    seconds = float(corrected_time/1000)
                    (hours, seconds) = divmod(seconds, 3600)
                    (minutes, seconds) = divmod(seconds, 60)

                    timestamp = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"

                    html_code = f'<div class="container"> <div class="content"> <h3>Κατηγορία: {katigoria} , {timestamp}</h2> ' \
                                f'<h4>Θέμα: {thema}</h4> <img src="photos/{str(corrected_time)}.png" alt="forest" height="200px" ' \
                                'width="300px"/> </div> </div> '

                    with open('C:\\Users\\Panagiotis\\Desktop\\results\\results.html', 'r', encoding='utf8') as fh:
                        contents = fh.readlines()

                    contents = " ".join(contents)
                    index_ofdiv = str(contents).rfind('</div>')
                    new_html = str(contents)[:index_ofdiv] + html_code + str(contents)[index_ofdiv:]
                    new_html = new_html.replace('\t', '')
                    new_html = new_html.replace('\n', '')
                    new_html = new_html.replace('\\', '')

                    with open('C:\\Users\\Panagiotis\\Desktop\\results\\results.html', 'w', encoding='utf8') as fh:
                        fh.write(new_html)

                    plt.savefig("C:\\Python\\myNewsScraper\\speech_photos\\" + str(corrected_time) + ".png")
                except ValueError:
                    print("No keywords for this batch of speech!")
            print("--------------------------------------")
            # ----------------------------------------------------------------------------------------------------

            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                sys.stdout.write(YELLOW)
                sys.stdout.write("Exiting...\n")
                stream.closed = True
                break

        else:
            sys.stdout.write(RED)
            sys.stdout.write("\033[K")
            sys.stdout.write(str(corrected_time) + ": " + transcript + "\r")

            stream.last_transcript_was_final = False


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "el-GR"  # a BCP-47 language tag

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'my-stt-demo-4f6486132c42.json'
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        enable_automatic_punctuation=True,
        enable_spoken_punctuation=True,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    mic_manager = MicrophoneStream(RATE, CHUNK)
    print(mic_manager.chunk_size)
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
    sys.stdout.write("End (ms)       Transcript Results/Status\n")
    sys.stdout.write("=====================================================\n")

    with mic_manager as stream:

        while not stream.closed:
            sys.stdout.write(YELLOW)
            sys.stdout.write(
                "\n" + str(STREAMING_LIMIT * stream.restart_counter) + ": NEW REQUEST\n"
            )

            stream.audio_input = []
            audio_generator = stream.generator()

            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            listen_print_loop(responses, stream)

            if stream.result_end_time > 0:
                stream.final_request_end_time = stream.is_final_end_time
            stream.result_end_time = 0
            stream.last_audio_input = []
            stream.last_audio_input = stream.audio_input
            stream.audio_input = []
            stream.restart_counter = stream.restart_counter + 1

            if not stream.last_transcript_was_final:
                pass
                sys.stdout.write("\n")
            stream.new_stream = True


if __name__ == "__main__":
    main()
