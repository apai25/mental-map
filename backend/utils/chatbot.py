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
   
    prompt = f"""
        Your goal is to summarize all of the events given to you about a person's life below.
        Respond in second-person perspective with words like "you" as if you're communicating with the person you're describing.
        Summarize the given information as if it were a diary of entries over the past week. 
        You will be given a list of diary entries after "context: ". Diary entires may vary largely, and some may be negative or positive. 
        For the final weekly summary, try to highlight the positive aspects of the user's week. Do not spend as much time on negative weeks.
        For negative events that are very, very negative, make sure to give a positive outlook that would boost the user's mental health.
        Try to make those summaries sound more positive, and spend less time on the negative events.
        Use slightly informal language in your response.
        Respond with no more than 2 sentences per event. I will now provide you with the diary entries thus far.

        Context: {daily_summaries}

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
    
    context = [
        {"user": "user", "text": "I'm really struggling with my studies. I can't seem to focus, and my grades are slipping."},
        {"user": "chatbot", "text": "I'm sorry to hear that. It's common to have academic challenges. Have you tried setting a study schedule or seeking help from a tutor?"},
        {"user": "user", "text": "Yeah, I've tried that, but it's just not working for me. I feel overwhelmed."},
        {"user": "chatbot", "text": "Don't give up. Maybe it's time to talk to your professors or a counselor about your difficulties. They can provide valuable guidance."},
        {"user": "user", "text": "You're right; I shouldn't give up so easily. Thanks for the advice."},
        {"user": "chatbot", "text": "You're welcome! Remember, there are always ways to improve. Keep pushing forward!"},
        {"user": "user", "text": "I will. Thanks for the support."},
        {"user": "chatbot", "text": "Anytime. Good luck with your studies!"},
        {"user": "user", "text": "Thanks, I appreciate it."},
        {"user": "chatbot", "text": "No problem. Let me know if you need more help."},
        {"user": "user", "text": "Sure thing."},
        {"user": "chatbot", "text": "Take care!"},
        {"user": "user", "text": "You too!"},
        {"user": "chatbot", "text": "Goodbye!"}
    ]

    context = [
        {"user": "user", "text": "I'm really excited about my upcoming vacation to Italy. It's been a dream of mine for years."},
        {"user": "chatbot", "text": "That sounds amazing! Italy is a beautiful country with so much to offer. Do you have an itinerary planned?"},
        {"user": "user", "text": "Yes, I've planned to visit Rome, Florence, and Venice. I can't wait to try the delicious Italian food."},
        {"user": "chatbot", "text": "Those are fantastic choices! The food in Italy is a real treat. Don't forget to try the gelato!"},
        {"user": "user", "text": "I've heard the gelato is a must-try. I'll definitely indulge in it. Have you been to Italy?"},
        {"user": "chatbot", "text": "No, I haven't been there, but I've heard many great things. I hope you have a fantastic trip and create wonderful memories!"},
        {"user": "user", "text": "Thank you! I can't wait to go. It's a dream come true."},
        {"user": "chatbot", "text": "I'm sure it will be an unforgettable experience. Enjoy every moment!"},
        {"user": "user", "text": "I will. Thanks for your well-wishes!"},
        {"user": "chatbot", "text": "You're welcome. Safe travels!"}
    ]

# Add more conversations as needed

    # daily_summary = get_daily_summary(context)
    # print(daily_summary)
    # daily_sentiment = get_daily_sentiment(context)
    # print(daily_sentiment)


# print(get_chatbot_summary([{"sentiment": "positive", "text": "Great job!"},
#  {"sentiment": "negative", "text": "Terrible experience."},
#  {"sentiment": "neutral", "text": "No strong feelings either way."}]))