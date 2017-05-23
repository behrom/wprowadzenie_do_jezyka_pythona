#-*- coding: utf-8 -*-

import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random

class App:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("Window")


        self.entry1 = Gtk.Entry()
        self.entry1.connect("changed", self.zmien)

        self.entry2 = Gtk.Entry();

        box = Gtk.VBox()
        box.pack_start(self.entry1, True, True, 0)
        box.pack_start(self.entry2, True, True, 0)

        self.window.add(box)
        self.window.show_all()

    def zmien(self, entry):
        txt = entry.get_text()
        if len(txt) > 2:
            shuffled = list(txt[1:-1])
            random.shuffle(shuffled)
            shuffled = ''.join(shuffled)
            self.entry2.set_text(txt[0] + shuffled + txt[-1])

if __name__ == "__main__":
    a = App()
    Gtk.main()