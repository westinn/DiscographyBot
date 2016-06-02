# file handling
import linecache
# image handling imports
import urllib.request
import pyimgur
# reddit imports
import praw
import OAuth2Util
# spotify imports
import spotipy
import os

# reddit data
r = praw.Reddit("DiscographyBot by /u/Brozilean")
o = OAuth2Util.OAuth2Util(r, server_mode=True)
o.refresh(force=True)

# imgur data
# iKey = str(linecache.getline('bot_data.txt', 1))[:-1]
# Retrieve heroku env variables
ik = [os.environ['iKey']]
im = pyimgur.Imgur(ik)
# spotify data
sp = spotipy.Spotify()

# general data
words_to_match = ["!discobot"]
cache = []


# =================================================================================================
# Imgur

# Upload an album cover to imgur
# Could've left it with the spotify link, but doesn't work as well with RES Extension
def image_upload(spImgUrl, albumName):
    image_path = "temp_art.png"
    urllib.request.urlretrieve(spImgUrl, image_path)
    uploaded_image = im.upload_image(image_path, title=albumName)
    return uploaded_image


# =================================================================================================
# Spotify

# Returns an artist's ID
def find_artist(artist):
    results = sp.search(q=artist, type='artist')
    # print(results)
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


# Returns a given artists albums, formatted for reddit
def find_albums(artist):
    albums = []
    added = []

    artistName = artist['name']
    artistData = sp.artist_albums(artist['id'], album_type='album')
    albumsResults = artistData['items']

    for album in albumsResults:
        albumName = album['name']
        if albumName not in added:
            albums.append(album)
            added.append(albumName)
    comment = comment_formatter(artistName, albums)
    print(comment)
    return comment


# =================================================================================================
# Reddit

def comment_formatter(artistName, albums):
    comment = "Title | Album Artwork\n" + ":--|:--:\n"
    for album in albums:
        if len(album['images']) > 0:
            img = image_upload(album['images'][0]['url'], album['name'])
            img = img.link
            albumItem = "[{name:s}]( {albumURL:s} ) | [Artwork Link]( {image:s} )\n".format(
                name=album['name'],
                albumURL=album['external_urls']['spotify'],
                image=img)
        else:
            albumItem = "[{name:s}]( {albumURL:s} ) | No Artwork Available\n".format(
                name=album['name'],
                albumURL=album['external_urls']['spotify'])
        comment += albumItem
    head = "*Here's the discography for:*\n\n**" + artistName + "**\n\n"
    tail = "\n\n*I am a bot. You can provide feedback in my subreddit: /r/DiscographyBot.*"
    finalComment = str(head + comment + tail)
    return finalComment


def get_comment(artist):
    return find_albums(find_artist(artist))


# =================================================================================================
# Run


def run_bot():
    o.refresh()
    subreddit = r.get_subreddit("music+test")
    comments = praw.helpers.comment_stream(r, subreddit, limit=None)
    for comment in comments:
        comment_text = comment.body.lower()
        isMatch = any(string in comment_text for string in words_to_match)
        if isMatch and comment.id not in cache:
            artistName = comment_text[10:]
            comment.reply(get_comment(artistName))
            cache.append(comment.id)


if __name__ is '__main__':
    run_bot()
