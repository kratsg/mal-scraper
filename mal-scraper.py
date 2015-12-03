'''
First step, get username and password for logging in
'''
import os
import json
import myanimelist
import logging
username = os.environ.get('user', None)
password = os.environ.get('pass', None)
if username is None or password is None:
    raise ValueError('Must specify username and password for MyAnimeList.')

'''
Set up configurations for logging
'''
logging.basicConfig(filename='mal-scraper.log', filemode='w', level=logging.DEBUG)

'''
Let's load in the python-mal package and start a session
'''
from myanimelist.session import Session
s = Session(username=username, password=password)

'''
Let's hope we logged in just fine.

Create the anime directory if it does not exist
'''
if not os.path.exists('anime'):
    os.makedirs('anime')

'''
Time to start the loop, let's make sure we catch the right exceptions
'''
from myanimelist.anime import InvalidAnimeError, MalformedAnimePageError
i = 0
anime_attributes = [
    # the following come from myanimelist.anime
    'aired',
    'duration',
    'episodes',
    'producers',
    'rating',
    'staff',
    'voice_actors',
    # the following come from myanimelist.media
    'alternative_titles',
    'characters',
    'favorites',
    'genres',
    'members',
    'picture',
    'popular_tags',
    'popularity',
    'rank',
    'related',
    'score',
    'score_stats',
    'status',
    'status_stats',
    'synopsis',
    'title',
    'type'
]

while True:
    try:
        anime = s.anime(i)
        # force a load
        anime.load()
        with open('anime/{0:d}.json'.format(i), 'w+') as f:
            json.dump(dict((attr, getattr(anime, attr)) for attr in anime_attributes), f, sort_keys=True, indent=4, separators=(',', ': '))
    except (InvalidAnimeError, MalformedAnimePageError) as e:
        logging.exception(e)
    i+=1
