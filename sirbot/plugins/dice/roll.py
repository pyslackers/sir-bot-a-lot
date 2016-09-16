import re
from random import randint

dice_regex = re.compile(r'(?P<number>\d+)?d?(?P<face>\d+)(?P<add>[\+,-]\d+)?')


def parse_dice(argument):
    argument = argument.strip().replace(' ', '')
    dice_parsed = dice_regex.match(argument).groupdict()
    print('PARSED - {}'.format(dice_parsed))
    dice = {
        'number': int(dice_parsed.get('number', 1)),
        'face': int(dice_parsed.get('face', 20)),
        'add': int(dice_parsed.get('add', 0)),
    }
    return dice


def roll_dice(context, argument):
    dice = parse_dice(argument)
    result = dice['add']
    for _ in range(dice['number']):
        result += randint(1, dice['face'])

    message = '{user} - Rolled {argument} for a result of {result}'.format(
        user=context['user'],
        result=result,
        argument=argument,
    )
    return message
