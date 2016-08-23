# -*- coding: utf-8 -*-
"""
test_dice
----------------------------------

Tests for `dice` plugin
"""
import pytest
from sirbot.plugins import dice

class TestDiceBot(object):
    @classmethod
    def set_up(self):
        pass

    def test_regex_parse_full(self):
        result = dice.roll.parse_dice('6d5+10')
        assert(result.get('number') == 6)
        assert(result.get('face') == 5)
        assert(result.get('add') == 10)
        pass

    def test_regex_parse_neg(self):
        result = dice.roll.parse_dice('6d5-10')
        assert(result.get('add') == -10)
        pass

    def test_regex_parse_spaces(self):
        result = dice.roll.parse_dice('6d5 - 10')
        assert(result.get('add') == -10)

    def test_roll_adds(self):
        ctx = {'user': 'test'}
        result = dice.roll_dice(ctx, '10d1+10')
        assert(result == 'test - Rolled 10d1+10 for a result of 20')
        
    @classmethod
    def tear_down(self):
        pass
