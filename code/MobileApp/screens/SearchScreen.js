import React from 'react'
import { StyleSheet, View } from 'react-native'
import { getStatusBarHeight } from 'react-native-status-bar-height'
import Background from '../components/Background'
import Header from '../components/Header'

export default function SearchScreen({ navigation }) {
    return (
        <Background>
            <Header style={styles.header}>Αναζήτηση Καταχώρησης</Header>
        </Background>
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
  })