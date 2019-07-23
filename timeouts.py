import time

class Timeouts():
    def __init__(self):
        self.timeouts = dict()

    def add_timeout(self, channel_id, command, length):
        if channel_id not in self.timeouts:
            self.timeouts[channel_id] = dict()

        self.timeouts[channel_id][command] = time.time() + length

    def is_timeout(self, channel_id, command):
        if channel_id in self.timeouts and command in self.timeouts[channel_id]:
            if time.time() > self.timeouts[channel_id][command]:
                return False
            else:
                return True

        return False