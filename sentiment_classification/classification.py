import asyncio # must import asyncio to run the actual function

# import subprocess
# python_executable = '/usr/local/bin/python3'
# package_names = ['hume', 'hume[stream]', 'websockets']
# for package_name in package_names:
#     subprocess.check_call([python_executable, '-m', 'pip', 'install', package_name])

from hume import HumeStreamClient
from hume.models.config import LanguageConfig

# import sys
# {sys.executable} -m pip install "hume[stream]"
# {sys.executable} -m pip install hume
# {sys.executable} -m pip install websockets


async def main(text):
    client = HumeStreamClient("sa4h1KJloRvXssnhlFfGTldG7QiaYyVrJgWrUNR3y0KWzGA8")
    config = LanguageConfig()
    async with client.connect([config]) as socket:
        result = await socket.send_text(text)
        emotions = result["language"]["predictions"][0]["emotions"]
    scores = [emotions[i]["score"] for i in range(53)]
    emotions = ['Admiration', 'Adoration', 'Aesthetic Appreciation', 'Amusement', 'Anger', 'Annoyance', 'Anxiety', 'Awe', 
                'Awkwardness', 'Boredom', 'Calmness', 'Concentration', 'Confusion', 'Contemplation', 'Contempt', 'Contentment', 
                'Craving', 'Determination', 'Disappointment', 'Disapproval', 'Disgust', 'Distress', 'Doubt', 'Ecstasy', 
                'Embarrassment', 'Empathic Pain', 'Enthusiasm', 'Entrancement', 'Envy', 'Excitement', 'Fear', 'Gratitude', 
                'Guilt', 'Horror', 'Interest', 'Joy', 'Love', 'Nostalgia', 'Pain', 'Pride', 'Realization', 'Relief', 'Romance', 
                'Sadness', 'Sarcasm', 'Satisfaction', 'Desire', 'Shame', 'Surprise (negative)', 'Surprise (positive)', 
                'Sympathy', 'Tiredness', 'Triumph']
    index, maximum = -1, 0
    for i in range(53):
        if scores[i] > maximum:
            maximum, index = scores[i], i
    return emotions[index]

# print(asyncio.run(main(text="")))