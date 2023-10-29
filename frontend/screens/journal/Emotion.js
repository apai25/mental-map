import React from 'react'
import { View, Text, StyleSheet } from 'react-native'
import { AnimatedCircularProgress } from 'react-native-circular-progress';


const Emotion = ({ emoji, percent, sentiment }) => {
  return (
    <View style={{ width: 110, height: 120, textAlign: 'center'}}>
        <AnimatedCircularProgress
            rotation={-90}
            size={90}
            width={4}
            fill={Math.round(percent)}
            tintColor="#B0926A"
            backgroundColor="#F1EFE7">
            {
                (fill) => (
                <View> 
                    <Text style={{textAlign: 'center', fontSize: 40}}>{emoji}</Text>
                    <Text style={{textAlign: 'center', fontSize: 15}}>{Math.round(percent)}%</Text>
                </View>
                )
            }
        </AnimatedCircularProgress>
        <Text style={{textAlign: 'center', fontSize: 11, marginTop: 10, marginRight: 25}}>{sentiment}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
    centered: { 
      alignItems: "center", 
      backgroundColor: '#F1EFE7'
    }
  })

export default Emotion