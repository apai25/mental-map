import React from 'react'
import { View, Text, Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StyleSheet } from 'react-native';
import axios from "axios"
import MoodView from './MoodView';

const baseURL = "http://localhost:3000"

const JournalScreen = ({ navigation, route }) => {

  const { userId } = route.params;

  // const sentiments = [
  //   {sentiment: "anger", percent: 55},
  //   {sentiment: "anxiety", percent: 20},
  //   {sentiment: "disappointment", percent: 15},
  // ]

  const [sentiments, setSentiments] = React.useState(null);
  const [summary, setSummary] = React.useState(null);


  React.useEffect(() => {
    console.log("Console " + userId)
    axios
    .post(`${baseURL}/get-weekly-summary`, {
      user_id: userId,
    })
    .then((response) => {
      if (response.status == 200) {
        console.log(response.data)
        setSummary(response.data.summary)
        setSentiments(response.data.sentiments)
      }
    })
    .catch((error) => {
      console.log(error)
    });
  }, []);

  const goToChat = () => {
    navigation.navigate('Chat')
  }

  if (!sentiments || !summary) return <View></View>;

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