from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import sys

## Variables
URL = "<Add BB URL here>" 
PSEUDONAME = "Mike Pence"
ERR_STRINGS =["Loading failed. Exiting...","Joining Session Failed. Exiting...","Loading of Audio Test Page failed. Exiting...","Audio Test failed. Exiting...","Something went wrong while Cleaning Screen. Exiting...","Camera Test Failed. Exiting..."]
T_UNTIL_LEAVE = 5900
LEAVE_IF_USERS_DECREASE_BY = 3
WARNINGS = []

## Functions

## 1. Configure Firefox Preferences
def new_foxfire():
    p = webdriver.FirefoxProfile()
    p.set_preference("permissions.default.microphone", 1) #Allow mic access
    p.set_preference("permissions.default.camera", 1) # Allow cam access
    p.update_preferences()
    return p
## 2. Configure Headless Mode
def new_foxfire_options():
    n = Options()
    n.headless = False
    return n
## 3. Safely Check if an element is visible
def waitforexec(arg1, arg2, arg3=30,arg4=False):
    try:
        found = WebDriverWait(browser, arg3).until(EC.visibility_of_element_located((By.XPATH,arg1)))
        if (arg4 == True):
            return found;
    except TimeoutException:
        term(arg2)
## 4. Terminate Script w Reason.
def term(reason):
    browser.quit()
    sys.exit(reason)

def warn_user(text): # Reduce terminal spam.
    s = len(WARNINGS)
    if (s ==0):
        WARNINGS.append(text)
        print(WARNINGS[0])
    elif(WARNINGS[s-1] != text):
        WARNINGS.append(text)
        print(WARNINGS[len(WARNINGS)-1])
## 5. Clean up BB UI

def cleanupUI():
    a = waitforexec("//button[@analytics-id='announcement.introduction.later']",ERR_STRINGS[5],30,True)
    time.sleep(5)
    a.click()
    b = waitforexec("//button[@analytics-id='tutorial.finish']","Tutorial Finish Btn not found.",30,True)
    time.sleep(5)
    b.click()
    try:
        side = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH,"//button[@id='side-panel-open']")))
        time.sleep(5)
        side.click()
    except:
        term("Sidepanel btn couldn't be selected.")
    c = waitforexec("//li[@id='panel-control-participants']","Could find participants tab.",30,True)
    time.sleep(5)
    c.click()
    print("Cleared up UI.")


## 6. Alternative way to bypass Audiocheck
def backup_way():
    try:
        yesaudio = browser.find_element_by_xpath("//button[@analytics-id='techcheck.audio.ok-button']")
        time.sleep(3)
        yesaudio.click()
        print("OK.")
    except NoSuchElementException:
        term(ERR_STRINGS[3]);

## 7. Count number of people in class.
# FLAWED when moderator adds your bot as a presenter too. No idea why.
def count_users():
    listofp = False
    presenter = False
    presenters_num =0
    participants_num =0
    try:
        listofp = browser.find_element_by_xpath("//ul[@class='participant-roster']") # Find unordered list containing participants.
    except NoSuchElementException:
        warn_user("Couldn't find participants.")
        warn_user("Checking for Presenter mode instead..")
    try:
        presenter = browser.find_element_by_xpath("//ul[@class='presenter-roster']") # Find unordered list containing presenters.
        warn_user("Presenter Mode is ON.")
    except NoSuchElementException:
            warn_user("Presenter Mode is OFF.")
    if(listofp == False and presenter ==False):
        term("Participants or Presenters were not found. Exiting...")
    if (presenter != False):
        in_li_p = presenter.find_elements_by_xpath("//li[contains(@class, 'participant-list-item')]")
        presenters_num = len(in_li_p) # Count every presenter
    if (listofp != False):
        in_li_p = listofp.find_elements_by_xpath("//li[contains(@class, 'participant-list-item')]")
        participants_num = len(in_li_p) # Count every participant
    total_number = presenters_num + participants_num
    return total_number

## 8. Check if people have left the session.
def check_decrease():
    initial_num = count_users()
    print("Waiting for "+str(T_UNTIL_LEAVE)+"s")
    print("OR for at least "+str(LEAVE_IF_USERS_DECREASE_BY)+" people to leave.")
    while(time.time() < time.time()+T_UNTIL_LEAVE):
        time.sleep(5)
        new_num = count_users()
        if(initial_num < new_num):
            #Somebody has joined.
            initial_num = new_num
        if (initial_num-new_num >= LEAVE_IF_USERS_DECREASE_BY):
            #People have left the session.
            break;
    term("Class Time finished!")

#Launch GeckoDriver with custom prefs.
print("Launching Firefox...")
browser = webdriver.Firefox(options=new_foxfire_options(), firefox_profile=new_foxfire())

print("Loading BlackBoard Join Page...")
browser.get(URL)
join_button = 0
try:
    join_button = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.ID,"launch-html-guest"))) #Explicit wait 30s until join button pops up.
    print("Join button Found!")
except TimeoutException:
    term(ERR_STRINGS[0])

if (join_button ==0): # I don't think this is needed but gon leave it in.
    browser.quit()
    exit(1)

# Join online class as <PSEUDONAME>   
inputfield = browser.find_element_by_id("guest-name")
inputfield.send_keys(PSEUDONAME)
time.sleep(3)

join_button.click();
print("Clicked Join button.")

waitforexec("//p[@analytics-id='session.connection-status.user-joining-session']",ERR_STRINGS[1])
waitforexec("//span[@analytics-id='techcheck.audio.header']",ERR_STRINGS[2])

print("Bypassing Mic Check...")
time.sleep(10)
try:
    skip_audio = browser.find_element_by_xpath("//button[@analytics-id='techcheck.audio.skip-audio']")
    skip_audio.click()
    print("OK.")

except NoSuchElementException:
    backup_way()


waitforexec("//span[@analytics-id='techcheck.video.fullcheck-mode.header']",ERR_STRINGS[2])
    
print("Bypassing Camera check...")
time.sleep(8)
try:
    yescam = browser.find_element_by_xpath("//button[@analytics-id='techcheck.video.fullcheck-mode.ok-button']")
    yescam.click()
    print("OK.")
except NoSuchElementException:
    term(ERR_STRINGS[6])

print("Finishing Join...")
waitforexec("//h2[@analytics-id='announcement.introduction.title']", ERR_STRINGS[1],50)
print("You have joined the class!")

cleanupUI()
check_decrease()
