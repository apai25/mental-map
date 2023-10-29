from hume import HumeStreamClient
from hume.models.config import LanguageConfig
import os

HUME_CLIENT_KEY = os.environ['HUME_CLIENT_KEY']
async def get_sentiments(text):
    client = HumeStreamClient(HUME_CLIENT_KEY)
    config = LanguageConfig()
    emotions_lst = ['Admiration', 'Adoration', 'Aesthetic Appreciation', 'Amusement', 'Anger', 'Annoyance', 'Anxiety', 'Awe', 
                    'Awkwardness', 'Boredom', 'Calmness', 'Concentration', 'Confusion', 'Contemplation', 'Contempt', 'Contentment', 
                    'Craving', 'Determination', 'Disappointment', 'Disapproval', 'Disgust', 'Distress', 'Doubt', 'Ecstasy', 
                    'Embarrassment', 'Empathic Pain', 'Enthusiasm', 'Entrancement', 'Envy', 'Excitement', 'Fear', 'Gratitude', 
                    'Guilt', 'Horror', 'Interest', 'Joy', 'Love', 'Nostalgia', 'Pain', 'Pride', 'Realization', 'Relief', 'Romance', 
                    'Sadness', 'Sarcasm', 'Satisfaction', 'Desire', 'Shame', 'Surprise (negative)', 'Surprise (positive)', 
                    'Sympathy', 'Tiredness', 'Triumph']
    N_EMOTIONS = len(emotions_lst)
    emotions_dict = {e: 0 for e in emotions_lst}

    async with client.connect([config]) as socket:
        result = await socket.send_text(text)
        N = len(result['language']['predictions'])
        for i in range(N):
            curr_word = result["language"]["predictions"][i]["emotions"]
            for j in range(N_EMOTIONS):
                emotions_dict[emotions_lst[j]] += curr_word[j]['score']
    
    scores = [emotions_dict[i] for i in emotions_lst]
    IMPORTANT_EMOTIONS = {"Anger": 4, "Anxiety": 6, "Disappointment": 18, "Excitement": 29, "Fear": 30, 
                          "Joy": 35, "Love": 36, "Pain": 38, "Sadness": 43, "Tiredness": 51}
    sentiments = {i: scores[IMPORTANT_EMOTIONS[i]] for i in IMPORTANT_EMOTIONS}
    return sentiments

# print(asyncio.run(get_sentiments("i just finished coding my calhacks project after 15 hours!")))