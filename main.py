# Personal Project - Goal is to make program that checks certain YouTube
# channels that you tell it to follow and downloads new YouTube videos from
# the channels. Also, I might look into a way of getting notifications on my
# phone for when a new video is downloaded to my computer.

# Program developed using Python 3.4.4

# NOTE: I'm using the github project 'youtube-dl' to download the YouTube
# videos.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, os, re, time, json

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

YOUTUBE_LINK = 'https://www.youtube.com/'

# Gets user input for channels
# NOTE: With newer channels, usernames no longer work so instead you'll have
# to enter part of the url of the channel such as: 'channel/' followed by the
# channel id
channels = input('Please enter YouTube channels you\'d like to follow, each ' +
                 'separated by a comma.\nEx.(channel1, channel2, ect.): ').split(', ')

# Creates a list of Channel objects
channelList = [Channel(channel) for channel in channels]

# Gets user choice for importing previous channel info
importChoice = input('Would you like to import past channel info from' +
                     ' previous program runs? (yes or no): ')

# If the user chooses to import
if importChoice == 'yes':
    
    # Tries to import the JSON file 
    try:

        # Loads in the JSON file and adds the info to channelList if the
        # channel isn't already in the list.
        with open('youtubeData.json', 'r') as f:
            jsonList = json.load(f)
        for channel in jsonList:
            temp = Channel(channel['channelName'])
            temp.latestVideo = channel['latestVideo']
            if channel['channelName'] not in channels:
                channelList.append(temp)
    
    # If there is no JSON file to import, reports so and then continues
    except FileNotFoundError as e:
        print('No file found to import data from.')

# Make a json list out of channelList to then put in a json file
jsonList = [{"channelName": channel.name, "latestVideo": channel.latestVideo} for channel in channelList]
with open('youtubeData.json', 'w') as f:
    json.dump(jsonList, f)

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
            
            # Otherwise, reports nothing new found.
            else:
                print('Nothing new found.')

        # If unable to find a regular expression match, reports so.
        else:
            print('Unable to find a match within the HTML file.')

    # Has the program check every 5 minutes for new videos
    time.sleep(5*60)