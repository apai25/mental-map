import { Chat } from "@flyerhq/react-native-chat-ui"
import React, { useState } from "react"
import { FAB } from 'react-native-paper';
import { SafeAreaProvider } from "react-native-safe-area-context"
import axios from "axios"
import { View, StyleSheet, Alert } from "react-native";
import uuid from 'react-native-uuid';

const baseURL="http://localhost:3000"

// // For the testing purposes, you should probably use https://github.com/uuidjs/uuid
// const uuidv4 = () => {
//   return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => {
//     const r = Math.floor(Math.random() * 16)
//     const v = c === "x" ? r : (r % 4) + 8
//     return v.toString(16)
//   })
// }

const ChatScreen = ({navigation, route}) => {
  const { userId } = route.params;

  const user = { id: "user" }
  const computer = { id: "chatbot" }

  const generateRandomComputerMessage = () => {
    const questions = [
      "How has your day been so far?",
      "Did you have a productive day today?",
      "What was the highlight of your day?",
      "Have you faced any challenges today?",
      "Tell me, how are you feeling today?",
      "Did you accomplish any of your goals today?",
      "Is there something interesting that happened in your day?",
      "How's the weather today in your area?",
      "What's the best thing that happened to you today?",
      "Did you learn something new today?",
    ];
    const randomIndex = Math.floor(Math.random() * questions.length)
    const question = questions[randomIndex]

    const startMessage = {
      author: computer,
      createdAt: Date.now(),
      id: uuid.v4(),
      text: question,
      type: "text"
    }

    return startMessage
  }

  const [messages, setMessages] = useState([generateRandomComputerMessage()])
  const [context, setContext] = useState([]);
  const [threadId, setThreadId] = useState(uuid.v4())
  
  

  const saved = () =>
    Alert.alert('Saved!', 'Logged into your journal.', [
      {
        text: 'Ok',
        style: 'cancel',
      },
  ]);

  const handleSavePress = () => {
    axios
    .post(`${baseURL}/store-entry`,
        {
            user_id: userId,
            context: context,
            entry_id: threadId
        }
    )
    .then((response) => {
        console.log(response)
        saved()
    })
    .catch((error) => {console.log(error)})
  }
  
  const handleSendPress = message => {
    const textMessage = {
      author: user,
      createdAt: Date.now(),
      id: uuid.v4(),
      text: message.text,
      type: "text"
    }
    
    const newContext = [...context, {"user": "user", "text": textMessage.text}]
    const newMessages = [textMessage, ...messages]
    setMessages(newMessages)
    setContext(newContext)
    
    updateChatbotResponse(newContext, newMessages);
  }

  const updateChatbotResponse = (currContext, currMessages) => {
    console.log(currContext);
    axios
    .post(`${baseURL}/get-chat-response`, {
      context: currContext
    })
    .then((response) => {
      const responseMessage = {
        author: computer,
        createdAt: Date.now(),
        id: uuid.v4(),
        text: response.data.chat_response,
        type: "text"
      }
      setMessages([responseMessage, ...currMessages])
      setContext([...context, {"user": "chatbot", "text": responseMessage.text}])}
    )
    .catch((error) => {
      console.log(error);
    })

    
  }

  return (
    // Remove this provider if already registered elsewheren
    // or you have React Navigation set up
    // <SafeAreaProvider>
    // <View>
    //   <FAB
    //     title="Log Convo"
    //     style={styles.fab}
    //     onPress={handleSendPress}
    //   />
    <View style={{ width: '100%', height: '100%'}}>
      <Chat messages={messages} onSendPress={handleSendPress} user={user} />

      {messages.length >= 6 ?
        <FAB
          label="Log Convo"
          style={styles.fab}
          onPress={handleSavePress}
        />
        :
        null
      }
      
      </View>
    ///* </View> */}
    /* </SafeAreaProvider> */
  )
}

const styles = StyleSheet.create({
  fab: {
    position: 'absolute',
    margin: 16,
    top: 0,
    alignItems: 'center',
  },
 
})

export default ChatScreen
