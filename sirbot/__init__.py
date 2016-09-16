# -*- coding: utf-8 -*-
"""
sirbot
~~~~~~~~~~~~~~~~~~~

the sirbot api

:copyright: (c) 2016 by Python Developers Slack Community
:licence: MIT, see LICENCE for more details
"""
# http://patorjk.com/software/taag/#p=display&f=Star%20Wars&t=sirbot

#      _______. __  .______         .______     ______   .___________.
#     /       ||  | |   _  \        |   _  \   /  __  \  |           |
#    |   (----`|  | |  |_)  |       |  |_)  | |  |  |  | `---|  |----`
#     \   \    |  | |      /        |   _  <  |  |  |  |     |  |
# .----)   |   |  | |  |\  \----.   |  |_)  | |  `--'  |     |  |
# |_______/    |__| | _| `._____|   |______/   \______/      |__|
#                          ___                 __        ______   .___________.
#                         /   \               |  |      /  __  \  |           |
#                        /  ^  \     _______  |  |     |  |  |  | `---|  |----`
#                       /  /_\  \   |       | |  |     |  |  |  |     |  |
#                      /  _____  \   -------  |  `----.|  `--'  |     |  |
#                     /__/     \__\           |_______| \______/      |__|

DATA = {
    "author": 'Mike from IT',
    "author_email": 'mike@mikefromit.com',
    "copyright": 'Copyright 2016 Python Developers Community',
    "description": 'The good Sir Bot a lot',
    "license": 'MIT',
    "name": 'sirbot',
    "url": 'https://gitlab.com/mikefromit/sirbot',
    # Versions should comply with PEP440. For a discussion on
    # single-sourcing the version across setup.py and the project code,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    "version": '0.0.1',
    'docker_name': 'sirbot_api',
    'docker_tag': 'latest'
}

from .core import SirBot  # noqa
