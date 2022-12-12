import React from 'react';
import Background from '../components/Background';
import Logo from '../components/Logo';
import Header from '../components/Header';
import Button from '../components/Button';
import Paragraph from '../components/Paragraph';

export default function HomeScreen({navigation}) {
  return (
        <Background>
            <Logo/>
            <Header>Σελίδα Σύνδεσης</Header>
            <Paragraph>Καλωσήρθατε στην εφαρμογή Mobile Journalism.</Paragraph>
            <Button
                mode="contained"
                onPress={() => navigation.navigate('LoginScreen')}
            >
                Σύνδεση
            </Button>
            <Button
                mode="outlined"
                onPress={() => navigation.navigate('RegisterScreen')}
            >
                Εγγραφή
            </Button>
        </Background>
  );
}

