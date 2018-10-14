
import argparse
import time
import webbrowser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import urllib.request, json
import sys

DEVELOPER_KEY = 'lol'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
      q=options.q,
      part='id,snippet',
      maxResults=options.max_results,
      type='video'
      ).execute()

    video_id = search_response['items'][0]['id']['videoId']

    return video_id

site = 'https://osu.ppy.sh/api/'
config = json.loads(open('config.json').read())
key = config["APIKey"]
user = 'Naranja%20Sagged'
timeThreshold = 1
bpsThreshold = 1.0

#lol u gay
def getBeatmapInfo(beatmapID, key):
    apiSite = site + "get_beatmaps?b=" + beatmapID + '&k=' + key
    web_stuff = urllib.request.urlopen(apiSite)
    jason = json.loads(web_stuff.read().decode())
    return jason

def getUserRecent(userName, key):
    apiSite = site + "get_user_recent?u=" + userName + '&k=' + key
    web_stuff = urllib.request.urlopen(apiSite)
    jason = json.loads(web_stuff.read().decode())
    return jason

def getUser(userName, key):
    apiSite = site + "get_user?u=" + userName + '&k=' + key
    web_stuff = urllib.request.urlopen(apiSite)
    jason = json.loads(web_stuff.read().decode())
    return jason

def breakTime(recentSecondsPlayed, beatmapJason):
    print("YES")
    avgbps = 0
    for x in range(0, numMaps):
        jasonBeat = getBeatmapInfo(beatmapJason[x]['beatmap_id'], key)
        avgbps = avgbps + int(jasonBeat[0]['bpm'])
    avgbps = avgbps/recentSecondsPlayed
    if avgbps > bpsThreshold:
        f = open("remind.txt", "w+")
        f.write("OSU HEALTH REMINDER:\nYou have reached your designated Time and BPM thresholds.\n" \
            + "Now would be a great time to consider taking a break and stretching.\nAre you in pain? Y\\N\n"
            + "Trick question. You ARE in pain.")
        print("OSU HEALTH REMINDER:\nYou have reached your designated Time and BPM thresholds.\n" \
            + "Now would be a great time to consider taking a break and stretching.\nAre you in pain? Y\\N\n"
            + "Trick question. You ARE in pain.")
        parser = argparse.ArgumentParser()
        search_query = str(input('Where do you feel pain?\n')) + ' esports stretches'
        parser.add_argument('--q', help='Search term', default=search_query)
        parser.add_argument('--max-results', help='Max + arg.parse(addargument()) results', default=1)
        args = parser.parse_args()
        video_id = youtube_search(args)
        url = 'https://www.youtube.com/watch?v=' + str(video_id)
        webbrowser.open(url)
        time.sleep(1)
        f.close()
        discordBot(1)
        discordBot(0)
        return True
    else:
        discordBot(0)
        return False

def discordBot(trigger):
    if trigger == 1:
        print(1)
        sys.stdout.flush()
        return 1
    else:
        print(0)
        sys.stdout.flush()
        return 0


if __name__ == '__main__':

    jasonUser = getUser(user, key)
    jasonRecent = getUserRecent(user, key)
    totalSecondsPlayed = int(jasonUser[0]['total_seconds_played'])
    numMaps = 0
    while(1):
        lastTimePlayed = jasonRecent[0]['date']
        time.sleep(10)
        jasonRecent = getUserRecent(user, key)
        jasonUser = getUser(user, key)
        if lastTimePlayed != jasonRecent[0]['date']:
            print('im gay')
            numMaps += 1
            if totalSecondsPlayed + timeThreshold < int(jasonUser[0]['total_seconds_played']): #Remember to adjust this value later
                print(jasonUser[0]['total_seconds_played'])
                print(totalSecondsPlayed)
                if breakTime(int(jasonUser[0]['total_seconds_played']) - totalSecondsPlayed, jasonRecent):
                    numMaps = 0
                    totalSecondsPlayed = int(jasonUser[0]['total_seconds_played'])
                    lastTimePlayed = jasonRecent[0]['date']
