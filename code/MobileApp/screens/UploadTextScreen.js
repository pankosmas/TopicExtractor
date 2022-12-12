import { TextInput } from 'react-native-paper';
import { Text, ScrollView, Alert } from 'react-native'
import Button from '../components/Button'
import Background from '../components/Background'
import React, {useState, useEffect} from 'react';

export default function UploadTextScreen({navigation}) {

    const [text, setText] = React.useState("");
    //const [published, setPublished] = useState(null);
    const user = 3
    
    /*useEffect(() => {
        let today = new Date();
        let published = today.getFullYear()+"-"+(today.getMonth()+1)+"-"+today.getDate();
        setPublished(published)
    }, []);*/

    const saveText = () => {
        fetch('http://192.168.2.2:8000/api/texts/', { //http://192.168.2.6:8000/api/texts/
            method: 'POST',
            headers: {
                'Authorization': 'Token 10c217e6ef64023282cf08b3a6ef59d3dd89976b',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({text: text, user: user})
        })
        .then(res => res.json())
        .then(text => {
            navigation.navigate("TextScreenResults", {text: text} )
        })
        .catch(error => Alert.alert("error", error.message))
    }

    return (
        <ScrollView style={{flex:1}}>
        <Background>
            {/*Create first radio button */}
                <Text style={{marginBottom: 30, marginTop:10}}>Εισαγωγή Κειμένου:</Text>
                <TextInput
                    multiline
                    maxLength={10000}
                    style={{width:350, height:580, marginBottom: 10}}
                    label="Καταχωρήστε το κείμενο σας εδώ..."
                    value={text}
                    onChangeText={text => setText(text)}
                />
                <Text>
                    Χαρακτήρες: {text.length}/10000
                </Text>
                <Button
                        mode="contained"
                        onPress={() => saveText()}
                    >
                        Επεξεργασία
                </Button>
                <Text style={{marginBottom: 10}}></Text>
        </Background>
        </ScrollView>
    );
};