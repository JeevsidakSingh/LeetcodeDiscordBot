import bot

# Function to handle responses from the user
def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'random-easy':
        return bot.randomEasy()
    elif p_message == 'random-medium':
        return bot.randomMedium()
    elif p_message == 'random-hard':
        return bot.randomHard()
    elif p_message == 'help':
        response = ("These are my functions:\n\n!random-easy: I can pick a random easy problem for you\n\n!random-medium: I can pick a random medium problem for you\n\n!random-hard: I can pick a random hard problem for you\n\nI will also send out 3 daily leetcode problems at 12:00 EST everyday")
        return response
    else:
        return "I didn't quite catch that. If you need help remembering what I can do, type !help"