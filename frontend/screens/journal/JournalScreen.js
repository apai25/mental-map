import React from 'react'
import { View, Text, Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StyleSheet } from 'react-native';
import MoodView from './MoodView';

const JournalScreen = (props) => {

  const { navigation } = props;

  const sentiments = [
    {sentiment: "anger", percent: 55},
    {sentiment: "anxiety", percent: 20},
    {sentiment: "disappointment", percent: 15},
  ]

  const goToChat = () => {
    navigation.navigate('Chat')
  }

  return (
    <View style={styles.centered}>
        <MoodView title="Week Recap" sentiments={sentiments}/>
    </View>
  )
}

const styles = StyleSheet.create({
  centered: { 
    alignItems: "center", 
    backgroundColor: '#F1EFE7'
  }
})

export default JournalScreen