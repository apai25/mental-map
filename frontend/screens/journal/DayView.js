import React from 'react'
import { View, Text, ScrollView } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StyleSheet } from 'react-native';
import axios from "axios"
import MoodView from './MoodView';
import { Avatar, Button, Card } from 'react-native-paper';
import Emotion from './Emotion';

const baseURL = "http://localhost:3000"

const DayView = ({route, navigation}) => {

    const { userId, date } = route.params;

    const emojis = {
        "anger": "🤬", 
        "anxiety": "😬", 
        "disappointment": "🫠", 
        "excitement": "🥳", 
        "fear": "😰", 
        "joy": "😁", 
        "love": "🥰", 
        "pain": "😖", 
        "sadness": "😔", 
        "tiredness": "🥱"
    }

    // const [dailySentiments, setDailySentiments] = React.useState(null);
    const [dailyEntries, setDailyEntries] = React.useState(null);

  React.useEffect(() => {
    console.log("Console " + userId + date)
    axios
    .post(`${baseURL}/get-entries`, {
      user_id: userId,
      date: date
    })
    .then((response) => {
      if (response.status == 200) {
        console.log(response.data)
        setDailyEntries(response.data)
      }
    })
    .catch((error) => {
      console.log(error)
    });
  }, []);

  if (!dailyEntries) return <View></View>;

  return (
    <View style={styles.centered}>
        <ScrollView>
            {dailyEntries.map((entry) => (
                <Card mode='elevated' /*style={styles.container}*/>
                <Card.Content>
                <View
                    style={[
                        styles.container,
                        {
                        marginLeft: '3%',
                        flexDirection: 'row',
                        width: '100%',
                        alignItems: 'center',
                        justifyContent: 'center'
                        },
                    ]}>

                    <Emotion emoji={emojis[entry.sentiments[0][0].toLowerCase()]} percent={entry.sentiments[0][1]} sentiment={entry.sentiments[0][0]}/>
                    <Emotion emoji={emojis[entry.sentiments[1][0].toLowerCase()]} percent={entry.sentiments[1][1]} sentiment={entry.sentiments[1][0]}/>
                    <Emotion emoji={emojis[entry.sentiments[2][0].toLowerCase()]} percent={entry.sentiments[2][1]} sentiment={entry.sentiments[2][0]}/>

                </View>
                    <Text style={styles.text}>{entry.entry_text}</Text>
                </Card.Content>
            </Card>
            ))}
        </ScrollView>
        
    </View>
  )
}

const styles = StyleSheet.create({
  centered: { 
    alignItems: "center", 
    backgroundColor: '#F1EFE7'
  },
  container: { 
    width: '98%',
    justifyContent: "center", 
    alignItems: "center", 
    marginTop: '3%',
    borderRadius: 15,
},
  title: {
    textAlign: 'center',
    fontFamily: 'HelveticaNeue-Bold',
    fontSize: 20
    },
    text: {
        marginTop: '5%',
        fontSize: 14,
        textAlign: 'center',
        lineHeight: 20
    }
})

export default DayView