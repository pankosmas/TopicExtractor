import React, {useState, useEffect} from 'react';
import { StyleSheet, Text, View, ScrollView, Image, TouchableOpacity, Alert, FlatList} from 'react-native';
import { VictoryLabel, VictoryPie } from 'victory-native';


export default function TextScreen(props, {navigation}){

    const text = props.route.params.text

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

    const onPressSave = () => { return Alert.alert("Καταχώρηση", "Αποθήκευση και Επιστροφή στο Αρχικό Μενού;",
        [ // The "Yes" button
            {
            text: "Ναι",
            onPress: () => props.navigation.navigate('MenuScreen')
            },
            // The "No" button // Does nothing but dismiss the dialog when tapped
            {
            text: "Όχι",
            },
        ]
        );
    };

    /*
    useEffect(() => {
        fetch('http://192.168.2.8:8000/api/texts/', { //http://192.168.2.6:8000/api/texts/
            method: "GET",
            headers: {
                'Authorization': 'Token 10c217e6ef64023282cf08b3a6ef59d3dd89976b'
            }
        })
        .then(res => res.json())
        .then(jsonRes => setDetails(jsonRes))
        .catch(error => Alert.alert("error", error.message))
    }, []);
    */

    const arrayTopic = text.topic.split(',')
    const arrayEnts = text.ents.split(',')
    const arrayPercentages = text.percentages.split(',')
    const arrayColors = text.colors.split(',')

    for (let i = 0; i < arrayTopic.length; i++){
        arrayTopic[i] = arrayTopic[i].replace('[', '');
        arrayColors[i] = arrayColors[i].replace('[', '');
        arrayPercentages[i] = arrayPercentages[i].replace('[', '');
        arrayTopic[i] = arrayTopic[i].replace(']', '');
        arrayColors[i] = arrayColors[i].replace(']', '');
        arrayPercentages[i] = arrayPercentages[i].replace(']', '');
        arrayTopic[i] = arrayTopic[i].replace('\'', '');
        arrayColors[i] = arrayColors[i].replace('\'', '');
        if (i != arrayTopic.length-1){
            arrayTopic[i] = arrayTopic[i].replace('\'', '');
            arrayColors[i] = arrayColors[i].replace('\'', '');
        }
        else {
            arrayTopic[i] = arrayTopic[i].replace('\'', '');
            arrayColors[i] = arrayColors[i].replace('\'', '');
        }
    }

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
   
    return(
        <ScrollView>
            <View style={{flexDirection: "row", paddingLeft: 330, backgroundColor: '#fff', marginTop: 3}}>
            <TouchableOpacity onPress={() => onPressSave()} hitSlop={{ top: 30, bottom: 30, left: 30, right: 30 }}> 
              <Image style={{width:25, height:25, marginRight: 10, marginTop: 3, marginLeft:-20}} source={require("../assets/save_png.jpg")} resizeMode='contain' />
            </TouchableOpacity>
            <TouchableOpacity> 
              <Image style={{width:25, height:25, marginRight: 10, marginTop: 3}} source={require("../assets/edit_png.png")} resizeMode='contain' />
            </TouchableOpacity>
            <TouchableOpacity onPress={() => onPressDelete()}> 
              <Image style={{width:25, height:25, marginTop: 3}} source={require("../assets/delete_png.png")} resizeMode='contain' />
            </TouchableOpacity>
        </View> 
        <ScrollView style={{backgroundColor: 'white'}}>
            <TouchableOpacity>
            <View style={{flexDirection: "row", alignItems:"center"}}>
            <Text style={styles.head} > Τίτλος: </Text>
            <Image style={styles.arrow_tiny} source={require("../assets/down_arr.png")}  />
            </View>
            </TouchableOpacity>
            <Text style={styles.text}> {text.title} </Text>

            <TouchableOpacity>
            <View style={{flexDirection: "row", alignItems:"center"}}>
            <Text style={styles.head}> Κατηγορία: </Text>
            <Image style={styles.arrow_tiny} source={require("../assets/down_arr.png")}  />
            </View>
            </TouchableOpacity>
            <VictoryPie padding={{left: 0, bottom:0, top: -140}} colorScale={"heatmap"} data={arrayPercentages} labels={arrayTopic} radius={80} innerRadius={60} padAngle={({ datum }) => datum.y } style={{ labels: { fontSize: 16, fill: "black"}}} />
            <Text style={{marginTop: -300, marginLeft: 160, marginBottom: 100}}>   Βρέθηκαν {arrayColors.length} {'\n'}       Κύριες {'\n'}  Κατηγορίες! </Text>

            <TouchableOpacity>
            <View style={{flexDirection: "row", alignItems:"center"}}>
            <Text style={styles.head}> Οντότητες: </Text>
            <Image style={styles.arrow_tiny} source={require("../assets/down_arr.png")}  />
            </View>
            </TouchableOpacity>
            <ScrollView horizontal showsVerticalScrollIndicator={false} showsHorizontalScrollIndicator={true} contentContainerStyle={{ paddingVertical: 20 }}>
                <FlatList style={styles.controlSpace}
                    scrollEnabled={false} contentContainerStyle={{alignSelf: 'flex-start',}} numColumns={Math.ceil(arrayEnts.length / 3)} showsVerticalScrollIndicator={false}
                    showsHorizontalScrollIndicator={false} data={arrayEnts} renderItem={({ item }) => <Text style={styles.item}>#{item}</Text>}
                />
            </ScrollView>

            <TouchableOpacity>
            <View style={{flexDirection: "row", alignItems:"center"}}>
            <Text style={styles.head}> Κείμενο: </Text>
            <Image style={styles.arrow_tiny} source={require("../assets/down_arr.png")}  />
            </View>
            </TouchableOpacity>
            <Text style={styles.text}> {text.text} </Text>

            <TouchableOpacity>
            <View style={{flexDirection: "row", alignItems:"center"}}>
            <Text style={styles.head}> Περίληψη: </Text>
            <Image style={styles.arrow_tiny} source={require("../assets/down_arr.png")}  />
            </View>
            </TouchableOpacity>
            <Text style={styles.text}> {text.summary} </Text>
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
        padding:5,
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