# Importing the requires libraries for webscrapping and discord
import time
import pandas as pd
import discord
import responses
import random
import os
import datetime
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Creating arrays for storage and a url vairable to reference leetcode website
siteUrl = 'https://leetcode.com/problemset/all/'
easyQuestionNameList = []
easyQuestionUrlList = []
mediumQuestionNameList = []
mediumQuestionUrlList = []
hardQuestionNameList = []
hardQuestionUrlList = []

# Creating variables to run the bot and its various functions
global currentNum
currentNum = 0
load_dotenv()

# Stores the collected data in pandas
def storeData():

    # Creating the Easy, Medium, and Hard data structures to store questions
    easy = {
        'Name': easyQuestionNameList,
        'URL': easyQuestionUrlList,
        'Status': False
    }

    medium = {
        'Name': mediumQuestionNameList,
        'URL': mediumQuestionUrlList,
        'Status': False
    }

    hard = {
        'Name': hardQuestionNameList,
        'URL': hardQuestionUrlList,
        'Status': False
    }

    # Creating the pandas for easy access to questions
    global easyPanda
    easyPanda = pd.DataFrame(easy)
    global mediumPanda
    mediumPanda = pd.DataFrame(medium)
    global hardPanda 
    hardPanda = pd.DataFrame(hard)

# Opens a headless browser in chrome
def openBrowser(url):
    print("     -----------> Opening Browser")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # headless browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    driver.maximize_window()
    return driver

# Closes the headless browser
def closeBrowser(driver):
    print("     -----------> Closing Browser")
    driver.close()

# Gets data from a single page
def fetchPageData(pageUrl):
    # Allow time for data to load
    sleepTime = 3

    # print("Page URL: ", pageUrl)
    browser = openBrowser(pageUrl)
    time.sleep(sleepTime)
    pageSource = browser.page_source
    WebDriverWait(browser, 10).until(EC.title_contains("Problems - LeetCode"))
    # print(f"title is: {browser.title}")

    soup = BeautifulSoup(pageSource, 'html.parser')
    if (browser.title == "Problems - LeetCode"):
        print(
            "\n\n                     ------------------- Parsing data -------------------\n\n"
        )

        #Fetching all the questions on the page and storing them in questionList
        newSoup = BeautifulSoup(pageSource, 'html.parser')
        questionBlock = newSoup.find('div', role='rowgroup')
        questionList = questionBlock.find_all('div', role='row')
        print(f"Total {questionList.__len__()} data fetched ")

        # Getting the required information for each question on the page
        for question in questionList:
            row = question.find_all('div', role='cell')
            questionName = row[1].find('a').text # Find the a tag in the first row, take it's text attribute
            questionUrl = row[1].find('a')['href'] # Find the a tag in the first row, take it's href attribute
            questionUrl = 'https://leetcode.com' + questionUrl
            questionDifficulty = row[4].find('span').text # Finding the span within the 4th row, take its text attribute

            # Storing the data in the corresponding arrays
            if questionDifficulty == 'Easy':
                easyQuestionNameList.append(questionName)
                easyQuestionUrlList.append(questionUrl)
            elif questionDifficulty == 'Medium':
                mediumQuestionNameList.append(questionName)
                mediumQuestionUrlList.append(questionUrl)
            else:
                hardQuestionNameList.append(questionName)
                hardQuestionUrlList.append(questionUrl)
        print("     -----------> Done")
        closeBrowser(browser)

    # Handling Errors
    else:
        print("Page does not exist o connection Failed, status code: ",
              soup.status_code)
    return

# Gets data from all pages on the website
def getData():

    try:

        # Opening the browser using the function created eariler
        browser = openBrowser(siteUrl) 
        # Waiting 2 seconds to allow the data to load
        time.sleep(2) 
        # Waiting another 10 seconds at maximum for the page to whole page to load
        WebDriverWait(browser, 10).until(EC.title_contains("Problems - LeetCode"))
        # Creating required variables and objects (collecting the source code for the page)
        pageSource = browser.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')

        # If the page loaded properly then we can proceed
        if (browser.title == "Problems - LeetCode"):

            # print(f"Total {totalQuestion} questions available")
            totalPage = 50
            print(f"Total {totalPage} pages available")
            closeBrowser(browser)

            # Fetching data from each page
            for page in range(1, totalPage + 1):
                print(
                    f"\n\n                     ------------------- Fetching Page {page} -------------------\n\n"
                )
                pageUrl = siteUrl + '?page=' + str(page)
                fetchPageData(pageUrl)

            print("     -----------> Done all pages ")
            storeData()

        # Error Handling
        else:
            print("Connection Failed")
            return

    except Exception as e:
        print("Some error occured, error: ", e)
        return

# Generates a random easy question
def randomEasy():
    index  = random.randint(0, len(easyQuestionNameList) - 1)

    if False in easyPanda.values:
        while easyPanda.at[index, 'Status'] == True:
            index  = random.randint(0, len(easyQuestionNameList) - 1)
        
        name = easyPanda.at[index, 'Name']
        url = easyPanda.at[index, 'URL']
        easyPanda.iloc[index].replace(to_replace=False, value = True)

        return str(name) + ': ' + url
    else:
        return 'All Easy Leetcode Questions Have been complete'

# Generates a random medium question
def randomMedium():
    index  = random.randint(0, len(mediumQuestionNameList) - 1)

    if False in mediumPanda.values:
        while mediumPanda.at[index, 'Status'] == True:
            index  = random.randint(0, len(mediumQuestionNameList) - 1)
        
        name = mediumPanda.at[index, 'Name']
        url = mediumPanda.at[index, 'URL']
        mediumPanda.iloc[index].replace(to_replace=False, value = True)

        return str(name) + ': ' + url
    else:
        return 'All Medium Leetcode Questions Have been complete'

# Generates a random hard question    
def randomHard():
    index  = random.randint(0, len(hardQuestionNameList) - 1)

    if False in hardPanda.values:
        while hardPanda.at[index, 'Status'] == True:
            index  = random.randint(0, len(hardQuestionNameList) - 1)
        
        name = hardPanda.at[index, 'Name']
        url = hardPanda.at[index, 'URL']
        hardPanda.iloc[index].replace(to_replace=False, value = True)

        return str(name) + ': ' + str(url)
    else:
        return 'All Hard Leetcode Questions Have been complete'

# Returns a question of easy difficulty
def dailyLeetcode(index):
    # Check if the index is in range
    if (index + 1) in range(len(hardQuestionNameList)):
        
        # Create variables for eahc question type to return
        easyName = easyPanda.at[index, 'Name']
        easyUrl = easyPanda.at[index, 'URL']
        mediumName = mediumPanda.at[index, 'Name']
        mediumUrl = mediumPanda.at[index, 'URL']
        hardName = hardPanda.at[index, 'Name']
        hardUrl = hardPanda.at[index, 'URL']

        # Increase the index by 1
        currentNum = index + 1

        # Return the leetcode of the day
        return '\u0332'.join('LEETCODE OF THE DAY:') + '\n\nEasy - ' + str(easyName) + ': ' + str(easyUrl) + '\n\nMedium - ' + str(mediumName) + ': ' + str(mediumUrl) + '\n\nHard - ' + str(hardName) + ': ' + str(mediumUrl)
    else:
        # If all indexes have been exausted
        return 'All Questions have been completed' 

# Responds to the user
async def sendMessage(message, user_message):
    try:
        response = responses.handle_response(user_message)
        print(message.channel)
        await message.channel.send(response)
    except Exception as e:
        print(e)

# Function which is called continousily while the bot is active
def runDiscordBot():
    # Initializing the variables for the bot
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.all()
    intents.guilds = True
    client = discord.Client(command_prefix='!', intents=intents)
    bot = commands.Bot(command_prefix='!', intents=intents)
    time = datetime.time(23, 55)

    # Calls dailyLeetcode function once a day at 12:00 EST
    async def daily():
        # Keeps the loop running endlessly
        while True:
            # Calculating wait-time
            now = datetime.datetime.now()
            then = now + datetime.timedelta(days=1)
            then.replace(hour=12, minute=0, second=0)
            wait_time = (then - now).total_seconds()

            # Waiting the required amount the calling the desired function at the correct time
            await asyncio.sleep(wait_time)
            await channel.send(dailyLeetcode(currentNum))
            
    # Gets called when the bot is ready
    @client.event
    async def on_ready():
        # For testing, lets us know the bot is running
        print('We have logged in as {0.user}'.format(client))

        # Storing the channel id in a global variable
        global channel
        channel = client.get_channel(920108137313349645)

        # Calls the loop
        await daily()

    # Responds to the user's message
    @client.event
    async def on_message(message):
        # If the bot says something, do not respond
        if message.author == client.user:
            return
        
        # Store important information in variables
        username = str(message.author)
        userMessage = str(message.content)
        channel = str(message.channel)

        # For testing, prints chat history
        print(f"{username} said: '{userMessage}' ({channel})")

        # If the message starts with a '!' then it is probably a command, try to respond to the message
        if userMessage[0] == '!':
            userMessage = userMessage[1:]
            await sendMessage(message, userMessage)

    # Run the bot
    client.run(TOKEN)

