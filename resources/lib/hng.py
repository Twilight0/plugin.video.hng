# -*- coding: utf-8 -*-

'''
    Heroes & Generals Addon
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import json
from base64 import b64decode
from zlib import decompress
from os.path import exists as file_exists
from tulip import directory, youtube, cache, control, bookmarks, client
from tulip.compat import iteritems
from tulip.init import sysaddon, syshandle
from youtube_registration import register_api_keys


MAIN_ID = 'UCdiTNAd8yrUcRaOEotk6oww'
OST = 'PLZF-_NNdxpb4FKRLZ7Z_VTe4ii_ObKyoC'


scramble = (
    'eJwVzNsKgjAAANBfkT2XTMW59SYSYmWgkdGTjDnmfeomMaN/Dz/gnC9oKnCyAPIQDBzi+xB5R8hmriBkNUHSHT1PuBBL'
    '7NS+I4l2MLLpNClbSCl6viq+MDlqPmqbyQEcLECnpuy42dsw2ejDRGc0yyII1ix95Ui4Q1JsbabwR88zLa8m3ZXibOF6R'
    '2/TB2HcVreCXkS8LU/Y5RG5b+D3Bwj/Nu0='
)


def item_list(id=MAIN_ID):

    keys = json.loads(decompress(b64decode(scramble)))

    key = keys['api_key']

    return youtube.youtube(key=key).videos(id, limit=10)


def _playlists(id=MAIN_ID):

    keys = json.loads(decompress(b64decode(scramble)))

    key = keys['api_key']

    return youtube.youtube(key=key).playlists(id)


def keys_registration():

    filepath = control.transPath(
        control.join(control.addon('plugin.video.youtube').getAddonInfo('profile'), 'api_keys.json'))

    setting = control.addon('plugin.video.youtube').getSetting('youtube.allow.dev.keys') == 'true'

    if file_exists(filepath):

        f = open(filepath)

        jsonstore = json.load(f)

        no_keys = control.addonInfo('id') not in jsonstore.get('keys', 'developer').get('developer')

        if setting and no_keys:
            keys = json.loads(decompress(b64decode(scramble)))

            register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])

        f.close()


def third_party():

    keys_registration()

    menu = []

    channels = [
        {
         'title': 'Kotton Gamer',
         'icon': 'https://yt3.ggpht.com/-INHVBEYrqPs/AAAAAAAAAAI/AAAAAAAAAAA/KIxzHZaoLAE/s256-c-k-no-mo-rj-c0xffffff/photo.jpg',
         'url': 'UCuVsAtrhly8r38slgKYihqw'
        },
        {
         'title': 'Atway',
         'icon': 'https://yt3.ggpht.com/-ndqPynNZhng/AAAAAAAAAAI/AAAAAAAAAAA/_1t_ZtmICKs/s256-c-k-no-mo-rj-c0xffffff/photo.jpg',
         'url': 'UC80K82TkjjQ-mauzncjTxeQ'
        },
        {
         'title': 'Luftangreifer',
         'icon': 'https://yt3.ggpht.com/-2cqx9aLhEaE/AAAAAAAAAAI/AAAAAAAAAAA/DNMsGKqVzek/s256-c-k-no-mo-rj-c0xffffff/photo.jpg',
         'url': 'UCaX0s3rQjI4fZYli4G0YwNA/playlist/PLZhVK1RzI0ZIx6fF7szLnfC62ZgazoTYK'
        },
        {
         'title': 'Schilli',
         'icon': 'https://yt3.ggpht.com/-6ZZ8Y18Vow4/AAAAAAAAAAI/AAAAAAAAAAA/GKc2Q-Hij5w/s256-c-k-no-mo-rj-c0xffffff/photo.jpg',
         'url': 'UC4AAJlFH9Pl0vj0hlF5M9bQ'
        },
        {
         'title': 'Ignitation',
         'icon': 'https://yt3.ggpht.com/-bjbqCx0kGvY/AAAAAAAAAAI/AAAAAAAAAAA/bJfBTiVyPOQ/s256-c-k-no-mo-rj-c0xffffff/photo.jpg',
         'url': 'UC9xyLaJGLBOZ81r4bvp7VfQ'
        },
        {
         'title': 'Nemesis 073',
         'icon': 'https://yt3.ggpht.com/-D_kVdH4dBdI/AAAAAAAAAAI/AAAAAAAAAAA/nagGMSVcYOY/s256-c-k-no-mo-rj-c0xffffff/photo.jpg',
         'url': 'UCWWu23gFvqP6_gGz8ZTJkeg'
        }
    ]

    plugin = 'plugin://plugin.video.youtube/channel/'

    for channel in channels:
        channel['url'] = ''.join([plugin, channel['url'], '/?addon_id=', control.addonInfo('id')])
        li = control.item(label=channel['title'])
        li.setArt({'icon': channel['icon'],'fanart': control.addonInfo('fanart')})
        li.addContextMenuItems([(control.lang(30006), 'RunPlugin({0}?action=addBookmark)'.format(sysaddon))])
        url = channel['url']
        menu.append((url, li, True))

    control.addItems(syshandle, menu)
    control.directory(syshandle)


def playlists():

    _list = cache.get(_playlists, 24)

    for p in _list:
        p.update({'action': 'youtube'})

    for p in _list:
        bookmark = dict((k, v) for k, v in iteritems(p) if not k == 'next')
        bookmark['bookmark'] = p['url']
        bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        refresh = {'title': 30008, 'query': {'action': 'refresh'}}
        cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
        p.update({'cm': [refresh, cache_clear, bm_cm]})

    directory.add(_list)


def yt(pid):

    keys = json.loads(decompress(b64decode(scramble)))

    key = keys['api_key']

    _list = cache.get(youtube.youtube(key=key).playlist, 12, pid)

    if _list is None:
        return

    for i in _list:
        i.update({'action': 'play', 'isFolder': 'False'})

    for item in _list:
        bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
        bookmark['bookmark'] = item['url']
        bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        refresh = {'title': 30008, 'query': {'action': 'refresh'}}
        cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
        item.update({'cm': [refresh, cache_clear, bm_cm]})

    directory.add(_list)


def videos():

    video_list = cache.get(item_list, 12)

    if video_list is None:
        return

    for v in video_list:
        try:
            v['title'] = client.replaceHTMLCodes(v['title'].decode('utf-8'))
        except Exception:
            v['title'] = client.replaceHTMLCodes(v['title'])
        v.update({'action': 'play', 'isFolder': 'False'})

    for item in video_list:
        bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
        bookmark['bookmark'] = item['url']
        bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        refresh = {'title': 30008, 'query': {'action': 'refresh'}}
        cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
        item.update({'cm': [refresh, cache_clear, bm_cm]})

    directory.add(video_list)


def bm_list():

    bm = bookmarks.get()

    na = [{'title': 30012, 'action': None, 'icon': 'camouflage.jpg'}]

    if not bm:
        directory.add(na)
        return na

    for item in bm:
        bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
        bookmark['delbookmark'] = item['url']
        item.update({'cm': [{'title': 30007, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

    il = sorted(bm, key=lambda k: k['title'].lower())

    directory.add(il)


def main():

    menu = [
        {
            'title': 30001,
            'action': 'videos',
            'icon': 'pointerquickfire.jpg'
        }
        ,
        {
            'title': 30002,
            'action': 'playlists',
            'icon': 'tightgrip.jpg'
        }
        ,
        {
            'title': 30016,
            'action': 'youtube',
            'url': OST,
            'icon': 'ghillie.jpg'
        }
        ,
        {
            'title': 30003,
            'action': 'bookmarks',
            'icon': 'marathonman.jpg'
        }
        ,
        {
            'title': 30013,
            'action': 'third_party',
            'icon': 'scavenger.jpg'
        }
        ,
        {
            'title': 30004,
            'action': 'settings',
            'icon': 'mechanic.jpg',
            'isFolder': 'False', 'isPlayable': 'False'
        }
    ]

    if control.setting('third_party') == 'false':
        del menu[-2]

    cc = {'title': 30005, 'query': {'action': 'cache_clear'}}

    for item in menu:
        item.update({'cm': [cc]})

    directory.add(menu)


def play(url):

    directory.resolve(url)
