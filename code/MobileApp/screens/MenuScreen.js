import React, { useState, useEffect, useMemo } from 'react'
import { StyleSheet, FlatList, Alert, Text, View, Image, TouchableOpacity } from 'react-native'
import { Card } from 'react-native-paper';
import { getStatusBarHeight } from 'react-native-status-bar-height'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import Background from '../components/Background'
import Logo from '../components/Logo'
import Header from '../components/Header'
import Paragraph from '../components/Paragraph'
import Button from '../components/Button'


export default function MenuScreen({ navigation }) {

    const [texts, setTexts] = useState([])

    // navigate text on click
    const textClicked = (text) => {
        navigation.navigate("TextScreen", { text: text })
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

        const url = item.img_url

        return (
            <TouchableOpacity onPress={() => textClicked(item)}>
                <Card style={styles.cardStyle}>
                    <Text style={{ fontSize: 20, padding: 0, margin: 0}}></Text>
                    <Image source={{ uri: url }} style={{ width: '100%', height: '65%', position: 'absolute' }}></Image>
                    <Text style={{ fontSize: 20, padding: 0, marginTop: 250 }}>{item.title}</Text>
                    <Text style={{ fontSize: 12, paddingTop: 5, paddingBottom: 5 }}>{item.published}     |     Πηγή: {item.source}</Text>
                    <Image source={require("../assets/rightarrow.png")} style={{ width: 30, height: 20, position: 'absolute', right: 5, bottom: 5 }}></Image>
                    <Text style={{ fontSize: 14, paddingRight: 25, fontWeight: "bold" }}>Κατηγορία: <Text style={{ fontWeight: "normal" }}>{item.topic}</Text> </Text>
                </Card>
            </TouchableOpacity>
        )
    }

    return (
        <View style={styles.container}>
            <FlatList
                data={texts.reverse()}
                renderItem={({ item }) => {
                    return renderData(item)
                }}
                keyExtractor={item => item.id}
            />
            <View style={{ backgroundColor: 'white', position: 'absolute', bottom: 0, left: 0, width: '100%', height: '10%', flexDirection: 'row', alignItems: 'center' }}>
                <TouchableOpacity onPress={() => navigation.navigate('UploadTextScreen')}>
                    <Image source={require("../assets/text.png")} style={{ flex: 2, width: 70, height: '8%', marginLeft: 30 }}></Image>
                </TouchableOpacity>
                <TouchableOpacity>
                    <Image source={require("../assets/rec.png")} style={{ flex: 2, width: 70, height: '8%', marginHorizontal: 60 }}></Image>
                </TouchableOpacity>
                <TouchableOpacity>
                    <Image source={require("../assets/records.png")} style={{ flex: 2, width: 70, height: '8%', marginRight: 60 }}></Image>
                </TouchableOpacity>
            </View>
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
    cardStyle: {
        padding: 10,
        margin: 10,
        borderWidth: 1,
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
        margin: 10,
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
    button: {
        marginRight: 5,
        padding: 2,
        backgroundColor: "#f5f5f5",
        height: 25,
        borderRadius: 5,
    },
})