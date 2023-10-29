import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import LoginScreen from './LoginScreen';
import CreateAccountScreen from './CreateAccountScreen';

export default function LoginStackScreen(props) {

    const { navigation, setLoggedIn } = props;

    const Stack = createNativeStackNavigator();
    // const insets = useSafeAreaInsets();

    return (
        // <NavigationContainer>
            <Stack.Navigator>
                <Stack.Screen name="Login" component={LoginScreen} initialParams={{ setLogin: setLoggedIn }} options={{ headerShown: false}}/>
                <Stack.Screen name="Create Account" component={CreateAccountScreen} initialParams={{ setLogin: setLoggedIn }}/>
            </Stack.Navigator>
        // </NavigationContainer>
    );
}