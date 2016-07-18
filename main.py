# Personal Project - Goal is to make program that checks certain YouTube
# channels that you tell it to follow and downloads new YouTube videos from
# the channels. Also, I might look into a way of getting notifications on my
# phone for when a new video is downloaded to my computer.

# NOTE: I'm using the github project 'youtube-dl' to download the YouTube
# videos.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import os

YOUTUBE_LINK = 'https://www.youtube.com/'

channels = input('Please enter YouTube channels you\'d like to follow, each ' +
                 'separated by a comma.\nEx.(channel1, channel2, ect.): ').split(', ')
print(channels)
htmlFiles = []
for number, channel in enumerate(channels):
    try:
        htmlFiles.append(urlopen(YOUTUBE_LINK + channel + '/Videos'))
    except:
        print('An error occurred while attempting to open a YouTube link.')
        sys.exit(1)

    htmlFiles[number] = str(htmlFiles[number].read())

    # Don't need these lines when done. Temporarily using for viewing files.
    soup = BeautifulSoup(htmlFiles[number], 'html.parser')
    htmlFiles[number] = soup.prettify()
    fileName = 'htmlFile' + str(number) + '.html'
    with open(fileName, 'w') as f:
        f.write(htmlFiles[number])

# When using regex to find links in the html, use: 'h3 class="yt-lockup-title'

# Also, maybe lookup a way of integrating a terminal with Sublime

# os.system('youtube-dl -o "E:/Users/spart/Videos/YouTube Videos/%(title)s.%(ext)s" https://www.youtube.com/watch?v=r4ZrDSR81RE')
