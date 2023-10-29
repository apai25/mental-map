import React from 'react'
import { View, StyleSheet, Text } from 'react-native';
import { Avatar, Button, Card } from 'react-native-paper';
import Emotion from './Emotion';


const MoodView = (props) => {
    const { title, sentiments } = props;

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


    return (
        <Card mode='elevated' style={styles.container}>
            <Card.Content>
                <Text style={styles.title}>{title}</Text>
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
                    <Emotion emoji={emojis[sentiments[0].sentiment]} percent={sentiments[0].percent} sentiment={sentiments[0].sentiment}/>
                    <Emotion emoji={emojis[sentiments[1].sentiment]} percent={sentiments[1].percent} sentiment={sentiments[1].sentiment}/>
                    <Emotion emoji={emojis[sentiments[2].sentiment]} percent={sentiments[2].percent} sentiment={sentiments[2].sentiment}/>
{/* 
                    // <Text style={{...styles.text, flex: 1}}>{emojis[sentiments[0].sentiment]}</Text>
                    // <Text style={{...styles.text, flex: 2}}>{emojis[sentiments[1].sentiment]}</Text>
                    // <Text style={{...styles.text, flex: 3}}>{emojis[sentiments[2].sentiment]}</Text> */}
                </View>
            </Card.Content>
        </Card>
    )
}

const styles = StyleSheet.create({
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
        width: 30,
        fontSize: 60,
        textAlign: 'center'
    }
})

export default MoodView