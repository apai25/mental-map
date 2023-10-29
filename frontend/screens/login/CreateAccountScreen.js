import React from 'react'
import { View, Image, Text, StyleSheet } from 'react-native'
import { TextInput, Button } from 'react-native-paper';

const CreateAccountScreen = (props) => {

  const { setLoggedIn } = props;
  
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");



  const login = () => {
    setLoggedIn(true);
  }

  return (
    <View style={styles.centered}>
      <Image
        style={styles.icon}
        source={require('../../assets/brain-icon.png')}
      />
      {/* <Image
        style={styles.logo}
        source={require('../../assets/mentalmap-logo.png')}
      /> */}
      <TextInput
        mode='outlined'
        label="Email"
        value={email}
        onChangeText={email => setEmail(email)}
        style={styles.textField}
      />
      <TextInput
        mode='outlined'
        secureTextEntry={true}
        label="Password"
        value={password}
        onChangeText={password => setPassword(password)}
        style={styles.textField}
      />
      <Button mode="outlined" onPress={login} style={styles.submitButton}>
        Create Account
      </Button>
      {/* <View
        style={styles.textContainer}>
        <Button mode="text" onPress={() => console.log('Pressed')} style={styles.textLeft}>
          <Text style={styles.buttonText}>Create Account</Text>
        </Button>
        <Button mode="text" onPress={() => console.log('Pressed')} style={styles.textRight}>
          <Text style={styles.buttonText}>Forgot Password?</Text>
        </Button>
      </View> */}
    </View>
  )
}

const styles = StyleSheet.create({
  centered: { 
    flex: 1, 
    justifyContent: "center", 
    alignItems: "center", 
    backgroundColor: '#F1EFE7'
  }, 
  logo: {
    width: '70%',
    height: 100,
    resizeMode: 'contain',
  },
  icon: {
    width: '10%',
    height: '5%',
    resizeMode: 'contain'
  },
  textField: {
    width: '70%',
    marginTop: '2%'
  },
  submitButton: {
    marginTop: '5%',
    fontSize: 25
  },
  textContainer: {
    marginTop: '10%',
    flexDirection: 'row',
    width: '70%',
  },
  textLeft: {
    width: '50%',
  },
  textRight: {
    width: '50%',
    textAlign: 'right'
  },
  buttonText: {
    fontSize: 12
  }
})

export default CreateAccountScreen