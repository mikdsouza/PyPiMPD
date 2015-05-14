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

    def getCurrentStatus(self):
        self.__tryConnect()
        return self.client.status()

    def play(self):
        self.__tryConnect()
        self.client.pause()
        return self.client.status()

    def stop(self):
        self.__tryConnect()
        self.client.stop()
        return self.client.status()

    def prev(self):
        self.__tryConnect()
        self.client.previous()
        return self.client.status()

    def next(self):
        self.__tryConnect()
        self.client.next()
        return self.client.status()

    def idle(self):
        self.__tryConnect()
        self.client.idle()
