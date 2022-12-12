import { TextInput } from 'react-native-paper';
import { Text, ScrollView } from 'react-native'
import Button from '../components/Button'
import Background from '../components/Background'
import React from 'react';

export default function UploadAudioScreen({navigation}) {
    const [text, setText] = React.useState("");

    return (
        <ScrollView style={{flex:1}}>
        <Background>
            {/*Create first radio button */}
                <Text style={{marginBottom: 30, marginTop:10}}>Εισαγωγή Κειμένου:</Text>
                <TextInput
                    multiline
                    maxLength={5000}
                    style={{width:350, height:580, marginBottom: 10}}
                    label="Καταχωρήστε το κείμενο σας εδώ..."
                    value={text}
                    onChangeText={text => setText(text)}
                />
                <Text>
                    Χαρακτήρες: {text.length}/5000
                </Text>
                <Button
                        mode="contained"
                        onPress={() => {checked === 'Αρχείο Κειμένου' ? navigation.navigate('UploadTextScreen'): navigation.navigate('UploadAudioScreen')}}
                    >
                        Καταχώρηση
                </Button>
        </Background>
        </ScrollView>

    );
};