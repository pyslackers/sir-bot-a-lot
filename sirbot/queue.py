import asyncio


class IterableQueue(asyncio.Queue):
    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.get()
        except StopIteration:
            raise StopAsyncIteration
