import selenium; import time; import langdetect; import googletrans; import fuzzywuzzy; import random; import os
from fuzzywuzzy  import fuzz
from googletrans import Translator
from langdetect  import detect
from selenium    import webdriver
from langdetect  import DetectorFactory ; DetectorFactory.seed = 0
from selenium.webdriver.common.keys import Keys
#===========================================================================================================================================
def cookie():
    try:
        if (driver.find_element_by_class_name('cc-btn')):
            driver.find_element_by_class_name('cc-btn').click()
    except: pass
#===========================================================================================================================================
def mute():
    try:
        if (driver.find_element_by_id('mute-audio')):
            driver.find_element_by_id('mute-audio').click()
    except: pass
#===========================================================================================================================================
def logIn(username, password):
    user_box = driver.find_element_by_name('username'); user_box.send_keys(username)
    pass_box = driver.find_element_by_name('password'); pass_box.send_keys(password)
    login_button = driver.find_elements_by_class_name('btn')[2]; login_button.click()
#===========================================================================================================================================
def next():
    next_button = driver.find_element_by_class_name('btn')
    next_button.click()
#===========================================================================================================================================
def translate(prompt):
    translator = Translator()
    try: #dictionary method
        if (prompt in phrasesF2E):
            translatedprompt = phrasesF2E[prompt]
            return translatedprompt
        if (prompt in phrasesE2F):
            translatedprompt = phrasesE2F[prompt]
            return translatedprompt
    except: pass
    try: #google translate method
        if (detect(prompt) == 'en'):
            translatedprompt = translator.translate(prompt, dest='fr').text
            return translatedprompt
        if (detect(prompt) == 'fr'):
            translatedprompt = translator.translate(prompt, dest='en').text
            return translatedprompt
    except: pass
#===========================================================================================================================================
def main():
    while(True): 
        time.sleep(random.uniform(1, 3)) #makes it not sus
        #end================================================================================================================================
        try: 
            if(driver.find_element_by_class_name('end_of_session')): break
        except: pass
        try: 
            if(driver.find_element_by_class_name('continue-btn')): 
                time.sleep(1)
                try:
                    driver.find_element_by_class_name('continue-btn').click()
                except: pass
        except: pass
        #definitions========================================================================================================================
        try:
            if(driver.find_element_by_class_name('primary-value')): 
                content = driver.find_elements_by_class_name('primary-value')
                for i in range(len(content)): content[i] = content[i].text
                phrasesF2E[content[0]] = content[1]
                phrasesE2F[content[1]] = content[0]
                with open(path+'\\assets\\translationsF2E.txt', 'w') as translationsF2E:
                    translationsF2E.write(str(phrasesF2E))
                with open(path+'\\assets\\translationsE2F.txt', 'w') as translationsE2F:
                    translationsE2F.write(str(phrasesE2F))
                next()
                continue
        except: pass
        #typing questions===================================================================================================================
        try:
            if(driver.find_element_by_class_name('typing')):
                prompt = driver.find_element_by_id('prompt-row').text
                translatedPrompt = translate(prompt)
                driver.find_element_by_css_selector('input').send_keys(translatedPrompt)
                next()
                continue
        except: pass
        #multiple choice questions==========================================================================================================
        try:
            if(driver.find_element_by_class_name('multiple_choice')):
                prompt = driver.find_element_by_id('prompt-row').text
                translatedPrompt = translate(prompt)
                content = driver.find_elements_by_class_name('val')
                for i in range(len(content)): 
                    content[i] = content[i].text
                    if (fuzz.ratio(content[i], translatedPrompt) > 90):
                        driver.find_element_by_css_selector('body').send_keys(i+1)
                        break
                driver.find_element_by_css_selector('body').send_keys(1) #learning the answer if cant find   
                continue
        except: pass
        #tapping questions==================================================================================================================
        try:
            if(driver.find_element_by_class_name('tapping')): 
                prompt = driver.find_element_by_id('prompt-row').text
                translatedPrompt = translate(prompt).split()    
                for i in range(len(translatedPrompt)):
                    if (',' in translatedPrompt[i] and len(translatedPrompt[i]) > 1): 
                        translatedPrompt[i] = translatedPrompt[i].split()[0] ; translatedPrompt.insert(i+1, ',')
                    if ('?' in translatedPrompt[i] and len(translatedPrompt[i]) > 1): 
                        translatedPrompt[i] = translatedPrompt[i].split()[0] ; translatedPrompt.insert(i+1, '?')
                    if ('/' in translatedPrompt[i] and len(translatedPrompt[i]) > 1): 
                        translatedPrompt[i] = translatedPrompt[i].split()[0] ; translatedPrompt.insert(i+1, '/')
                content = (driver.find_element_by_class_name('word-box-choice').text).split()
                for i in range(len(translatedPrompt)):
                    for x in range(len(content)):
                        if (fuzz.ratio(content[x], translatedPrompt[i]) > 90): 
                            driver.find_elements_by_class_name('word')[x+i].click()
                next()
                continue
        except: 
            try: next()
            except: pass
        #===================================================================================================================================
        print('no prompt found and no question found')
#===========================================================================================================================================
if __name__ == '__main__':
    username = str(input('username >> '))
    password = str(input('password >> '))
    website = str(input('link >> '))
    print(username, password, website)
    for i in range(100):
        path = os.getcwd()
        dir = os.path.dirname(__file__)
        chrome_path = os.path.join(dir, 'selenium','webdriver','chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        #getting the webdriver component and opening the website----------------------------------------------------------------------------
        driver = webdriver.Chrome(options=options)
        driver.get(website)
        #initializing dictionaries for the correct translations-----------------------------------------------------------------------------
        translationsF2E = open(path+'\\assets\\translationsF2E.txt', 'r+')
        translationsE2F = open(path+'\\assets\\translationsE2F.txt', 'r+')
        phrasesF2E = eval(translationsF2E.read())
        phrasesE2F = eval(translationsE2F.read())
        translationsF2E.close()
        translationsE2F.close()
        #logging in-------------------------------------------------------------------------------------------------------------------------
        cookie()
        logIn(username, password)
        mute()
        main()
        driver.quit()