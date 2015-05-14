from mpd import MPDClient

class MPDCli:
    def __init__(self, ipaddress):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.client.connect(ipaddress, 6600)

        self.ip = ipaddress

    def close(self):
        self.client.close()
        self.client.disconnect()

    def __tryConnect(self):
        try:
            self.client.update()
        except ConnectionError:
            self.client.connect(self.ip, 6600)
            self.client.update()

    def getNowPlaying(self):
        self.__tryConnect()
        return self.client.currentsong()

    def play(self):
        self.__tryConnect()
        self.client.pause()
