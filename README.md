# blackboard.bot
A Python bot that joins your online class on BlackBoard Collaborate Ultra.

_Bored of having to join your online class every time? 
Are you rarely asked a single question during the online lesson? 
Do you straight up don't give a shit about that class?_

_**Welp! Look no further, mi amigo! This Python bot/script is the perfect solution for your hurldes!**_

## Requirements
* Python3
* [Selenium Module](https://pypi.org/project/selenium/#description)
* [GeckoDriver](https://github.com/mozilla/geckodriver/releases/latest)\*
* Latest Mozilla Firefox

##### \* Add GeckoDriver to PATH on Windows/UNIX; See [here](https://stackoverflow.com/a/40208762).
## Important Note:

The script doesn't fully work in Presenter Mode. What is that you ask?

Presenter Mode is when your moderator decides to share a presentation with the class. When doing that he/she has the option to add the online participants as presenters. 

**Currently script works if the moderator doesn't add the whole class (including you) as presenters.**

Hopefully somebody can fix this cuz I cannot figure out what is going on.

## How-To Use

Open-up bot.py in a text editor and do the following:

* Edit the URL var with your BlackBoard Collaborate Ultra invite link.
* Edit the ```T_UNITL_LEAVE``` var to tell bot the maximum time it should stay in class. **Default is 1.64 hrs**
* Edit the ```LEAVE_IF_USERS_DECREASE_BY``` var to tell bot to exit class if at least so many ppl exit. **Default is 3.**
* Run.

## Use Cases

Running the script using a cronjob or a scheduled task every time you have class is the best use-case for this script. 

## Enjoy!
