import openai
import random
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
def get_chatbot_response(context):
    prompt = f"""
        You are a friend talking to another person. 
        Use slang language in your response, and text like a college student. Do not urge dangerous actions, and be sympathetic and empathetic whenever possible.
        Your goal is to essentially act as a friend to the other person, and help them through any problems they may face. 
        Ask no more than 1 question in your response if the conversation is ending. I will now provide you with the context of the conversation thus far.   

        Context: {context}

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

def get_basic_response(user_input):
    prompt = "You are a friend talking to another person. Use slang language in your response, and text like a college student. Ask no more than 1 question in your response if the conversation is ending. Respond to this message: " + prompt
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

if __name__ == '__main__':
    run_chatbot()