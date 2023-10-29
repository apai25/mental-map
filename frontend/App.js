// In App.js in a new project

import * as React from 'react';
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