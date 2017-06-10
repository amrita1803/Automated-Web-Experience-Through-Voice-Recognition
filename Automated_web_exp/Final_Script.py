#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

 
#--------------------------------------Importing the necessary modules---------------------------------    
import speech_recognition as sr
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import subprocess
import os
import pyttsx
import feedparser
import sys

#-------------------------------Function to convert text to speech---------------------------------------
def text_converter(text):
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate-50)
    # changes the voice
    engine.say(text)
    engine.runAndWait()



#------------------------------Function Remove a specific value from a list---------------------------------------
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

#----------------------------------Function For News Feed------------------------------------------------------------

# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines( rss_url ):
    headlines = []
    
    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    
    return headlines


#----------------------------------Function To Exit Multiple web page------------------------------------------------
def exit_multipleweb():
    os.system("taskkill /f /im  MicrosoftEdge.exe")
    
#-------------------------------Function to Open multiple websites----------------------------------------------------
def open_multiple():
    print("Waiting for input of multiple websites")
    text_converter('Waiting for input of multiple websites')
    websites = []
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio1 = r.listen(source)
        try:    
            result = r.recognize_google(audio1).lower()
            websites = result.split()
            if '.com' in result or '.org' in result or '.edu' in result or '.net' in result or '.gov' in result or '.in' in result and 'open' in result:
                websites = remove_values_from_list(websites, 'open')
                for website in websites:
                    print('Opening ' + website)
                    text_converter('opening ' + website)
                    webbrowser.open_new('https://www.'+ website)
                open_multiple()
            elif 'exit' in result and 'browser' in result:
                print('Microsoft Edge will is now close')
                text_converter('Microsoft Edge will is now close')
                exit_multipleweb()
                record()
            elif 'exit' in result and 'application' in result:
                print('Ending Application')
                text_converter('Ending Application')
                print('Closed Successfully')
                text_converter('Closed Successfully')
                exit
            elif '.com' in result or '.org' in result or '.edu' in result or '.net' in result or '.gov' in result or '.in' in result:
                for website in websites:
                    print('Opening ' + website)
                    text_converter('Opening ' + website)
                    webbrowser.open_new('https://www.'+ website)
                open_multiple()
            else:
                print('\''+result+'\''+' is an invalid input')
                text_converter(result + ' is an invalid input')
                print('Kindly, Retry.')
                text_converter('Kindly, Retry.')
                open_multiple()    
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            text_converter('Sorry, dint quite get that')
            open_multiple()
        except sr.RequestError as e:
            print("Could not request results due to network issue; {0}".format(e))
            text_converter('There seems to be an issue with the network')
            open_multiple()


#-------------------------------Function to Open a particular website--------------------------------------------------
def open_website(website):
        global driver
        driver = webdriver.Edge('C:\Python27\Scripts\MicrosoftWebDriver.exe')
        driver.wait = WebDriverWait(driver, 5)
        #return driver
        driver.get('https://www.'+website)
        
#--------------------------------Function To Exit Web Driver-------------------------------------------------------------
def exit_web():
    print('Microsoft Edge will is now close')
    driver.quit()
        
#-----------------------------Function used for voice recognition--------------------------------------------------------
def record():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for input")
        text_converter('Waiting for input')
        audio = r.listen(source)      
    # Speech recognition using Google Speech Recognition
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    #print("You said: " + r.recognize_google(audio))
        #tld = ['open','.com','.co.in','.org','.edu','.net','.gov','.in']
        result = r.recognize_google(audio).lower()
        #print(result)
        if 'exit' in result and 'browser' in result:
            print('Closing Browser')
            text_converter('Closing Browser')
            exit_multipleweb()
            #exit_web()
            record()
        elif 'close' in result and 'application' in result:
            print('Closing Application')
            text_converter('Closing Application')
            print('Closed Successfully')
            text_converter('Closed Successfully')
            sys.exit()    
        elif 'open' in result and 'multiple' in result:
            open_multiple()
        elif '.com' in result or '.org' in result or '.edu' in result or '.net' in result or '.gov' in result or '.in' in result and 'open' in result:
            strippedresult = result.replace("open","")
            finalresult = strippedresult.replace(" ","")
            print('opening ' + finalresult)
            text_converter('opening ' + finalresult)
            open_website(finalresult)
            record()
        elif '.com' in result or '.org' in result or '.edu' in result or '.net' in result or '.gov' in result or '.in' in result:
            finalresult = result.replace(" ","")
            print('Opening ' + finalresult)
            text_converter('Opening ' + finalresult)
            open_website(finalresult)
            record()
        elif 'top' in result and 'news' in result:
            print('Getting Todays Top News')
            text_converter('Getting Todays Top News')
            # A list to hold all headlines
            allheadlines = []

            # List of RSS feeds that we will fetch and combine
            newsurls = {
                'apnews':           'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909',
                'googlenews':       'http://news.google.com/?output=rss',
                'yahoonews':        'http://news.yahoo.com/rss/'
                        }

            # Iterate over the feed urls
            for key,url in newsurls.items():
            # Call getHeadlines() and combine the returned headlines with allheadlines
                allheadlines.extend( getHeadlines( url ) )


            # Iterate over the allheadlines list and print each headline
            count = 0
            for hl in allheadlines:
                count = count + 1
                if count <=5:
                    print(hl)
                    text_converter(hl)
                else:
                    print('Those were the top news from around the world.')
                    text_converter('Those were the top news from around the world.')
                    record()
        elif 'search' in result:
            result1 = result.replace('search', '')
            ur="https://www.google.co.in/search?q="
            webbrowser.open_new(ur+str(result1))
            print('Searching')
            text_converter('Searching')
            record()
        else:
            print('\''+result+'\''+' is an invalid input')
            text_converter(result +' is an invalid input')
            print('Kindly, Retry.')
            text_converter('Kindly, Retry.')
            record()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
        text_converter('Sorry, dint quite get that')
        record()
    except sr.RequestError as e:
        print("Could not request results due to network issue; {0}".format(e))
        text_converter('There seems to be an issue with the network')
        record()
        

#---------------------------------Code to verify input and display the result----------------------------------------------------
print('Automated Web experience through voice recognition')
text_converter('Automated Web experience through voice recognition.')
print('Application will now attempt to recognise speech')
text_converter('Application will now attempt to recognise speech.')
record()
        
