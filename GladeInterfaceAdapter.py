import sys
import threading
import MPDC

guiLock = threading.Lock()

class Updater(threading.Thread):
    def __init__(self, builder, ipaddress):
        self.builder = builder
        self.mpdc = MPDC.MPDCli(ipaddress)
        threading.Thread.__init__(self)
        self.firstTime = True

        self.playImage = Gtk.Image()
        self.playImage.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)

        self.pauseImage = Gtk.Image()
        self.pauseImage.set_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.BUTTON)

    def run(self):
        while True:
            if not self.firstTime:
                self.mpdc.idle()

            self.firstTime = False

            with guiLock:
                nowPlaying = self.mpdc.getNowPlaying()

                #Show all the usual info
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

                #Decide what to do with the play pause thing
                currentStatus = self.mpdc.getCurrentStatus()
                print(currentStatus)

                if currentStatus['state'] == 'play':
                    button = self.builder.get_object('bPlay')
                    # button.set_image(self.pauseImage)
                    button.set_label("Pause")
                else:
                    button = self.builder.get_object('bPlay')
                    # button.set_image(self.playImage)
                    button.set_label("Play")

                # currentSeconds = float(currentStatus['elapsed'])
                # Track = self.builder.get_object('pbTrack')
                # Track.set_fraction(currentSeconds / (totalM * 60 + totalS))

class Handler:

    def __init__(self, builder, ipaddress):
        self.builder = builder
        self.mpdc = MPDC.MPDCli(ipaddress)

        self.updateThread = Updater(self.builder, ipaddress)
        self.updateThread.daemon = True
        self.updateThread.start()

    def onDeleteWindow(self, *args):
        with guiLock:
            self.mpdc.close()
            Gtk.main_quit(*args)

    def playClick(self, button):
        with guiLock:
            self.mpdc.play()

    def stopClick(self, button):
        with guiLock:
            self.mpdc.stop()

    def nextClick(self, button):
        with guiLock:
            self.mpdc.next()

    def prevClick(self, button):
        with guiLock:
            self.mpdc.prev()

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
builder.connect_signals(Handler(builder, '192.168.0.3'))

window = builder.get_object("MainWindow")
window.show_all()

Gtk.main()

print("END")