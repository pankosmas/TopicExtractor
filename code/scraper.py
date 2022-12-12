# This is a sample Python script.
import requests
from datetime import datetime
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError, MaxRetryError

sites = {
    "cnn": ["politiki", "oikonomia", "ellada", "kosmos", "sports", "tech", "perivallon", "style/politismos"],
    "iefimerida": ["oikonomia", "politiki", "ellada", "kosmos", "politismos", "ygeia", "spor", "tehnologia"],
    "newsit": ["ellada", "kosmos", "politikh", "oikonomia", "athlitika", "texnologia", "ygeia", "kairos"],
    "enikos": ["politics", "economy", "international", "society", "sports", "ygeia"],
    "gazzetta": ["football", "basketball", "other-sports"],
    "newsbomb": ["ellada", "kosmos", "politikh", "ygeia", "oikonomia", "sports", "kairos", "bombplus/texnologia",
                 "bombplus/politismos"],
    "pronews": ["category/elliniki-politiki/", "category/athlitismos/", "category/ygeia/", "category/thriskeia/",
                "category/perivallon/", "category/politismos/", "category/oikonomia/", "category/kosmos/",
                "category/koinonia/", "category/epistimes/"]
}


days = ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]

months1 = ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαϊος", "Ιουνίου", "Ιουλίου", "Αυγούστου",
           "Σεπτεμβρίου",
           "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"]

months2 = ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου", "Ιουλίου", "Αυγούστου",
           "Σεπτεμβρίου",
           "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"]


def get_html_doc(uri):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    try:
        response = requests.get(uri, headers=headers, timeout=6)
    except requests.exceptions.Timeout:
        print("Timeout occurred!")
        response = requests.get(uri, headers=headers, timeout=120)
    return response.text


def find_cnn_elements(s):
    try:
        ftitle = s.find(class_="main-title").get_text()
        ftitle = ftitle.replace("  ", "")
        ftitle = ftitle.replace("\n", " ")
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find('time').get_text()
        fdate = fdate.replace("  ", "")
        fdate = fdate.replace("\n", " ")
        fdate = fdate.replace("\t", "")
        fdate = fdate.replace(",", "")
        for day in days:
            if day in fdate:
                fdate = fdate.replace(day, "")
        for month in months1:
            if month in fdate:
                fdate = fdate.replace(" " + month + " ", "/" + str("{:02d}".format(months1.index(month) + 1)) + "/")
        for month in months2:
            if month in fdate:
                fdate = fdate.replace(" " + month + " ", "/" + str("{:02d}".format(months2.index(month) + 1)) + "/")
        fdate = fdate.replace("  ", "")
        fdate = fdate + ":00"
        print(fdate)
        datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find("picture", class_="main-image").find("img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="main-text story-fulltext").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_iefimerida_elements(s):
    try:
        ftitle = s.find(class_="f-big w-bold").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find('time').get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace("&nbsp;", "")
        fdate = fdate.replace("\xa0", "")
        fdate = fdate.replace("  ", " ") + ":00"
        if "UPD" in str(fdate):
            fdate = fdate[22:]
        print(fdate)
        datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find(class_="aspect-ratio two-one").find("img").get("src")
        fimage_url = "https://www.iefimerida.gr" + fimage_url
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="field--name-body").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_newsit_elements(s):
    try:
        ftitle = s.find(class_="entry-title").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find('time').get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace("  ", "")
        fdate = fdate[6:16] + " " + fdate[0:5]
        fdate = fdate + ":00"
        print(fdate)
        datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find(class_="page-header-image-single grid-container grid-parent generate-page-header").find(
            "img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="entry-content post-with-no-excerpt").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_enikos_elements(s):
    try:
        ftitle = s.find("h1").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find(class_="post-date").get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace(",", "")
        for day in days:
            if day in fdate:
                fdate = fdate.replace(day, "")
        for month in months1:
            if month in fdate:
                fdate = fdate.replace(" " + month + " ", "/" + str("{:02d}".format(months1.index(month) + 1)) + "/")
        for month in months2:
            if month in fdate:
                fdate = fdate.replace(" " + month + " ", "/" + str("{:02d}".format(months2.index(month) + 1)) + "/")
        print(fdate)
        fdate = fdate.replace("  ", "")
        fdate = fdate.replace(" ", "")
        fdate = fdate[5:] + " " + fdate[0:5] + ":00"
        try:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            fdate = fdate.replace(" ", "")
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find(class_="featured-img").find("img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="articletext").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_newsbomb_elements(s):
    try:
        ftitle = s.find("h1").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find('time').get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace(",", "")
        fdate = fdate.replace("\t", "")
        fdate = fdate[:10] + " " + fdate[10:]
        fdate = fdate + ":00"
        print(fdate)
        try:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            fdate = fdate.replace(" ", "")
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find(class_="main-image").find("img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ""
        for p in s.find(class_="main-text story-fulltext").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_raptack_elements(s):
    try:
        ftitle = s.find("h1").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find(class_='story-date').get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace("\t", "")
        fdate = fdate.replace(" ", "")
        fdate = fdate + " 00:00:00"
        print(fdate)
        try:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            fdate = fdate.replace(" ", "")
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find(class_="story-image-block").find("img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="story-fulltext").find_all('p'):
            ftext = p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_pronews_elements(s):
    try:
        ftitle = s.find("h1").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find(class_="postdate").get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace("\t", "")
        fdate = fdate.replace(" ", "")
        fdate = fdate.replace("|", " ")
        fdate = fdate.replace(".", "/")
        fdate = fdate + ":00"
        print(fdate)
        try:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = s.find(class_="article__cover").find("img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="wrap-content body").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def find_gazzetta_elements(s):
    try:
        ftitle = s.find(class_="headline").get_text()
    except AttributeError:
        ftitle = None

    try:
        fdate = s.find('time').get_text()
        fdate = fdate.replace("\r", "")
        fdate = fdate.replace("\n", "")
        fdate = fdate.replace("\t", "")
        fdate = fdate.replace(" ", "")
        fdate = fdate.replace("-", " ")
        fdate = fdate.replace(".", "/")
        for day in days:
            if day in fdate:
                fdate = fdate.replace(day, "")
        for month in months1:
            if month in fdate:
                fdate = fdate.replace(month, "/" + str("{:02d}".format(months1.index(month) + 1)) + "/")
        for month in months2:
            if month in fdate:
                fdate = fdate.replace(month, "/" + str("{:02d}".format(months2.index(month) + 1)) + "/")
        fdate = fdate + ":00"
        print(fdate)
        try:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            datef = datetime.strptime(fdate, '%d/%m/%Y %H:%M:%S')
        fts = datetime.timestamp(datef)
    except AttributeError:
        fdate = None
        fts = None

    try:
        fimage_url = "https://www.gazzetta.gr/" + s.find('picture').find("img").get("src")
    except AttributeError:
        fimage_url = None

    try:
        ftext = ''
        for p in s.find(class_="group-left column is-8 is-relative").find_all('p'):
            ftext += p.get_text() + '\n'
    except AttributeError:
        ftext = None

    return ftitle, fdate, fimage_url, ftext, fts


def main():
    data = {'title': [], 'text': [], 'img': [], 'date': [], 'timestamp': [], 'category': [], 'src': []}
    df_data = pd.DataFrame(data)
    for site, categories in sites.items():
        raptack = False
        raptacks = []
        for category in categories:
            data2 = {'title': [], 'text': [], 'img': [], 'date': [], 'timestamp': [], 'category': [], 'src': []}
            df_data2 = pd.DataFrame(data2)

            print(category)
            url = "https://www." + site + ".gr/" + category

            # find all the anchor tags with "href"
            # attribute starting with "https://"
            counter1 = 0
            articles = []

            for page in range(1):  # ---------- BRES LINKS ARTHRWN GIA TIS 25 PRWTES SELIDES THS KATHGORIAS --------------
                if page == 0:
                    pass
                else:
                    if site == "cnn":
                        url = "https://www." + site + ".gr/" + category + "?page=" + str(page + 1)
                    elif site == "kathimerini":
                        url = url
                    elif site == "iefimerida":
                        url = "https://www." + site + ".gr/" + category + "?page=" + str(page + 1)
                    elif site == "newsbomb":
                        url = "https://www." + site + ".gr/" + category + "?page=" + str(page + 1)
                    elif site == "news247":
                        url = "https://www." + site + ".gr/" + category + "/?pages=" + str(page + 1)
                    elif site == "newsit":
                        url = "https://www." + site + ".gr/" + category + "/page/" + str(page + 1)
                    elif site == "enikos":
                        url = "https://www." + site + ".gr/" + category + "/page/" + str(page + 1)
                    elif site == "pronews":
                        url = "https://www." + site + ".gr/" + category + "/page/" + str(page + 1)
                    elif site == "gazzetta":
                        url = "https://www." + site + ".gr/" + category + "?page=" + str(page + 1)

                html_doc = get_html_doc(url)
                soup = BeautifulSoup(html_doc, 'html.parser')
                # print(soup)

                if site == "cnn":  # ----------------------------------  CNN  --------------------------------------------
                    for link in soup.find_all('a', attrs="item-link"):
                        # print(link.get("href"))
                        article_url = "https://www." + site + ".gr/" + link.get("href")
                        articles.append(article_url)
                elif site == "kathimerini":  # ---------------------------- KATHIMERINI ------------------------------------
                    for link in soup.find_all('a', attrs="item-link"):
                        # print(link.get("href"))
                        article_url = "https://www." + site + ".gr/" + link.get("href")
                        articles.append(article_url)
                elif site == "iefimerida":  # ------------------------------- IEFIMERIDA ----------------------------------
                    for link in soup.find_all("article"):
                        article_url = link.find('a').get("href")
                        articles.append("https://www." + site + ".gr" + article_url)
                elif site == "news247":  # -------------------------------- NEWS247 ----------------------------------------
                    for link in soup.find_all('a', attrs="item-link"):
                        # print(link.get("href"))
                        article_url = "https://www." + site + ".gr" + link.get("href")
                        articles.append(article_url)
                elif site == "newsit":  # ------------------------------- NEWSIT ---------------------------------------
                    for link in soup.find_all('article'):
                        # print(link.get("href"))
                        article_url = link.find('a').get("href")
                        articles.append(article_url)
                elif site == "enikos":  # ------------------------------- ENIKOS ---------------------------------------
                    for link in soup.find_all(class_='archive-post'):
                        # print(link.get("href"))
                        article_url = link.find('a').get("href")
                        articles.append(article_url)
                elif site == "newsbomb":  # ------------------------------- ENIKOS ---------------------------------------
                    for link in soup.find_all('figure'):
                        # print(link.get("href"))
                        extra = link.find('a').get("href")
                        article_url = "https://www." + site + ".gr" + extra
                        if (article_url.count("www") > 1) and ("ratpack" in extra):
                            article_url = extra
                            raptack = True
                        raptacks.append(raptack)
                        articles.append(article_url)
                        raptack = False
                elif site == "pronews":  # ------------------------------- PRONEWS ---------------------------------------
                    for link in soup.find_all(
                            class_="column is-half-desktop is-half-tablet is-half-mobile is-full-small"):
                        # print(link.get("href"))
                        article_url = link.find('a').get("href")
                        articles.append(article_url)
                elif site == "gazzetta":  # ------------------------------- GAZZETTA ---------------------------------------
                    for link in soup.find_all(class_="list-article__info"):
                        # print(link.get("href"))
                        article_url = "https://www." + site + ".gr/" + link.find('h3').find('a').get("href")
                        articles.append(article_url)

            # print(len(articles))

            for i in range(3):  # len(articles)
                # print(i)
                if articles[i].count("www") > 1:
                    continue
                else:
                    html_doc = get_html_doc(articles[i])
                    soup = BeautifulSoup(html_doc, 'html.parser')

                if category == "style/moda" or category == "gynaika":
                    category = "Μόδα"
                elif (category == "politiki") or (category == "politikh") or (category == "politics") or (
                        category == "category/elliniki-politiki/"):
                    category = "Πολιτική"
                elif category == "style/psyxagogia":
                    category = "Ψυχαγωγία"
                elif category == "style/politismos" or category == "politismos" or category == "bombplus/politismos" or category == "category/politismos/":
                    category = "Πολιτισμός"
                elif category == "perivallon" or category == "category/perivallon/":
                    category = "Περιβάλλον"
                elif category == "oikonomia" or category == "economy" or category == "category/oikonomia/":
                    category = "Οικονομία"
                elif category == "ellada" or category == "society" or category == "category/koinonia/" or category == "category/thriskeia/":
                    category = "Κοινωνία"
                elif category == "kosmos" or category == "international" or category == "category/kosmos/":
                    category = "Κόσμος"
                elif category == "sports" or category == "athlitika" or category == "spor" or category == "sports" or category == "category/athlitismos/" or category == "football" or category == "basketball" or category == "other-sports":
                    category = "Αθλητισμός"
                elif category == "tech" or category == "texnologia" or category == "tehnologia" or category == "bombplus/texnologia" or category == "category/epistimes/":
                    category = "Τεχνολογία"
                elif category == "style/aytokinito" or category == "auto" or category == "aytokinito" or category == "bombplus/aytokinhto" or category == "category/auto-moto/":
                    category = "Αυτοκίνητο"
                elif category == "ygeia" or category == "category/ygeia/":
                    category = "Υγεία"
                elif category == "kairos":
                    category = "Καιρός"
                elif category == "zodia" or category == "bombplus/zwdia":
                    category = "Ζώδια"

                if site == "cnn":
                    title, date, image_url, text, ts = find_cnn_elements(soup)
                elif site == "iefimerida":
                    title, date, image_url, text, ts = find_iefimerida_elements(soup)
                elif site == "newsit":
                    title, date, image_url, text, ts = find_newsit_elements(soup)
                elif site == "enikos":
                    title, date, image_url, text, ts = find_enikos_elements(soup)
                elif site == "newsbomb":
                    title, date, image_url, text, ts = find_newsbomb_elements(soup)
                    if raptacks[i]:
                        title, date, image_url, text, ts = find_raptack_elements(soup)
                elif site == "pronews":
                    title, date, image_url, text, ts = find_pronews_elements(soup)
                elif site == "gazzetta":
                    title, date, image_url, text, ts = find_gazzetta_elements(soup)

                df2 = pd.DataFrame({'title': title, 'text': text, 'img': image_url, 'date': date, 'timestamp': ts,
                                    'category': category, 'src': site}, index=[0])
                df_data = pd.concat([df_data, df2], ignore_index=True, axis=0)
                df_data2 = pd.concat([df_data2, df2], ignore_index=True, axis=0)

                # df_data2.to_csv(category + '.csv', encoding="utf-8")
        # df_data.to_csv(site + '.csv', encoding="utf-8")
    df_data = df_data.drop_duplicates()
    df_data = df_data.dropna(subset=['text'])
    return df_data
