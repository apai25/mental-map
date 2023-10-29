import React from 'react'
import { View, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StyleSheet } from 'react-native';
import axios from "axios"
import MoodView from './MoodView';
import { Avatar, Button, Card } from 'react-native-paper';

const baseURL = "http://localhost:3000"

const EntryView = ({route, navigation}) => {

    const { sentiments, summary } = route.params;

  return (
    <View style={styles.centered}>
        <MoodView title="Week Recap" sentiments={sentiments}/>
        <Card mode='elevated' style={styles.container}>
            <Card.Content>
                <Text style={styles.title}>Summary</Text>
                <Text style={styles.text}>{summary}</Text>
            </Card.Content>
        </Card>
    </View>
  )
}

const styles = StyleSheet.create({
  centered: { 
    alignItems: "center", 
    backgroundColor: '#F1EFE7'
  },
  container: { 
    width: '90%',
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
        marginTop: '3%',
        fontSize: 14,
        textAlign: 'center',
        lineHeight: 20
    }
})

export default EntryView