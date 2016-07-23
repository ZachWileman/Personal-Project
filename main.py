# Personal Project - Goal is to make program that checks certain YouTube
# channels that you tell it to follow and downloads new YouTube videos from
# the channels. Also, I might look into a way of getting notifications on my
# phone for when a new video is downloaded to my computer.

# Program developed using Python 3.4.4

# NOTE: I'm using the github project 'youtube-dl' to download the YouTube
# videos.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, os, re

class Channel:
    def __init__(self):
        self.latestVideo = ""
    def checkVideo(self, videoTitle):
        if videoTitle != self.latestVideo:
            print('New video found!')
            self.latestVideo = videoTitle
            return True
        else:
            return False 

YOUTUBE_LINK = 'https://www.youtube.com/'

channels = input('Please enter YouTube channels you\'d like to follow, each ' +
                 'separated by a comma.\nEx.(channel1, channel2, ect.): ').split(', ')
print(channels)
htmlFiles = []

# This is the portion I want to repat every five minutes; checking for new videos
# Also, look into saving latest video information to some sort of log file, maybe json?
for number, channel in enumerate(channels):
    try:
        htmlFiles.append(urlopen(YOUTUBE_LINK + channel + '/Videos'))
    except:
        print('An error occurred while attempting to open a YouTube link.')
        sys.exit(1)

    htmlFiles[number] = str(htmlFiles[number].read())

    soup = BeautifulSoup(htmlFiles[number], 'html.parser')
    htmlFiles[number] = soup.prettify()
    regExp = re.compile('<h3\sclass=\"yt-lockup-title\s\">\n.*href=\"/(.*)\"\stitle=\"(.*)\">')
    match = regExp.search(str(htmlFiles[0]))
    if match:

        print('New video found: ', match.group(2))
        downloadString = 'youtube-dl -o "E:/Users/spart/Videos/YouTube Videos/%(title)s.%(ext)s" ' + YOUTUBE_LINK + match.group(1)
        print(downloadString)
        os.system(downloadString)
    else:
        print('Unable to find a match within the HTML file.')

    # Don't need these lines when done. Temporarily using for viewing files.
    fileName = 'htmlFile' + str(number) + '.html'
    with open(fileName, 'w') as f:
        f.write(htmlFiles[number])

# When using regex to find links in the html, use: 'h3 class="yt-lockup-title'
# <h3 class="yt-lockup-title ">\n.*
# <h3\sclass=\"yt-lockup-title\s\"

# os.system('youtube-dl -o "E:/Users/spart/Videos/YouTube Videos/%(title)s.%(ext)s" https://www.youtube.com/watch?v=r4ZrDSR81RE')
