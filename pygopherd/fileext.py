# pygopherd -- Gopher-based protocol server in Python
# module: File extension utility
# Copyright (C) 2002 John Goerzen
# <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import mimetypes

typemap = {}

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def extcmp(x, y):
    if x.count('.') > y.count('.'):
        return 1
    if x.count('.') < y.count('.'):
        return -1
    if len(x) > len(y):
        return 1
    if len(x) < len(y):
        return -1
    return (x>y)-(x<y)

def extstrip(file, filetype):
    """Strips off the extension from file given type and returns the result.
    Returns file unmodified if no action is possible."""
    if not (filetype and filetype in typemap):
        return file
    for possible in typemap[filetype]:
        if file.endswith(possible):
            extindex = file.rfind(possible)
            return file[0:extindex]
    return file

def init():
    for fileext, filetype in list(mimetypes.types_map.items()):
        extlist = []
        if filetype in typemap:
            extlist = typemap[filetype]

        baselist = []
        # Add the basic extension.
        baselist.append(fileext)
        # Add it in all encoding flavors.
        baselist.extend(
            [fileext + enc for enc in list(mimetypes.encodings_map.keys())])

        for shortsuff, longsuff in list(mimetypes.suffix_map.items()):
            if longsuff in baselist:
                baselist.append(shortsuff)

        extlist.extend(baselist)
        extlist.sort(key=cmp_to_key(extcmp))
        extlist.reverse()
        typemap[filetype] = extlist


        
