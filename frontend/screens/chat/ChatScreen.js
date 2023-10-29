import { Chat } from "@flyerhq/react-native-chat-ui"
import React, { useState } from "react"
import { SafeAreaProvider } from "react-native-safe-area-context"

// For the testing purposes, you should probably use https://github.com/uuidjs/uuid
const uuidv4 = () => {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, c => {
    const r = Math.floor(Math.random() * 16)
    const v = c === "x" ? r : (r % 4) + 8
    return v.toString(16)
  })
}

const ChatScreen = () => {
  const [messages, setMessages] = useState([])
  const user = { id: "06c33e8b-e835-4736-80f4-63f44b66666c" }
  const computer = { id: "4a7f9d12-9c24-4e0f-b0db-88e506acddc7" }

  const addMessage = message => {
    setMessages([message, ...messages])
  }

  const handleSendPress = message => {
    const textMessage = {
      author: user,
      createdAt: Date.now(),
      id: uuidv4(),
      text: message.text,
      type: "text"
    }

    const responseMessage = {
      author: computer,
      createdAt: Date.now(),
      id: uuidv4(),
      text: ":)",
      type: "text"
    }

    setMessages([responseMessage, textMessage, ...messages])
    // addMessage(textMessage)
    // addMessage(responseMessage)
  }

  return (
    // Remove this provider if already registered elsewheren
    // or you have React Navigation set up
    // <SafeAreaProvider>
      <Chat messages={messages} onSendPress={handleSendPress} user={user} />
    /* </SafeAreaProvider> */
  )
}

export default ChatScreen
