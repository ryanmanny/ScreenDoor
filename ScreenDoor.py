from urlparse import urljoin
from bs4 import BeautifulSoup
import requests

# Upon further reflection I think this program is too slow to ever be useful
# I will need to research song lyric APIs instead of waiting for pages to load
# Parallelization is also promising, check out:
# http://www.gregreda.com/2016/10/16/asynchronous-scraping-with-python/

BASE_URL = "http://songmeanings.com"

DAVIDBYRNE = "http://songmeanings.com/artist/view/songs/11962/"
GARTHBROOKS = "http://songmeanings.com/artist/view/songs/91/"
TAYLORSWIFT = "http://songmeanings.com/artist/view/songs/137438973836/"
TOBYKEITH = "http://songmeanings.com/artist/view/songs/7776/"

def get_song(link):
    """Return lyrics and title of song found at link"""
    # Opens page and soups it
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    req.close()

    # Grabs song title from the page
    title = soup.find("title").text.strip()
    title = title[:title.find("|")]

    # Grabs lyrics from the page
    lyrics = soup.find("div", class_="holder lyric-box").text.strip()
    lyrics = lyrics[:lyrics.find("Edit")]

    # This should probably be a dictionary, not a list... I'll figure that out eventually
    return [title, lyrics]


def screen_door(link):
    """Returns the number of instances of the string 'screen door' in an artist's discography"""
    # Opens page given by link and soups it
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    req.close()

    # Counts instances of screen doors
    count = 0
    total_count = 0

    num_songs = 0

    link_list = list()

    # Finds all song links on the page
    for link in soup.select("td > a"):
        link = urljoin(BASE_URL, link['href'])
        if link not in link_list:
            link_list.append(link)

    # Opens all links and gets the song info
    for song_link in link_list:
        song = get_song(song_link)

        num_songs += 1
        print str(num_songs) + " of " + str(len(link_list)) + " lyrics loaded, " + song[0]

        count = count_instances(song[1])
        if count > 0:
            print "Found " + str(count) + " instances of screen door in " + song[0]
            total_count += count

    return total_count

def count_instances(lyrics):
    """Counts instances of the word "screendoor" or "screen door" in a song lyric
       Accepts lyrics as a single string"""

    count = 0
    screen = False

    # Splits lyrics into a list of words
    lyrics = lyrics.split()

    # Increments count every time screen door is encountered
    for word in lyrics:
        # print word
        word = word.lower()
        
        if word == "screen":
            screen = True
        elif word == "door" and screen is True:
            count += 1
            screen = False
        else:
            screen = False

    return count

def get_link(artist_name):
    """Return an artist's songmeanings.com link from their name"""
    #I don't know what to do here

# lyrics = get_song("http://songmeanings.com/songs/view/3530822107858634184/")[1]
# print count_screen_door(lyrics)

num = screen_door(TOBYKEITH)
print str(num) + " instances of screen door found"
