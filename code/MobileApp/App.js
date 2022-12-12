import React, { useState } from 'react';
import { StyleSheet, Text, View, ScrollView, Image, TouchableOpacity, Alert, Button } from 'react-native';
import { Menu, Divider, Provider } from 'react-native-paper';
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { theme } from './core/theme'
import {
  HomeScreen,
  LoginScreen,
  RegisterScreen,
  ResetPasswordScreen,
  Dashboard,
  MenuScreen,
  UploadScreen,
  UploadTextScreen,
  UploadAudioScreen,
  MyRecordsScreen,
  SearchScreen,
  TextScreen,
  TextScreenResults,
} from './screens'

const Stack = createNativeStackNavigator();

export default function App() {

  const [visible, setVisible] = React.useState(false);

  const openMenu = () => setVisible(true);

  const closeMenu = () => setVisible(false);

  return (
    <Provider theme={theme}>
          <NavigationContainer>
              <Stack.Navigator initialRouteName="HomeScreen" screenOptions={{ headerShown: true, headerTitleAlign: 'center', headerStyle: { backgroundColor: "#fff",  }, }}>
          <Stack.Screen name="HomeScreen" component={HomeScreen} options={{ title: 'Αρχική Σελίδα'}} />
          <Stack.Screen name="LoginScreen" component={LoginScreen} options={{ title: 'LoginScreen' }}/>
          <Stack.Screen name="RegisterScreen" component={RegisterScreen} options={{ title: 'RegisterScreen' }}/>
          <Stack.Screen name="Dashboard" component={Dashboard} options={{ title: 'Dashboard' }}/>
          <Stack.Screen name="ResetPasswordScreen" component={ResetPasswordScreen} options={{ title: 'ResetPasswordScreen' }}/>
                  <Stack.Screen name="MenuScreen" component={MenuScreen} options={{
                      title: 'ΕΙΔΗΣΕΙΣ ΤΩΡΑ', headerLeft: () => (
                              <View
                                style={{
                                  paddingTop: 0,
                                  flexDirection: 'row',
                                  justifyContent: 'center',
                                }}>
                                <Menu
                                  visible={visible}
                                  onDismiss={closeMenu}
                                  anchor={<TouchableOpacity style={styles.button} onPress={openMenu }>
                                          <Image style={{ width: 20, height: 20 }} source={require("./assets/menu.png")} />
                                  </TouchableOpacity>}>
                                  <Menu.Item onPress={() => { }} title="ΑΡΧΙΚΗ" titleStyle={{ fontWeight: 'bold' }} />
                                  <Divider />
                                  <Menu.Item onPress={() => { }} title="ΠΟΛΙΤΙΚΗ" titleStyle={{ fontWeight:'bold' }} />
                                  <Menu.Item onPress={() => { }} title="ΟΙΚΟΝΟΜΙΑ" titleStyle={{ fontWeight: 'bold' }}/>
                                  <Menu.Item onPress={() => { }} title="ΚΟΙΝΩΝΙΑ" titleStyle={{ fontWeight: 'bold' }}/>
                                  <Menu.Item onPress={() => { }} title="ΔΙΕΘΝΗ" titleStyle={{ fontWeight: 'bold' }}/>
                                  <Menu.Item onPress={() => { }} title="ΑΘΛΗΤΙΚΑ" titleStyle={{ fontWeight: 'bold' }}/>
                                  <Menu.Item onPress={() => { }} title="ΠΟΛΙΤΙΣΜΟΣ" titleStyle={{ fontWeight: 'bold' }}/>
                                  <Menu.Item onPress={() => { }} title="ΥΓΕΙΑ" titleStyle={{ fontWeight: 'bold' }}/>
                                  <Divider />
                                  <Menu.Item onPress={() => { }} title="ΤΕΧΝΟΛΟΓΙΑ" />
                                  <Menu.Item onPress={() => { }} title="ΑΥΤΟΚΙΝΗΤΟ" />
                                  <Menu.Item onPress={() => { }} title="ΠΕΡΙΒΑΛΛΟΝ" />
                                  <Menu.Item onPress={() => { }} title="ΑΣΤΡΟΛΟΓΙΑ" />
                                  <Menu.Item onPress={() => { }} title="ΚΑΙΡΟΣ" />
                                </Menu>
                          </View>
                      ), headerRight: () => (
                          <Image style={{ width: 15, height: 15, marginRight: 85 }} source={require("./assets/red.png")} />
                          )
                  }} />
          <Stack.Screen name='UploadScreen' component={UploadScreen} options={{ title: 'Ανέβασμα Αρχείου' }}/>
          <Stack.Screen name='UploadTextScreen' component={UploadTextScreen} options={{ title: 'Αρχείο Κειμένου' }}/>
          <Stack.Screen name='UploadAudioScreen' component={UploadAudioScreen} options={{ title: 'UploadAudioScreen' }}/>
          <Stack.Screen name='MyRecordsScreen' component={MyRecordsScreen} options={{ title: 'Οι Καταχωρήσεις μου' }}/>
          <Stack.Screen name='SearchScreen' component={SearchScreen} options={{ title: 'Αναζήτηση Καταχώρησης' }}/>
          <Stack.Screen name='TextScreen' component={TextScreen} options={{ title: ''}} />
          <Stack.Screen name='TextScreenResults' component={TextScreenResults} options={{ title: 'Το Άρθρο'}} />
        </Stack.Navigator>
      </NavigationContainer>
    </Provider>
  )
}

const styles = StyleSheet.create({
    button: {
        backgroundColor: '#fff',
        borderRadius: 0,
        padding: 0,
        marginBottom: 0,
        shadowColor: '#fff',
        shadowOffset: { width: 0, height: 0 },
        shadowRadius: 0,
        shadowOpacity: 0.0,
    },
});