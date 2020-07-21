from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

WAITTIME = 2
LONGWAITTIME= 5

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver', options=chrome_options)
act=ActionChains(driver)
wait= WebDriverWait(driver, 5)
driver.delete_all_cookies()
driver.get("https://twitter.com/search?q=AVENGER&src=typed_query")



def get_curr_url():
    return driver.current_url
def check_url(text):
    return True if text == get_curr_url() else False 

def is_element_exist(text,typeofelement):
    return True if len(get_elements_data(text,typeofelement)) > 0 else False

def get_elements_data(text,typeofelement):
    if str(typeofelement).lower() == "partial_link_text":
        elements = driver.find_elements_by_partial_link_text(text)
    elif str(typeofelement).lower() == 'class':
        elements = driver.find_elements_by_class_name(text) 
    elif str(typeofelement).lower() == 'id':
        elements = driver.find_elements_by_id(text) 
    elif str(typeofelement).lower() == 'xpath':
        elements = driver.find_elements_by_xpath(text) 
    else:
        raise Exception('INVALID ARRUGMENT')
    return elements

def get_element_data(text,typeofelement):
    if str(typeofelement).lower() == "partial_link_text":
        element = driver.find_element_by_partial_link_text(text)
    elif str(typeofelement).lower() == 'class':
        element = driver.find_element_by_class_name(text) 
    elif str(typeofelement).lower() == 'id':
        element = driver.find_element_by_id(text) 
    elif str(typeofelement).lower() == 'xpath':
        element = driver.find_element_by_xpath(text) 
    else:
        raise Exception('INVALID ARRUGMENT')
    return element
    
def press_button(role,data_testid):
    text= "//div[@role='{}' and @data-testid='{}']".format(role,data_testid)
    if is_element_exist(text,'xpath'): 
        get_element_data(text,'xpath').click()
    else:
        time.sleep(WAITTIME)
        press_button(role,data_testid)


def start(USERNAME, PASSWORD):
    if check_url("https://twitter.com/login") == False:
        print('Not on Login Page // Redirecting to Login Page')
        driver.get("https://twitter.com/login")
    print('SENDING DATA TO FIELDS')
    login('session[username_or_email]', 'text', USERNAME)
    login('session[password]', 'password', PASSWORD)
    press_button('button', 'LoginForm_Login_Button')
    if is_element_exist('The username and password you entered did not match our records.', "partial_link_text"):
        print("IVALID USERNAME AND PASSWORD")
        USERNAME= input('Enter Correct Username:')
        PASSWORD= input('Enter Correct Password:')
        start(USERNAME, PASSWORD)
    
def search(searchText, clear=False):
    text= '//input[@data-testid="SearchBox_Search_Input" and @placeholder="Search Twitter"]'
    if clear == True: 
        if is_element_exist(text,'xpath'): 
            get_element_data(text,'xpath').send_keys(Keys.CONTROL + 'a'+  Keys.BACKSPACE)
        else:
            time.sleep(WAITTIME)
            search(searchText, clear=True)    
    if is_element_exist(text,'xpath'): 
        get_element_data(text,'xpath').send_keys(searchText + Keys.ENTER)
    else:
        time.sleep(WAITTIME)
        search(searchText, clear=False)

def remove_elements_from_second_list(mainList, targetList):
    for x in targetList:
            if x in mainList:
                mainList.remove(x)
    return mainList

def login(name, typeText, data):
    text= "//input[@name='{}' and @type='{}']".format(name,typeText)
    if is_element_exist(text,'xpath'): 
        get_element_data(text,'xpath').send_keys(data)
    else:
        time.sleep(WAITTIME)
        login(name, typeText, data)

#TWEET EXISTS FUNCTIONALITY LEFT
def tweet(messageText, noOfTweets):
    print(messageText)
    replyTextPath = '//div[@role="button" and @data-testid="reply" and @data-focusable="true"]' 
    tweetTextPath = '//div[@aria-label="Tweet text" and @data-testid="tweetTextarea_0" and @role="textbox"]'
    height,i,doneList=0,0,[]
    while i < noOfTweets:
        time.sleep(WAITTIME)    
        reply= remove_elements_from_second_list(get_elements_data(replyTextPath,'xpath'), doneList)
        for j in range(len(reply)):
            try:
                reply[j].click()
                doneList.append(reply[j])
                time.sleep(WAITTIME)
                get_element_data(tweetTextPath,'xpath').send_keys(messageText + Keys.CONTROL + Keys.ENTER)
                break
            except Exception:
                continue
        time.sleep(WAITTIME)
        driver.execute_script(f"window.scrollTo({height}, {height+400})")
        height+=400
        i+=1

if __name__ == "__main__":
    try:
        #STARTED
        USERNAME= input("ENTER USERNAME:")
        PASSWORD= input("ENTER PASSWORD:")
        MESSAGE = input("ENTER MESSAGE:")
        KEYWORD = input("ENTER KEYWORD:")
        time.sleep(WAITTIME)
        start(USERNAME,PASSWORD)
        search(KEYWORD)
        tweet(MESSAGE,10)
    except NoSuchElementException as e:
        print(f'ERROR FOUND-> {e}')
    except Exception as e:
        print(f'ERROR FOUND-> {e}')