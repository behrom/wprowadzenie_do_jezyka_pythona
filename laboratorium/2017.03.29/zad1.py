#!/usr/bin/env python
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class App(object):

    def __init__(self):
        self.len1 = Gtk.Label()
        self.len2 = Gtk.Label()
        self.len3 = Gtk.Label()
        self.len4 = Gtk.Label()
        self.entry = Gtk.Entry()

        self.entry.set_text("")

        self.entry.connect("changed", self.edytowano)

        box = Gtk.VBox()
        box.pack_start(self.entry, True, True, 0)
        box.pack_start(self.len1, True, True, 0)
        box.pack_start(self.len2, True, True, 0)
        box.pack_start(self.len3, True, True, 0)
        box.pack_start(self.len4, True, True, 0)

        self.window = Gtk.Window()
        self.window.add(box)
        self.window.set_default_size(640, 480)

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

    def edytowano(self, entry):
        tekst = str(entry.get_text())
        self.len1.set_text(str(len(tekst)))
        self.len2.set_text(str(sys.getsizeof(tekst)))
        self.len3.set_text(tekst.upper())
        self.len4.set_text(unicode(tekst).upper())


# uruchamiam glowna petle tylko jesi program jest uruchamiany "wprost"
# bez tej linijki okienko pojawi sie przy importowaniu tego pliku zrodlowego z poziomu innego kodu
if __name__ == "__main__":
    a = App()
    Gtk.main()