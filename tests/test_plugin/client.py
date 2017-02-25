import asyncio


class Client:
    def __init__(self, loop):
        self.loop = loop

    async def connect(self, config):
        while self.loop.is_running():
            try:
                await asyncio.sleep(2, loop=self.loop)
            except asyncio.CancelledError:
                break
