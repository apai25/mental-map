// In App.js in a new project

import * as React from 'react';
import { View, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import JournalScreen from './screens/journal/CumulativeScreen';
import ChatScreen from './screens/chat/ChatScreen';
import { SafeAreaProvider } from "react-native-safe-area-context"
import MainScreen from './MainScreen';

// const Stack = createNativeStackNavigator();

function App() {
  return (
    <SafeAreaProvider>
      <MainScreen />
    </SafeAreaProvider>
  );
}

export default App;