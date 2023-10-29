from sentiment_classification import get_sentiments
import psycopg
from random import choice
import asyncio

conn = psycopg.connect("postgresql://apai25:ZqZMx32nohbDmTaTwOqGZQ@mental-map-3658.g95.cockroachlabs.cloud:26257/defaultdb?sslmode=require")
EMOTIONS = ['Anger', 'Anxiety', 'Disappointment', 'Excitement', 'Fear', 'Joy', 'Love', 'Pain', 'Sadness', 'Tiredness']

EMAILS = ['test1@gmail.com', 'test2@gmail.com']
PASSWORDS = ['password1', 'password2']

def populate_users():
    for i in range(len(EMAILS)):
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user_information (email, user_password) VALUES (%s, %s)",
                (EMAILS[i], PASSWORDS[i])
            )
        conn.commit()

async def populate_entries(entries):
    count = 1
    for entry in entries:
        summary = entry['summary']
        date = entry['date']

        sentiments = await get_sentiments(summary)


        with conn.cursor() as cursor:
            user_email = choice(EMAILS)
            cursor.execute(
                "SELECT user_id FROM user_information WHERE email = %s", (user_email, )
            )
            user_id = cursor.fetchone()[0]
        conn.commit()

        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO diary_entries (entry_id, user_id, entry_date, entry_text, anger, anxiety, disappointment, excitement, fear, joy, love, pain, sadness, tiredness) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (count, user_id, date, summary, sentiments['Anger'], sentiments['Anxiety'], sentiments['Disappointment'], sentiments['Excitement'], sentiments['Fear'], sentiments['Joy'], sentiments['Love'], sentiments['Pain'], sentiments['Sadness'], sentiments['Tiredness'])
            )
            
        conn.commit()
        print(count)
        count += 1

if __name__ == '__main__':
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS diary_entries")
        cursor.execute("DROP TABLE IF EXISTS user_information")
        
    conn.commit()
    print('done dropping')

    with conn.cursor() as cursor:
        cursor.execute(
            """
                CREATE TABLE diary_entries (
                    entry_id STRING,
                    user_id INT,
                    entry_date VARCHAR,
                    entry_text VARCHAR,
                    anger FLOAT,
                    anxiety FLOAT,
                    disappointment FLOAT,
                    excitement FLOAT,
                    fear FLOAT,
                    joy FLOAT,
                    love FLOAT,
                    pain FLOAT,
                    sadness FLOAT,
                    tiredness FLOAT
                )
            """
        )

        cursor.execute(
            """
                CREATE TABLE user_information (
                    user_id SERIAL PRIMARY KEY,
                    email VARCHAR,
                    user_password VARCHAR
                )
            """
        )
    conn.commit()

    print('done creating')
    populate_users()
    print('Populating users...DONE')
    ex1 = {'summary': "Today was a day of celebration! I just got an internship at Apple for summer 2024 in ML/AI. After applying online and going through a rigorous interview process, I was thrilled to hear the good news. I'll be working on a mix of computer vision and natural language processing projects, which I'm really looking forward to. I'm a bit nervous about the high expectations, but I'm reminded of the faith Apple has in my skills and potential. I'm going to give this my all.", 'sentiments': {'Excitement': 60.33475588335631,'Joy': 23.690672813882667,'Anxiety': 15.974571302761017}, 'date': '2023-10-25'}
    ex2 = {'summary': "Today has been a tough one. I found out that my girlfriend had cheated on me and it's been a huge blow to my trust. I thought we had something special, but now I feel betrayed. Thankfully, I have a friend who's been supportive and understanding, and who's given me the space to open up and talk about what happened. I'm still feeling the pain, but I'm trying to remember that I'm strong and I'll get through this.", 'sentiments': {'Disappointment': 34.78068937076821,'Sadness': 34.766696837210866,'Pain': 30.452613792020937}, 'date': '2023-10-22'}
    ex3 = {'summary': "I was feeling overwhelmed about the upcoming computer science midterm on optimizing algorithms and intractable problems. I was grateful for my friend's encouragement, and I'm doing my best to prepare by reviewing class notes, doing practice problems, and watching online tutorials. I'm trying to be mindful of taking breaks and getting rest, understanding that the process is just as important as the result. I'm breaking it down and tackling one concept at a time.", 'sentiments': {'Anxiety': 60.09055119187781,'Tiredness': 28.412389139045164,'Fear': 11.497059669077036}, 'date': '2023-10-27'}
    ex4 = {'summary': "I finally confessed my feelings to my crush and she told me she likes me back! I'm over the moon and I think I might be in love with her. Now, I'm looking forward to getting to know her better and maybe planning a nice date. I'm so grateful for the support I've received and am excited to embark on this new chapter of my life.", 'sentiments': {'Love': 42.79288339475731,'Joy': 30.349479687422203,'Excitement': 26.857636917820493}, 'date': '2023-10-23'}
    ex5 = {'summary': "My beloved cat, who had been with me for 15 years, passed away yesterday. We had so many memories together, from the day we first brought her home as a tiny ball of fur to the many adventures we had over the years. It's tough to imagine coming home without her there. Talking about it helps, though, and I'm grateful for the time we had together. I'm also thankful for the support of my friends.", 'sentiments': {'Sadness': 45.76713114103804,'Love': 30.701021772652602,'Pain': 23.531847086309355}, 'date': '2023-10-26'}
    ex6 = {'summary': "Today was a really scary day. I was trying to do a parkour move, but I lost my footing and ended up falling off a building. Thankfully, I'm at the hospital now and it looks like nothing is broken, but I'm still pretty banged up. I'm just glad to be alive, and I know now that I need to prioritize safety when it comes to pursuing my passions. My friend was understanding and reminded me to take the time to rest and recover.", 'sentiments': {'Fear': 43.73803460319453,'Anxiety': 31.37518778363556,'Tiredness': 24.8867776131699}, 'date': '2023-10-24'}
    ex7 = {'summary': "Today was a difficult day. I woke up hungover and with no recollection of what had happened the night before. I was worried that I might have done something I would regret. Thankfully, my friend was there for me and offered support. We discussed ways to figure out what had happened, like checking my phone for texts or calls. They reminded me to focus on taking care of myself first, and that this was a learning experience. I'm grateful for their understanding and support.", 'sentiments': {'Tiredness': 42.140341844550925,'Anxiety': 30.488686630594408,'Sadness': 27.37097152485467}, 'date': '2023-10-28'}
    ex8 = {'summary': "Today was a great day. I had the most romantic date at a fancy restaurant with dim lighting, soft music, and delicious food. We even had a private corner overlooking the city lights. We talked about everything - our dreams, favorite books, and even our childhood memories. My date even surprised me with a special dessert with 'Congratulations' written in chocolate - they had heard about my recent promotion! We're already planning a weekend getaway to a cozy cabin in the mountains.", 'sentiments': {'Joy': 42.317625995351364,'Love': 32.88015333784602,'Excitement': 24.802220666802626}, 'date': '2023-10-21'}
    ex9 = {'summary': "Today was a long day. My team and I worked hard all night on a cybersecurity project for the Cal Hacks 10.0 hackathon. We put together a malware detection system that we are all proud of. Despite the exhaustion, we're still pumped up and ready to make some final adjustments before the submission. We want the user interface to be perfect, so we're putting in the extra effort. I'm a bit nervous about presenting it, but I'm sure all the hard work will pay off.", 'sentiments': {'Tiredness': 56.41072398109108,'Anxiety': 22.064660838162702,'Excitement': 21.524615180746228}, 'date': '2023-10-20'}
    ex10 = {'summary': "Today was a great day. I got assigned to work on a project with IKEA through my college tech consulting club. It's focused on optimizing the online customer experience and I'll be diving into UX/UI design and data analysis. I'm so excited to learn and contribute! I'm planning to do some research on IKEA's current online platforms and customer feedback, then come up with some creative solutions with the team. My friend was a great source of encouragement and showed their support.", 'sentiments': {'Excitement': 70.78050303882928,'Joy': 27.433368124331793,'Love': 1.7861288368389336}, 'date': '2023-10-28'}
    ENTRIES = [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10]
    asyncio.run(populate_entries(ENTRIES))
    print('Populating entries...DONE')