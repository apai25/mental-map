import openai
import random
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
def get_chatbot_response(context):
    formatted_context = parse_context(context)
    prompt = f"""
        You are a friend talking to another person. 
        Use slang language in your response, and text like a college student. Do not urge dangerous actions, and be sympathetic and empathetic whenever possible.
        Your goal is to essentially act as a friend to the other person, and help them through any problems they may face. 
        Ask no more than 1 question in your response if the conversation is ending. I will now provide you with the context of the conversation thus far.   

        Context: {formatted_context}

        Please respond to the above context in a way that is compliant with the information about your goal and task. 
        """
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other models like text-davinci-003
        prompt=prompt,
        max_tokens=100,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.6  # Adjust for desired randomness
    )
    return response.choices[0].text.strip()

def parse_context(context):
    parsed = ""
    for entry in context:
        if entry['user'] == 'chatbot':
            parsed += f'you: {entry["text"]},'
        elif entry['user'] == 'user':
            parsed += f'user: {entry["text"]}, '
    return parsed[:-2]

# daily summary is in first-person
def get_daily_summary(context):
    # context: [{"user": "INSERT_USER", "text": "INSERT_YOUR_TEXT"}, ...] # user = 'chatbot' or 'user'
    formatted_context = parse_context(context)
    prompt = f"""
        Your goal is to summarize this entire conversation about a person's life below.
        Respond in first-person perspective with words like "I" as if you are the person you're describing.
        Summarize the given information as if it were a diary of entries of the current day. 
        You will be given a long string transcript of your conversation where 'you' is what you said and 'user' is what the other person said.
        Use slightly informal language in your summary. I will now provide you with the context of the conversation thus far.

        Context: {formatted_context}

        Please respond to the above context in a way that is compliant with the information about your goal and task.
        """
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other models like text-davinci-003
        prompt=prompt,
        max_tokens=100,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.6  # Adjust for desired randomness
    )
    return response.choices[0].text.strip()


def get_weekly_summary(daily_summaries):
    # list_of_dicts: [{"sentiment": "INSERT_SENTIMENT", "text": "INSERT_TEXT"}]
    all_sentiments = {}
    for dict in daily_summaries:
        all_sentiments[dict["sentiment"]] = dict["text"]
    
    prompt = f"""
        Your goal is to summarize all of the events given to you about a person's life below.
        Respond in second-person perspective with words like "you" as if you're communicating with the person you're describing.
        Summarize the given information as if it were a diary of entries over the past week. 
        You will be given a dictionary that maps a person's sentiment to the event that occurred, which represents their diary entries.
        If the sentiment is "Excitement", "Joy", or "Love", summarize those events first in your response.
        Lastly, if the sentiment is "Anger", "Anxiety", "Disappointment", "Fear", "Pain", "Sadness", or "Tiredness", summarize those events last.
        Try to make those summaries sound more positive, and spend less time on the negative events.
        Use slightly informal language in your response.
        Respond with no more than 2 sentences per event. I will now provide you with the diary entries thus far.

        Context: {all_sentiments}

        Please respond to the above context in a way that is compliant with the information about your goal and task.
        """
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other models like text-davinci-003
        prompt=prompt,
        max_tokens=700,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.6  # Adjust for desired randomness
    )
    return response.choices[0].text.strip()


# THESE ARE OLD UNUSED FUNCTIONS
def get_basic_response(user_input):
    prompt = "You are a friend talking to another person. Use slang language in your response, and text like a college student. Ask no more than 1 question in your response if the conversation is ending. Respond to this message: " + user_input
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other models like text-davinci-003
        prompt=prompt,
        max_tokens=100,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.6  # Adjust for desired randomness
    )
    return response.choices[0].text.strip()

def run_chatbot():
    questions = ["Rose?", "Bud?", "Thorn?"]
    openai.api_key = OPENAI_API_KEY

    start = True
    while True:
        if start:
            print("To end your conversation, please enter any of the following: 'Quit', 'Exit', 'Q', or 'Done'")
            user_input = input(random.choice(questions) + " You: ")
            start = False
        else:
            user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit', 'q', 'done']:
            print("Exiting...")
            break

        gpt3_response = get_basic_response(user_input)
        print(f"Chat: {gpt3_response}")


# for testing purposes, use list_of_dicts to generate a summary of this week's entries
if __name__ == '__main__':
    # run_chatbot()
    list_of_dicts = [{"sentiment": "Sadness", "text": "I am feeling really bad because my girlfriend turned gay. I don't know what to do. She does not love me anymore. She started liking women after we had our first baby. She wants to raise our baby with her lesbian lover, which makes this really hard for me. I have lost my first marriage, and I am distraught."},
                    {"sentiment": "Anger", "text": "My boyfriend cheated on me when we were on a break, as he says. I needed some space away from our relationship, so I wanted a break from him. But that same night, he had sex with a random woman, and I found out through somebody else. I'm so upset with him, and I never want to see him ever again."},
                    {"sentiment": "Excitement", "text": "I just proposed to my fiancee, and she said yes! I will be getting married to the hottest, sexiest, most attractive white women in New York. This is absolutely fantastic, and my entire family has approved of the marriage, too! I can't wait to be a newly wed, and we have started planning our wedding now."},
                    {"sentiment": "Anxiety", "text": "I have a presentation at my paleontology museum very soon, but I am not ready for it. I have not had enough time to prepare for my presentation yet. My boss will be at this presentation, so if I don't do well, he will fire me. I need to someone figure out how to do this presentation well."},
                    {"sentiment": "Joy", "text": "I just won the Calhacks hackathon for my project about cybersecurity malware detection. This is so amazing, because I will be making a million dollars, and I get direct entry to the Y Combinator startups. I will be able to pursue this project full-time out of undergrad, and I can't wait to work on this project next summer."}]
    # summary = get_chatbot_summary(list_of_dicts=list_of_dicts)
    # print(summary)
    context = [{"user": "user", "text": "I am feeling really bad because my girlfriend turned gay. I don't know what to do. She does not love me anymore. She started liking women after we had our first baby. She wants to raise our baby with her lesbian lover, which makes this really hard for me. I have lost my first marriage, and I am distraught."},
               {"user": "chatbot", "text": "I'm sorry to hear that, bro. That's a tough spot to be in. Do you want to talk about it more?"},
               {"user": "user", "text": "Yes, I do. I have no clue what to do with my wife. We just got married, and I don't want to get a divorce already."},
               {"user": "chatbot", "text": "LOL sounds like u got urself in a pickle. Marriage is a tough gig, so don't be too hard on yourself. Have you tried couples counseling?"},
               {"user": "user", "text": "I mean, if she's lesbian, that means she don't want my dick and she want some pussy instead bruh."},
               {"user": "chatbot", "text": "LOL, yeah but that's her preference. You gotta respect that. Catch up with you later?"},
               {"user": "user", "text": "done"}]
    # daily_summary = get_daily_summary(context)
    # print(daily_summary)
    # daily_sentiment = get_daily_sentiment(context)
    # print(daily_sentiment)


# print(get_chatbot_summary([{"sentiment": "positive", "text": "Great job!"},
#  {"sentiment": "negative", "text": "Terrible experience."},
#  {"sentiment": "neutral", "text": "No strong feelings either way."}]))