# Importing the requires libraries for webscrapping
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

siteUrl = 'https://leetcode.com/problemset/all/'
easyQuestionNameList = []
easyQuestionUrlList = []
easyQuestionDifficultyList = []


def storeData():

    data_whole = {
        'Name': easyQuestionNameList,
        'Difficulty': easyQuestionDifficultyList,
        'URL': easyQuestionUrlList
    }

    df = pd.DataFrame(data_whole)

    print(df)

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

def closeBrowser(driver):
    print("     -----------> Closing Browser")
    driver.close()

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
            questionNameList.append(questionName)
            questionUrlList.append(questionUrl)
            questionDifficultyList.append(questionDifficulty)
            # print(questionName, questionUrl, questionDifficulty)
        print("     -----------> Done")
        closeBrowser(browser)

    else:
        print("Page does not exist o connection Failed, status code: ",
              soup.status_code)
    return

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
            print(f"Total {questionNameList.__len__()} questions fetched")
            storeData()

        else:
            print("Connection Failed")
            return

    except Exception as e:
        print("Some error occured, error: ", e)
        return

getData()