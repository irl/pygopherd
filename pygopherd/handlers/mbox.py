# pygopherd -- Gopher-based protocol server in Python
# module: Present a mbox file as if it were a folder.
# Copyright (C) 2002, 2005 John Goerzen
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


import re
import os, stat, os.path, mimetypes
from pygopherd import protocols, gopherentry
from pygopherd.handlers.virtual import Virtual
from pygopherd.handlers.base import VFS_Real
from mailbox import mbox, Maildir
from stat import *


###########################################################################
# Basic mailbox support
###########################################################################

class FolderHandler(Virtual):
    def getentry(self):
        ## Return my own entry.
        if not self.entry:
            self.entry = gopherentry.GopherEntry(self.getselector(),
                                                 self.config)
            self.entry.settype('1')
            self.entry.setname(os.path.basename(self.getselector()))
            self.entry.setmimetype('application/gopher-menu')
            self.entry.setgopherpsupport(0)
        return self.entry

    def prepare(self):
        self.entries = []
        count = 1
        mbox_iter = self.mbox.itervalues()
        while 1:
            try:
                message = next(mbox_iter)
                handler = MessageHandler(self.genargsselector(self.getargflag() + \
                                         str(count)), self.searchrequest,
                                         self.protocol, self.config, None)
                self.entries.append(handler.getentry(message))
                count += 1
            except StopIteration:
                break

    def isdir(self):
        return 1

    def getdirlist(self):
        return self.entries

class MessageHandler(Virtual):
    def canhandlerequest(self):
        """We put MBOX-MESSAGE in here so we don't have to re-check
        the first line of the mbox file before returning a true or false
        result."""
        if not self.selectorargs:
            return 0
        msgnum = re.search('^' + self.getargflag() + '(\d+)$',
                           self.selectorargs)
        if not msgnum:
            return 0
        self.msgnum = int(msgnum.group(1))
        self.message = None
        return 1

    def getentry(self, message = None):
        """Set the message if called from, eg, the dir handler.  Saves
        having to rescan the file.  If not set, will figure it out."""
        if not message:
            message = self.getmessage()
            
        if not self.entry:
            self.entry = gopherentry.GopherEntry(self.selector, self.config)
            self.entry.settype('0')
            self.entry.setmimetype('text/plain')
            self.entry.setgopherpsupport(0)

            subject = message.get('Subject', '<no subject>')
            # Sanitize, esp. for continuations.
            subject = re.sub('\s+', ' ', subject)
            if subject:
                self.entry.setname(subject)
            else:
                self.entry.setname('<no subject>')
        return self.entry

    def getmessage(self):
        if self.message:
            return self.message
        self.mbox = self.openmailbox()
        message = None
        mbox_iter = self.mbox.itervalues()
        for x in range(self.msgnum):
            message = next(mbox_iter)
        self.message = message
        return self.message

    def prepare(self):
        self.canhandlerequest()         # Init the vars

    def write(self, wfile):
        #for header in self.getmessage().headers:
        #    wfile.write(header)

        # Now the message body.
        #body = self.getmessage().get_payload()
        #wfile.write(body.encode('ascii'))
        wfile.write(self.getmessage().as_bytes())

###########################################################################
# Unix MBOX support
###########################################################################

class MBoxFolderHandler(FolderHandler):
    def canhandlerequest(self):
        """Figure out if this is a handleable request."""

        if self.selectorargs:
            return 0
        
        if not (self.statresult and S_ISREG(self.statresult[ST_MODE])):
            return 0
        try:
            fd = self.vfs.open(self.getselector(), "rt")
            startline = fd.readline()
            fd.close()
            fromlinepattern = 'From \\s*[^\\s]+\\s+\\w\\w\\w\\s+\\w\\w\\w\\s+\\d?\\d\\s+\\d?\\d:\\d\\d(:\\d\\d)?(\\s+[^\\s]+)?\\s+\\d\\d\\d\\d\\s*[^\\s]*\\s*$'
            return re.match(fromlinepattern, startline)
        except IOError:
            return 0

    def prepare(self):
        self.rfile = self.vfs.getfspath(self.getselector())
        self.mbox = mbox(self.rfile)
        FolderHandler.prepare(self)

    def getargflag(self):
        return "/MBOX-MESSAGE/"

class MBoxMessageHandler(MessageHandler):
    def getargflag(self):
        return "/MBOX-MESSAGE/"

    def openmailbox(self):
        rfile = self.vfs.getfspath(self.getselector())
        return mbox(rfile)

###########################################################################
# Maildir support
###########################################################################

class MaildirFolderHandler(FolderHandler):
    def canhandlerequest(self):
        if not isinstance(self.vfs, VFS_Real):
            return 0
        if self.selectorargs:
            return 0
        if not (self.statresult and S_ISDIR(self.statresult[ST_MODE])):
            return 0
        return self.vfs.isdir(self.getselector() + "/new") and \
               self.vfs.isdir(self.getselector() + "/cur")

    def prepare(self):
        self.mbox = Maildir(self.getfspath())
        FolderHandler.prepare(self)

    def getargflag(self):
        return "/MAILDIR-MESSAGE/"

class MaildirMessageHandler(MessageHandler):
    def getargflag(self):
        return "/MAILDIR-MESSAGE/"

    def openmailbox(self):
        return Maildir(self.getfspath())

