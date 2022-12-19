import bot

# Function to handle responses from the user
def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'start-daily':
        cycle = True
        return 'You will now receive 3 questions every day at 12:00pm EST'
    elif p_message == 'random-easy':
        return bot.randomEasy()
    elif p_message == 'random-medium':
        return bot.randomMedium()
    elif p_message == 'random-hard':
        return bot.randomHard()
    elif p_message == 'end-daily':
        cycle = False
        return 'I have ended the Daily Leetcode Cycle'
    elif p_message == 'help':
        response = ("These are my functions:\n!start-daily: I can start the daily leetcode cycle for you (1 problem of each difficulty every day)\n\n!end-daily: I can end the daily leetcode cycle for you\n\n!random-easy: I can pick a random easy problem for you\n\n!random-medium: I can pick a random medium problem for you\n\n!random-hard: I can pick a random hard problem for you")
        return response
    else:
        return "I didn't quite catch that. If you need help remembering what I can do, type !help"