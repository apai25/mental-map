import asyncio # must import asyncio to run the actual function

# import subprocess
# python_executable = '/usr/local/bin/python3'
# package_names = ['hume', 'hume[stream]', 'websockets']
# for package_name in package_names:
#     subprocess.check_call([python_executable, '-m', 'pip', 'install', package_name])

from hume import HumeStreamClient
from hume.models.config import LanguageConfig
import os

HUME_CLIENT_KEY = os.environ['HUME_CLIENT_KEY']
async def get_sentiment(text):
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
    important_emotions = {"Anger": 4, "Anxiety": 6, "Disappointment": 18, "Excitement": 29, "Fear": 30, 
                          "Joy": 35, "Love": 36, "Pain": 38, "Sadness": 43, "Tiredness": 51}
    important_scores = [scores[i] for i in important_emotions.values()]
    index, maximum = -1, 0
    for i in range(len(important_emotions)):
        if important_scores[i] > maximum:
            maximum, index = important_scores[i], i
    return list(important_emotions.keys())[index]

# print(asyncio.run(get_sentiment("insert input text here")))