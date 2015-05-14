import sys
import threading
import MPDC

class Updater(threading.Thread):
    def __init__(self, builder, mpdc):
        self.builder = builder
        self.mpdc = mpdc
        threading.Thread.__init__(self)

    def run(self):
        nowPlaying = self.mpdc.getNowPlaying()

        songTitle = self.builder.get_object("lSongTitle")
        songTitle.set_text(nowPlaying['title'])

        print(nowPlaying)

        artist = self.builder.get_object("lArtist")
        artist.set_text(nowPlaying['artist'])

        album = self.builder.get_object("lAlbum")
        album.set_text(nowPlaying['album'])

        totalM, totalS = divmod(int(nowPlaying['time']), 60)
        totalTime = "%02d:%02d" % (totalM, totalS)

        length = self.builder.get_object("lLength")
        length.set_text(totalTime)

class Handler:

    def __init__(self, builder):
        self.builder = builder
        self.mpdc = MPDC.MPDCli("192.168.0.3")

        self.updateThread = Updater(self.builder, self.mpdc)
        updateThread.start()

    def onDeleteWindow(self, *args):
        self.mpdc.close()
        Gtk.main_quit(*args)

    def playClick(self, button):
        self.mpdc.play()

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

try:
    from gi.repository import Gtk
except:
    print("GTK Not Availible")
    sys.exit(1)

builder = Gtk.Builder()
builder.add_from_file("MainWindow.glade")
builder.connect_signals(Handler(builder))

window = builder.get_object("MainWindow")
window.show_all()

Gtk.main()

print("END")