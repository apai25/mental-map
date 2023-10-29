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
    async with client.connect([config]) as socket:
        result = await socket.send_text(text)
        emotions = result["language"]["predictions"][0]["emotions"]
    N_EMOTIONS = 53
    scores = [emotions[i]["score"] for i in range(N_EMOTIONS)]
    emotions = ['Admiration', 'Adoration', 'Aesthetic Appreciation', 'Amusement', 'Anger', 'Annoyance', 'Anxiety', 'Awe', 
                'Awkwardness', 'Boredom', 'Calmness', 'Concentration', 'Confusion', 'Contemplation', 'Contempt', 'Contentment', 
                'Craving', 'Determination', 'Disappointment', 'Disapproval', 'Disgust', 'Distress', 'Doubt', 'Ecstasy', 
                'Embarrassment', 'Empathic Pain', 'Enthusiasm', 'Entrancement', 'Envy', 'Excitement', 'Fear', 'Gratitude', 
                'Guilt', 'Horror', 'Interest', 'Joy', 'Love', 'Nostalgia', 'Pain', 'Pride', 'Realization', 'Relief', 'Romance', 
                'Sadness', 'Sarcasm', 'Satisfaction', 'Desire', 'Shame', 'Surprise (negative)', 'Surprise (positive)', 
                'Sympathy', 'Tiredness', 'Triumph']
    index, maximum = -1, 0
    for i in range(N_EMOTIONS):
        if scores[i] > maximum:
            maximum, index = scores[i], i
    return emotions[index]