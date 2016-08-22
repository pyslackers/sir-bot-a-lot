from .roll import roll_dice

""" A dice module!
Usage:
    $BOTNAME: roll          - Rolls a d20 once
    $BOTNAME: roll 5d5      - Rolls a d5 5 times
    $BOTNAME: roll d6+5     - Rolls a d6 once and adds 5
"""

commands = {
    "roll": roll_dice,
}
