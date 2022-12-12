import React, { useState, useEffect, useMemo} from 'react'
import { StyleSheet, FlatList, Alert, Text, View, Image, TouchableOpacity } from 'react-native'
import { Card } from 'react-native-paper';
import { getStatusBarHeight } from 'react-native-status-bar-height'

export default function MyRecordsScreen({ navigation }) {
    
    const [texts, setTexts] = useState([])

    // Keep a status of the current selected status
    const [status, setStatus] = useState('NONE')

    // the filtered list, cached with useMemo
    // the callback is call each time the status or the fullList changes
    const filteredTexts = useMemo(
        () => {
        if (status === 'NONE' ) return texts
        return texts.filter(item => status === item.topic[0])
        },
        [status, texts]
    )

    // the onClick Method is a method that returns a method, which
    // updates the state based on the predefined status
    const onClick = (status) => () => {
        setStatus(status)
    }

    // navigate text on click
    const textClicked = (text) => {
        navigation.navigate("TextScreen", {text: text} )
    }

    // useEffect call GET method from my API for texts
    useEffect(() => {
        fetch('http://192.168.2.2:8000/api/texts/', { //http://192.168.2.6:8000/api/texts/
            method: "GET",
            headers: {
                'Authorization': 'Token 10c217e6ef64023282cf08b3a6ef59d3dd89976b'
            }
        })
        .then(res => res.json())
        .then(jsonRes => setTexts(jsonRes))
        .catch(error => Alert.alert("error", error.message))
    }, []);

    
    // render method on how to view my data
    const renderData = (item) => {
        const arrayTopic = item.topic.split(',')

        for (let i = 0; i < arrayTopic.length; i++){
            arrayTopic[i] = arrayTopic[i].replace('[', '');
            arrayTopic[i] = arrayTopic[i].replace(']', '');
            arrayTopic[i] = arrayTopic[i].replace('\'', '')
            if (i != arrayTopic.length-1){
                arrayTopic[i] = arrayTopic[i].replace('\'', ', ')
            }
            else {
                arrayTopic[i] = arrayTopic[i].replace('\'', '')
            }
        }

        return(
            <TouchableOpacity onPress={() => textClicked(item)}>
            <Card style = {styles.cardStyle}>
                <Text style={{fontSize:16, paddingBottom:5 }}>{item.title.slice(0, 70) +  "..."}</Text>
                <Text style={{fontSize:12, paddingBottom:5}}>{item.published}</Text>
                <Image source={require("../assets/rightarrow.png")} style={{width:30, height:20, position: 'absolute', right: 5, bottom: 5,}}></Image>
                <Text style={{fontSize:14, paddingRight: 25, fontWeight: "bold"}}>Κατηγορία: <Text style={{fontWeight:"normal"}}>{arrayTopic}</Text> </Text> 
            </Card>
            </TouchableOpacity>
        )
    }

    
    // main return method of function
    return (
        <View style={styles.container}>
            <Text style={{marginHorizontal:10}}>Επιλεγμένη Κατηγορία: {status}</Text>
            <View style={styles.filterBar}>
                <TouchableOpacity title="Clear" onPress={onClick('NONE')} style={styles.button}><Text>Clear</Text></TouchableOpacity>
                <TouchableOpacity title="Πολιτικά" onPress={onClick('Πολιτικά')} style={styles.button}><Text>Πολιτικά</Text></TouchableOpacity>
                <TouchableOpacity title="Κοινωνικά" onPress={onClick('Κοινωνικά')} style={styles.button}><Text>Κοινωνικά</Text></TouchableOpacity>
                <TouchableOpacity title="Διεθνή" onPress={onClick('Διεθνή')} style={styles.button}><Text>Διεθνή</Text></TouchableOpacity>
                <TouchableOpacity title="Αθλητικά" onPress={onClick('Αθλητικά')} style={styles.button}><Text>Αθλητικά</Text></TouchableOpacity>
                <TouchableOpacity title="Οικονομία" onPress={onClick('Οικονομία')} style={styles.button}><Text>Οικονομικά</Text></TouchableOpacity>
                <TouchableOpacity title="Πολιτισμός" onPress={onClick('Πολιτισμός')} style={styles.button}><Text>Πολιτισμός</Text></TouchableOpacity>
            </View>
            <FlatList
                data = {filteredTexts}
                renderItem = {({item}) => {
                    return renderData(item)
                }}
                keyExtractor = {item => item.id}
            />
        </View>
    )
}

const styles = StyleSheet.create({
    header: {
        fontSize: 17,
        color: '#560CCE',
        fontWeight: 'bold',
        paddingVertical: 12,
        position: 'absolute',
        top: 10 + getStatusBarHeight(),
        alignContent: 'center',
    },
    cardStyle:{
        padding:10,
        margin:10,
        borderWidth: 2,
        backgroundColor: "#ffffff",
    },
    container: {
        flex: 1,
        justifyContent: 'center',
        padding: 8,
        backgroundColor: 'white',
      },
      list: {
        height: '100%',
        width: '100%'
      },
      filterBar: {
          flexDirection: 'row',
          height: 40,
          margin:10,
      },
      item: {
        flex: 1,
        justifyContent: 'flex-start',
        padding: 8,
        backgroundColor: 'white',
      },
      text: {
        fontSize: 16,
        lineHeight: 21,
        fontWeight: 'bold',
        letterSpacing: 0.25,
        color: 'black',
      },
      button:{
          marginRight: 5,
          padding: 2,
          backgroundColor: "#f5f5f5",
          height: 25,
          borderRadius: 5,
      },
  })