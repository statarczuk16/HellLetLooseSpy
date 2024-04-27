import asyncio

import common

class Clock(object):
    def __init__(self, interval=1):
        self.counter = 0
        self.interval = interval
        self.tick = asyncio.Event()  # an event can be set to true or false, tick.wait() waits for true
        asyncio.ensure_future(self.tick_tock())  # ensure_future means this runs in background, no one is waiting for it

    async def tick_tock(self):
        while True:
            self.tick.clear()  # calling awaiting tick has to wait for tick.set() now
            await asyncio.sleep(self.interval)
            self.counter = self.__next__()
            self.tick.set()  # caller awaiting tick will not get a value until now

    def __next__(self):
        self.counter += 1 * common.time_scale_global.get()
        return self.counter

    async def wait_for_time(self, time_to_wait):
        time_to_return_at = self.counter + time_to_wait
        print("Waiting for " + str(time_to_return_at))
        while self.counter < time_to_return_at:
            await self.tick.wait()
        print("Done!")
        return

    def set_counter(self, time_seconds):
        self.tick.clear()  # calling awaiting tick has to wait for tick.set() now
        self.counter = time_seconds
        self.tick.set()  # caller awaiting tick will not get a value until now

    def advance_counter(self, time_seconds):
        self.counter += time_seconds

    def __aiter__(self):
        return self

    def restart(self):
        self.tick.clear()  # calling awaiting tick has to wait for tick.set() now
        self.counter = 0
        self.tick.set()  # caller awaiting tick will not get a value until now

    def get_game_clock_s(self):
        seconds = self.counter
        return common.GAME_TIME_S - seconds

    async def __anext__(self):
        await self.tick.wait()
        return self.counter