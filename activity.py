# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""HelloWorld Activity: A case study for developing an activity."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem


class MakeChatBotActivity(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""

    import json
    questions = {}
    questions['Hello'] = 'Hi'
    questions['How are you'] = 'Good'

    # Time Stuff
    import datetime
    import time
    localtime = time.asctime( time.localtime(time.time()) )

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        #make a grid
        self.grid = Gtk.Grid()
        self.set_canvas(self.grid)

        #chat
        self.button2 = Gtk.Button(label="Submit")
        self.button2.connect("clicked", self.chat)
        self.grid.attach(self.button2, 15, 0, 4, 1)
        self.button2.show()

        #entry
        self.entry = Gtk.Entry()
        self.entry.set_width_chars(60)
        self.entry.set_placeholder_text("Type in your question or add a question by typing q:<<yyour question>> a:<<your answer>> or type i:/e: to import/export questions")
        self.grid.attach(self.entry, 10, 0, 4, 1)
        self.entry.show()
        #Help
        self.label0 = Gtk.Label()
        self.label0.set_text(_("For Help Regarding The Make chatbot activity please see bit.do/mcbh"))
        self.grid.attach(self.label0, 0, 1, 4, 1)
        self.label0.show()
        self.grid.show()

    def import1(self, json_stuff):
        try:
            self.questions = json.loads(json_stuff)
            return "Success"
        except():
            print(sys.exc_info()[0])
            return "Please Enter Valid JSON"

    #Making Questions
    def makeQA(self, q, a):
        self.questions[str(q)] = str(a)
        return "Success"

    #Answer Formatting
    def formatanswer(self, text):
        answer = text
        if (answer.find("|MONTH|") != -1):
            text = text.replace("", str(datetime.now().month()))
        if (answer.find("|DAY|") != -1):
            text = text.replace("|DAY|", str(datetime.now().day()))
        if (answer.find("|YEAR|") != -1):
            text = text.replace("|YEAR|", str(datetime.date.today().year))
        if (answer.find("|TIME|") != -1):
            text = text.replace("|TIME|", str(localtime))
        if (answer.find("|QUESTION|") != -1):
            text = text.replace("|QUESTION|", str(question))
        return text

    #Getting Old Questions
    def answerQA(self, uquestion):
        try:
            return self.formatanswer(self.questions[str(uquestion)])
        except:
            return "Not a valid question"

    #export JSON
    def export1(self):
        try:
            json_data = json.dumps(self.questions)
            return str(json_data)
        except:
            return "{Hello: Hi, How are you: Good}"

    def chat(self, EntryValue):
        query = str(self.entry.get_text())
        r_value = "fail"
        i = 0
        if query.find("a:") != -1:
            s2 = query.split('a:')
            r_value = self.makeQA(str(s2[0]), str(s2[1]))
            i = 1

        if (query.find("i:") != -1):
            r_value = self.import1(str(query.replace("i:","")))
            i=1

        if (query.find("e:") != -1):
            r_value = self.export1()
            i=1

        if i != 1:
            r_value = self.answerQA(query)

        self.label = Gtk.Label(_(r_value))
        self.grid.attach(self.label, 0, 0, 4, 1)
        try:
            print(i)
            self.label.set_text(r_value)
        except:
            self.label.hide()
        self.label.show()
        self.grid.show()
        i = 5
