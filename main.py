# Personal Project - Goal is to make program that checks certain YouTube
# channels that you tell it to follow and downloads new YouTube videos from
# the channels. Also, I might look into a way of getting notifications on my
# phone for when a new video is downloaded to my computer.

# Program developed using Python 3.4.4

# NOTE: I'm using the github project 'youtube-dl' to download the YouTube
# videos.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, os, re, time

# Class used for saving info for each YouTube channel
class Channel:
    def __init__(self, channelName):
        self.latestVideo = ""
        self.name = channelName
    def checkVideo(self, videoTitle):
        if videoTitle != self.latestVideo:
            print('New video found!')
            self.latestVideo = videoTitle
            return True
        else:
            return False 

YOUTUBE_LINK = 'https://www.youtube.com/'

# Gets user input for channels
channels = input('Please enter YouTube channels you\'d like to follow, each ' +
                 'separated by a comma.\nEx.(channel1, channel2, ect.): ').split(', ')

# Creates a list of Channel objects
channelList = [Channel(channel) for channel in channels]

############### Also, look into saving latest video information to some sort of log file, maybe json?

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

        # Don't need these lines when done. Temporarily using for viewing files.
        #fileName = 'htmlFile' + str(number) + '.html'
        #with open(fileName, 'w') as f:
        #    f.write(htmlFiles[number])

# When using regex to find links in the html, use: 'h3 class="yt-lockup-title'
# <h3 class="yt-lockup-title ">\n.*
# <h3\sclass=\"yt-lockup-title\s\"

# os.system('youtube-dl -o "E:/Users/spart/Videos/YouTube Videos/%(title)s.%(ext)s" https://www.youtube.com/watch?v=r4ZrDSR81RE')
