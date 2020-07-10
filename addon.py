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

from sys import argv
from tulip.compat import parse_qsl
from tulip import control, bookmarks
from resources.lib import hng

sysaddon = argv[0]
syshandle = int(argv[1])
params = dict(parse_qsl(argv[2][1:]))
action = params.get('action')
url = params.get('url')


if action is None:

    hng.main()

elif action == 'videos':

    hng.videos()

elif action == 'play':

    hng.play(url)

elif action == 'refresh':

    control.refresh()

elif action == 'playlists':

    hng.playlists()

elif action == 'youtube':

    hng.yt(url)

elif action == 'third_party':

    hng.third_party()

elif action == 'bookmarks':

    hng.bm_list()

elif action == 'addBookmark':

    bookmarks.add(url)

elif action == 'deleteBookmark':

    bookmarks.delete(url)

elif action == 'settings':

    control.openSettings()

elif action == 'cache_clear':

    if control.yesnoDialog(line1=control.lang(30009), line2='', line3=''):

        control.deleteFile(control.cacheFile)
        control.infoDialog(control.lang(30010))

    else:

        control.infoDialog(control.lang(30011))