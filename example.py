import logging
import os

import aiohttp

from sirbot import SirBot
from sirbot.base import Message

token = os.environ['SIRBOT_TOKEN']

bot = SirBot(token)


logging.getLogger('sirbot').setLevel(logging.DEBUG)


# Example quote of the day plugin
async def get_quote_of_the_day():
    url = 'http://api.theysaidso.com/qod.json'
    quote_r = ''
    async with aiohttp.get(url) as response:
        if response.status != 200:
            raise Exception('Error talking to quote api')
        quote_r = await response.json()

    quote = quote_r['contents']['quotes'][0]['quote']
    author = quote_r['contents']['quotes'][0]['author']

    # Style up the quote for slack
    formatted_quote = '> {0} \n- {1} _theysaidso.com_'.format(quote, author)

    return formatted_quote


@bot.listen('(([Cc]an|[Mm]ay) I have the )?quote of the day\?$')
async def quote_of_the_day(message, *args, **kwargs):
    quote = await get_quote_of_the_day()
    response = Message(quote)
    response.to = message.to

    await bot._rtm_client.post_message(response)


if __name__ == '__main__':
    bot.run()
