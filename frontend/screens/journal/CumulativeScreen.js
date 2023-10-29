import React from 'react'
import { View, Text, Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const JournalScreen = (props) => {

  const { navigation } = props;

  const goToChat = () => {
    navigation.navigate('Chat')
  }

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>Home Screen</Text>
        <Button
          title="Chat"
          onPress={goToChat} //change "function" with your function for the button pressing
        />
    </View>
  )
}

export default JournalScreen