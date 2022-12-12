import { RadioButton } from 'react-native-paper';
import { Text, View, Pressable } from 'react-native'
import Button from '../components/Button'
import React from 'react';

export default function UploadScreen({navigation}) {
  const [checked, setChecked] = React.useState('Αρχείο Κειμένου'); //initial choice
  return (
    <View style={{alignItems: 'center', justifyContent: 'center', backgroundColor: "#fff", height: "100%"}}>
      {/*Create first radio button */}
        <RadioButton
          value="Αρχείο Κειμένου" 
          status={ checked === 'Αρχείο Κειμένου' ? 'checked' : 'unchecked' } //if the value of checked is Apple, then select this button
          onPress={() => setChecked('Αρχείο Κειμένου')} //when pressed, set the value of the checked Hook to 'Apple'
        />
        <Text>Αρχείο Κειμένου</Text>
        <RadioButton
          value="Αρχείο Ήχου"
          status={ checked === 'Αρχείο Ήχου' ? 'checked' : 'unchecked' }
          onPress={() => setChecked('Αρχείο Ήχου')}
        />
        <Text style={{marginBottom:50}}>Αρχείο Ήχου</Text>
        <Text> Συνέχεια με : {checked}</Text>
        <Button
            style={{width: "50%"}}
            mode="contained"
            onPress={() => {checked === 'Αρχείο Κειμένου' ? navigation.navigate('UploadTextScreen'): navigation.navigate('UploadAudioScreen')}}
        >
            OK
        </Button>
      </View>
  );
};