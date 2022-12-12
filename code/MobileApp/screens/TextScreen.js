import React, {useState, useEffect} from 'react';
import { StyleSheet, Text, View, ScrollView, Image, TouchableOpacity, Alert, FlatList } from 'react-native';
import { VictoryLabel, VictoryPie } from 'victory-native';

export default function TextScreen(props, {navigation}){

    const text = props.route.params.text

    const url = text.img_url

    const onPressDelete = () => { return Alert.alert("Είσαι σίγουρος;", "Είσαι σίγουρος ότι θες να διαγράψεις αυτό το αρχείο από την βάση δεδομένων;",
        [ // The "Yes" button
            {
            text: "Ναι",
            onPress: () => {
                fetch('http://192.168.2.2:8000/api/texts/'+ String(text.id)+'/', { //http://192.168.2.6:8000/api/texts/
                method: 'DELETE',
                headers: {
                    'Authorization': 'Token 10c217e6ef64023282cf08b3a6ef59d3dd89976b',
                },
            })
            .then(() => Alert.alert('Το αρχείο διαγράφηκε επιτυχώς'))
            .then(() => props.navigation.navigate('MenuScreen')
            )
            .catch(error => Alert.alert("error", error.message))
                },
            },
            // The "No" button // Does nothing but dismiss the dialog when tapped
            {
            text: "Όχι",
            },
        ]
        );
    };

    const arrayEnts = text.ents.split(',')


    for (let i = 0; i < arrayEnts.length; i++){
        arrayEnts[i] = arrayEnts[i].replace('[', '');
        arrayEnts[i] = arrayEnts[i].replace(']', '');
        arrayEnts[i] = arrayEnts[i].replace('\'', '');
        //        arrayEnts[i] = arrayEnts[i].replace(' ', '');
        if (i != arrayEnts.length-1){
            arrayEnts[i] = arrayEnts[i].replace('\'', '');
        }
        else {
            arrayEnts[i] = arrayEnts[i].replace('\'', '');
        }
    }

    return (
        <ScrollView style={{ backgroundColor: '#fff' }}>
            <Text style={{ fontSize: 20, marginLeft: 10, marginTop: 5 }}>{text.source} > {text.topic} </Text>
            <View style={{flexDirection: "row", paddingLeft: 330, backgroundColor: '#fff'}}>
                <TouchableOpacity>
                    <Image style={{ width: 25, height: 25, marginRight: 10, marginTop: -24 }} source={require("../assets/edit_png.png")} resizeMode='contain' />
            </TouchableOpacity>
                <TouchableOpacity onPress={() => onPressDelete()}>
                    <Image style={{ width: 25, height: 25, marginTop: -24, marginRight: 10 }} source={require("../assets/delete_png.png")} resizeMode='contain' />
            </TouchableOpacity>
        </View> 
                
                <Text style={{ fontSize: 30, margin: 10 }} >{text.title}. </Text>
                <Image source={{ uri: url }} style={{ width: '100%', height: 300, marginTop: 10 }}></Image>
                <Text style={{ fontSize: 18, marginTop: 10, marginLeft: 10, marginRight:10 }}>{text.text}</Text>

            <ScrollView horizontal showsVerticalScrollIndicator={false} showsHorizontalScrollIndicator={true} contentContainerStyle={{ paddingVertical: 10 }}>
                <FlatList style={styles.controlSpace}
                    scrollEnabled={false} contentContainerStyle={{ alignSelf: 'flex-start', }} numColumns={Math.ceil(arrayEnts.length / 3)} showsVerticalScrollIndicator={false}
                    showsHorizontalScrollIndicator={false} data={arrayEnts} renderItem={({ item }) => <Text style={styles.item}>#{item}</Text>}
                />
            </ScrollView>

        </ScrollView>
    )
}

const styles = StyleSheet.create({
    text:{
        fontSize:16, 
        padding:10,
        backgroundColor: "#fff",
        width:"100%",
        borderWidth: 0,
        borderBottomRightRadius:0,
        borderBottomLeftRadius:0,
        marginHorizontal:8,
        marginBottom:5,
    },
    head:{
        fontSize: 16,
        marginTop:10,
        padding:10,
        color:"#000",
        fontWeight: "bold",
        backgroundColor: "#fff",
        borderTopWidth:1,
        borderBottomWidth:3,
        width:"110%",
        borderWidth: 0,
    },
    tinyImage: {
      width: 20,
      height: 20,
    },
    item: {
        backgroundColor: "#87ceeb",
        borderRadius: 0,
        fontWeight: "bold",
        margin: 2,
        padding:10,
        textAlign: "center",
        borderRadius:10,
        fontSize: 14,
    },
      controlSpace: {
        width: "100%",
        flexDirection:"row",
        flexWrap:"wrap",
        marginTop:10,
        marginBottom:20,
        padding:5,
        backgroundColor: '#fff',
      },
      arrow_tiny: {
          width:25, 
          height:20, 
          marginLeft: -100, 
          marginTop:8, 
          backgroundColor:"#fff"
    },
})