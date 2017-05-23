#-*- coding: utf-8 -*-

import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class App:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("Window")

        self.label = Gtk.Label("Wymysl liczbe calkowita z zakresu od 1 do 30 a ja ja zgadne")

        self.button = Gtk.Button("Ok mam")
        self.button.connect("clicked", self.odgadnij)

        box = Gtk.VBox()
        box.pack_start(self.label, True, True, 10)
        box.pack_start(self.button, False, False, 10)

        self.window.add(box)
        self.window.show_all()

    def odgadnij(self, button):

        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO, ('Czy była to liczba: {}').format(1))
        res = dialog.run()
        dialog.destroy()
        if res == Gtk.ResponseType.YES:
            print "użytkownik powiedział tak!"
        else:
            print "użytkownik powiedział nie!"


if __name__ == "__main__":
    a = App()
    Gtk.main()