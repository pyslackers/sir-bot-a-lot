import os

import aiohttp

from sirbot import SirBot

token = os.environ['SIRBOT_TOKEN']

bot = SirBot(token)


# Example quote of the day plugin
async def get_quote_of_the_day():
    url = 'http://api.theysaidso.com/qod.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
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

    # This will definitely change once the HTTP client is implemented.
    # The main idea is that everything is in the message and the api
    # would look like this:
    # message.send(quote)
    await bot._rtm_client.post_message(message['channel'], quote)


if __name__ == '__main__':
    bot.run()
