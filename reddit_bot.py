import praw
import spotipy
from imgurpython import ImgurClient
import time

r = praw.Reddit(user_agent="DiscographyBot by /u/Brozilean")
# r.login(disable_warning=True)
# imgur = ImgurClient
sp = spotipy.Spotify()

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
            albumItem = "[{name:s}]( {albumURL:s} ) | [Artwork Link]( {image:s} )\n".format(
                name=album['name'],
                albumURL=album['external_urls']['spotify'],
                image=album['images'])
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
