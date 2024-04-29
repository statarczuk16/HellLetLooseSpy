import asyncio
import logging

import common


class Clock(object):
    def __init__(self, interval=1):
        self.counter = 0
        self.interval = interval
        self.tick = asyncio.Event()  # an event can be set to true or false, tick.wait() waits for true
        asyncio.ensure_future(self.tick_tock())  # ensure_future means this runs in background, no one is waiting for it
        self.busy = True
        self.interrupt = False
        self.pause = False

    async def tick_tock(self):
        while True:
            self.tick.clear()  # calling awaiting tick has to wait for tick.set() now
            await asyncio.sleep(self.interval)
            if self.pause == False:
                self.counter = self.__next__()
            self.tick.set()  # caller awaiting tick will not get a value until now

    def __next__(self):
        self.counter += 1 * common.time_scale_global.get()
        return self.counter

    async def wait_for_time(self, time_to_wait):
        time_to_return_at = self.counter + time_to_wait
        self.busy = True
        logging.debug("Clock waiting for " + str(time_to_return_at))
        while self.counter < time_to_return_at and self.interrupt == False:
            await self.tick.wait()
        if self.interrupt == True:
            self.interrupt = False
            logging.debug("Clock interrupted. Will not wait until " + str(time_to_wait))
            self.counter = 0
        return

    async def restart(self):
        logging.debug("Restarting clock")
        self.interrupt = True
        self.pause = False
        while self.interrupt == True:
            await self.tick.wait()
        logging.debug("Clock interrupted.")
        self.counter = 0
        return


    def set_counter(self, time_seconds):
        self.tick.clear()  # calling awaiting tick has to wait for tick.set() now
        self.counter = time_seconds
        self.tick.set()  # caller awaiting tick will not get a value until now

    def advance_counter(self, time_seconds):
        self.counter += time_seconds

    def __aiter__(self):
        return self

    def get_game_clock_s(self):
        seconds = self.counter
        game_time = common.GAME_TIME_S - seconds
        if game_time < 0:
            return 0
        return common.GAME_TIME_S - seconds

    async def __anext__(self):
        await self.tick.wait()
        return self.counter
