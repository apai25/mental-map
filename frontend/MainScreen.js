import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import JournalScreen from './screens/journal/JournalScreen';
import ChatScreen from './screens/chat/ChatScreen';
import LoginStackScreen from './screens/login/LoginStackScreen';
import LoginScreen from './screens/login/LoginScreen';
import CreateAccountScreen from './screens/login/CreateAccountScreen';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {Connect} from 'react-redux'


export default function MainScreen() {

    const Tab = createMaterialTopTabNavigator();
    const Stack = createNativeStackNavigator();
    const insets = useSafeAreaInsets();

    const [loggedIn, setLoggedIn] = useState(false);
    const [userId, setUserId] = useState("");

    return (
        <NavigationContainer>
            {loggedIn ?
                <Tab.Navigator screenOptions={{
                    tabBarStyle: {
                        marginTop: insets.top
                    }
                }}>
                    <Tab.Screen name="Chat" component={ChatScreen} initialParams={{userId: userId}} />
                    <Tab.Screen name="Journal" component={JournalScreen} initialParams={{userId: userId}}  />
                </Tab.Navigator>
            :
                <LoginStackScreen setLoggedIn={setLoggedIn} setUserId={setUserId}/>
                /* <Stack.Navigator >
                    <Stack.Screen name="Login" component={LoginScreen} />
                    <Stack.Screen name="Create Account" component={CreateAccountScreen} />
                </Stack.Navigator> */
            }
        </NavigationContainer>
    );
}