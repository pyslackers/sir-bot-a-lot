import asyncio


class Client:
    def __init__(self, loop, queue):
        self.loop = loop

    def configure(self, config, router):
        pass

    async def connect(self):
        while self.loop.is_running():
            try:
                await asyncio.sleep(2, loop=self.loop)
            except asyncio.CancelledError:
                break
