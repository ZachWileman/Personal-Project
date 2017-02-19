# Personal Project - Goal is to make program that checks certain YouTube
# channels that you tell it to follow and downloads new YouTube videos from
# the channels. Also, I might look into a way of getting notifications on my
# phone for when a new video is downloaded to my computer.

# Program developed using Python 3.4.4

# NOTE: I'm using the github project 'youtube-dl' to download the YouTube
# videos. I do not endorse the downloading of YouTube videos. The program
# I have made was made purely for educational purposes.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, os, re, time, json
from smtplib import SMTP

# Global values
YOUTUBE_LINK = 'https://www.youtube.com/'
userInfo = {'toEmailAdd': None, 'fromEmailAdd': None, 'password': None}

# Used for when importing JSON file
noFileFound = False 
noUserInfoFound = False

# Class used for saving info for each YouTube channel
class Channel:

    # Sets the channel name
    def __init__(self, channelName):
        self.latestVideo = ""
        self.name = channelName

    # checks if the video is new
    def checkVideo(self, videoTitle):
        if videoTitle != self.latestVideo:
            print('New video found!')
            self.latestVideo = videoTitle
            return True
        else:
            return False 



# Gets user input for channels
# NOTE: With newer channels, usernames no longer work so instead you'll have
# to enter part of the url of the channel such as: 'channel/' followed by the
# channel id
channels = input('Please enter YouTube channels you\'d like to follow, each ' +
                 'separated by a comma.\nEx.(channel1, channel2, ect.): \n').split(', ')
print('') # Adds new line

# Checks for empty list
if '' not in channels:
    # Creates a list of Channel objects
    channelList = [Channel(channel) for channel in channels]
else:
    channelList = []

# Gets user choice for importing previous channel info
importChoice = input('Would you like to import past channel/user info from previous program runs? (yes or no): \n' +
                     'WARNING: Selecting no will cause old information to be overwritten by new information if any is entered\n')
print('') # Adds new line

# If the user chooses to import
if importChoice == 'yes' or importChoice == 'y':
    
    # Tries to import the JSON file 
    try:

        # Loads in the JSON file and adds the info to channelList if the
        # channel isn't already in the list.
        with open('data.json', 'r') as f:
            jsonList = json.load(f)

        # Checks in case the JSON file contains an empty dictionary
        if jsonList:
            
            # Checks for channel info
            if 'channels' in jsonList:
                for channel in jsonList['channels']:
                    temp = Channel(channel['channelName'])
                    temp.latestVideo = channel['latestVideo']
                    if channel['channelName'] not in channels:
                        channelList.append(temp)

            # Checks for user email info
            if 'user' in jsonList:
                userInfo['fromEmailAdd'] = jsonList['user']['fromEmailAdd']
                userInfo['toEmailAdd'] = jsonList['user']['toEmailAdd']
                userInfo['password'] = jsonList['user']['password']
            else:
                noUserInfoFound = True
        else:
            print('No data found in file to import\n')
    
    # If there is no JSON file to import, reports so and then continues
    except FileNotFoundError as e:
        print('No file found to import data from\n')
        noFileFound = True

# If no data has been imported
if noFileFound or noUserInfoFound or (importChoice != 'yes' and importChoice != 'y'):

    # Gets email from user for sending notifications
    userInfo['fromEmailAdd'] = input('Please enter the email you would like to send emails from: ' +
                                   '(Leave blank if you don\'t want notifications)\n')
    print('') # Adds new line

    # Gets passsword (for sending emails) if email is entered
    if userInfo['fromEmailAdd']:
        userInfo['password'] = input('Please enter the password for your (sending) email address: ' +
                                     '(Your password and email will only be stored in a local JSON file)\n')
        print('') # Adds new line

        # Gets email from user for recieving notifications
        userInfo['toEmailAdd'] = input('Please enter the email you would like to receive notifications at: ' +
                                       '(Leave blank if you don\'t want notifications)\n')
        print('') # Adds new line

        with open('data.json', 'w') as f:
            json.dump({"user": {"toEmailAdd": userInfo['toEmailAdd'], "fromEmailAdd": userInfo['fromEmailAdd'], "password": userInfo['password']}}, f, indent=4)

# In case a file has/hasn't been created
try:
    # Opens JSON file and adds new channel info
    with open('data.json', 'r') as f:
        newData = json.load(f)
        newData['channels'] = [{"channelName": channel.name, "latestVideo": channel.latestVideo} for channel in channelList]
except:
    newData = {}

# Writes the new JSON data to the file
with open('data.json', 'w') as f:
    json.dump(newData, f, indent=4)

if not channelList:
    print('No channels were entered or imported from the JSON file.\nExiting program.')
    sys.exit(1)

# Loops every five minutes, checking for new videos from the given channels
while True:
    for channel in channelList:
        try:
            htmlFile = urlopen(YOUTUBE_LINK + channel.name + '/Videos')
        except:
            print('An error occurred while attempting to open a YouTube link.')
            sys.exit(1)

        # Cleans up the html file
        htmlFile = str(htmlFile.read())
        soup = BeautifulSoup(htmlFile, 'html.parser')
        htmlFile = soup.prettify()

        # Search through the html file for a match with the regular expression
        regExp = re.compile('<h3\sclass=\"yt-lockup-title\s\">\n.*href=\"/(.*)\"\stitle=\"(.*)\">')
        match = regExp.search(htmlFile)
        urlLink = match.group(1)
        videoFound = match.group(2)

        # If a match was successfully found
        if match:

            # Checks if a new video has been found. If so, reports so and
            # downloads the video
            if channel.latestVideo != videoFound:
                print('New video found: ', videoFound)
                downloadString = 'youtube-dl -o "E:/Users/spart/Videos/YouTube Videos/%(title)s.%(ext)s" ' + YOUTUBE_LINK + urlLink
                channel.latestVideo = videoFound
                os.system(downloadString)

                # Sends the user an email notification about the new video downloaded
                # (Assuming the user added an email)
                if userInfo['fromEmailAdd']:
                    fromAdd = username = userInfo['fromEmailAdd']
                    toAdd = userInfo['toEmailAdd']
                    password = userInfo['password']
                    msg = ('Subject: New YouTube Video!\r\n' +
                           'You\'ve got a new video downloaded from {} titled:\n{}'.format(channel.name, channel.latestVideo))
                    
                    server = SMTP('smtp.gmail.com:587')
                    server.ehlo()
                    server.starttls()

                    # Attempts to login and send email
                    try:
                        server.login(username, password)
                        server.sendmail(fromAdd, toAdd, msg)
                    except Exception as e:
                        print("You have entered an invalid email or password")
                        print(e)

                    server.quit()
            
            # Otherwise, reports nothing new found.
            else:
                print('Nothing new found.')

        # If unable to find a regular expression match, reports so.
        else:
            print('Unable to find a match within the HTML file.')

    # Updates JSON file with new 'lastest video' info for each channel
    with open('data.json', 'r') as f:
        newData = json.load(f)
        newData['channels'] = [{"channelName": channel.name, "latestVideo": channel.latestVideo} for channel in channelList]

    with open('data.json', 'w') as f:
        json.dump(newData, f, indent=4)

    # Has the program check every 5 minutes for new videos
    print('Waiting for 5 minutes to check for any new videos...\n')
    time.sleep(5*60)


############################# Also, possibly add something for entering new channels while the
############################# program is running?
