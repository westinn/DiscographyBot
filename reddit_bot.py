# basic networking imports
from pprint import pprint
import requests
import json
# image handling imports
import base64
import urllib
from io import StringIO
import Image
# file handling
import linecache
import praw
import spotipy

# reddit data
redditUser = linecache.getline('bot_data.txt', 0)
redditPass = linecache.getline('bot_data.txt', 1)
r = praw.Reddit()
rClient = reddit_login()


# followed
# http://blog.tankorsmash.com/?p=295
def reddit_login():
    # create dict with username and password
    user_pass_dict = {'user': redditUser, 'passwd': redditPass, 'api_type': 'json'}
    # set the header for all the following requests
    headers = {'user-agent': "DiscographyBot by /u/Brozilean"}

    # create a requests.session that'll handle our cookies for us
    client = requests.session()
    client.headers = headers

    # make a login request, passing in the user and pass as data
    post = client.post(r'http://www.reddit.com/api/login', data=user_pass_dict)

    # optional print to confirm error-free response
    # pprint(r.content)

    # turns the response's JSON to a native python dict
    j = json.loads(post.content)

    # grabs the modhash from the response
    client.modhash = j['json']['data']['modhash']

    # prints the users modhash
    # print('{USER}\'s modhash is: {mh}'.format(USER=username, mh=client.modhash))
    client.user = redditUser
    return client


# followed
# http://blog.tankorsmash.com/?p=249
def image_upload(spImgUrl, name):
    # image processing aka grab URL, read data, rencode binary data, upload b64image
    file = StringIO(urllib.urlopen(spImgUrl).read())
    img = open(file, 'rb')
    binary_data = img.read()
    b64image = base64.b64encode(binary_data)
    payload = {'key': iKey,
               'image': b64image,
               'title': name}
    # make the POST request, with the attached data of payload
    post = requests.post(iUpload, data=payload)
    # turn the returned jso0n into a python dict
    j = json.loads(r.text)
    finalImage = j['upload']['links']['imgur_page']
    return finalImage


# imgur data
iKey = linecache.getline('bot_data.txt', 2)[4:]
iUpload = r'http://api.imgur.com/2/upload.json'

# spotify data
sp = spotipy.Spotify()

# bot data
words_to_match = ["!discobot"]
cache = []


# Returns an artist's ID
def find_artist(artist):
    results = sp.search(q=artist, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


# Returns a given artists albums
def find_albums(artist):
    albums = []
    added = []
    results = sp.artist_albums(artist['id'], album_type='album')
    results = results['items']

    for album in results:
        albumName = album['name']
        if albumName not in added:
            albums.append(album)
            added.append(albumName)
    print(albums)
    albums = comment_formatter(albums)


def comment_formatter(albums):
    comment = "Title | Album Artwork\n" + ":--|:--:\n"
    for album in albums:
        if len(album['images']) > 0:
            img = image_upload(album['images'][0], album['name'])

            albumItem = "[{name:s}]( {albumURL:s} ) | [Artwork Link]( {image:s} )\n".format(
                name=album['name'],
                albumURL=album['external_urls']['spotify'],
                image=img)
        else:
            albumItem = "[{name:s}]( {albumURL:s} ) | No Artwork Available\n".format(
                name=album['name'],
                albumURL=album['external_urls']['spotify'])
        comment += albumItem


def disco_bot(artist):
    find_albums(find_artist(artist))


# def run_bot():
#     subreddit = r.get_subreddit("test")
#     comments = subreddit.get_comments(limit=None)
#     for comment in comments:
#         comment_text = comment.body.lower()
#         isMatch = any(string in comment_text for string in words_to_match)
#         if isMatch and comment.id not in cache:
#             comment.reply('I think you meant to say definitely')
#             cache.append(comment.id)
#
#
# while True:
#     run_bot()
#     time.sleep(10)

disco_bot('schoolboy q')
