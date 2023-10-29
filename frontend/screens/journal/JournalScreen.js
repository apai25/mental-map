import React from 'react'
import { View, Text, Button, TouchableHighlight } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StyleSheet } from 'react-native';
import axios from "axios"
import MoodView from './MoodView';
import EntryView from './EntryView';
import DayView from './DayView';
import CalendarView from './CalendarView';

const baseURL = "http://localhost:3000"

const JournalScreen = ({ navigation, route }) => {

  const { userId } = route.params;
  const Stack = createNativeStackNavigator();

  // const sentiments = [
  //   {sentiment: "anger", percent: 55},
  //   {sentiment: "anxiety", percent: 20},
  //   {sentiment: "disappointment", percent: 15},
  // ]

  const [sentiments, setSentiments] = React.useState(null);
  const [summary, setSummary] = React.useState(null);

  const [dailySentiments, setDailySentiments] = React.useState(null);
  const [dailySummary, setDailySummary] = React.useState(null);

  React.useEffect(() => {
    console.log("Console " + userId)
    axios
    .post(`${baseURL}/get-weekly-summary`, {
      user_id: userId,
    })
    .then((response) => {
      if (response.status == 200) {
        console.log(response.data)
        setSummary(response.data.weekly_summary)
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
    <Stack.Navigator>
        <Stack.Screen name="JournalView" component={Journal} initialParams={{ userId: userId, sentiments: sentiments }} options={{ headerShown: false}}/>
        <Stack.Screen name="Weekly Recap" component={EntryView} initialParams={{ sentiments: sentiments, summary: summary }}/>
        <Stack.Screen name="Daily Recap" component={DayView}/>
    </Stack.Navigator>
    
  )
}

const Journal = ({navigation, route}) => {
  const { userId, sentiments } = route.params;

  return (
    <View style={styles.centered}>
          <TouchableHighlight onPress={() => navigation.navigate("Weekly Recap")}  activeOpacity={0} underlayColor="#F1EFE7">
            <MoodView title="Week Recap" sentiments={sentiments}/>
          </TouchableHighlight>
          
          <CalendarView userId={userId} navigateToDate={(date) => navigation.navigate("Daily Recap", { userId: userId, date: date})}/>
    </View>
  )
}

const styles = StyleSheet.create({
  centered: { 
    alignItems: "center", 
    backgroundColor: '#FFF'
  }
})

export default JournalScreen