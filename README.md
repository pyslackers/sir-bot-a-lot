# Sir Bot a Lot

[![build status](https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/badges/master/build.svg)](https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/commits/master)
[![coverage report](https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/badges/master/coverage.svg)](https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/commits/master)

A slack bot built for the people and by the people of the python developers slack community. https://pythondev.slack.com/
Want to contribute?
Get an invite!
http://pythondevelopers.herokuapp.com/

* Documentation: https://sir-bot-a-lot.readthedocs.io

## Getting Started (with docker)

Running a copy of the bot locally requires using `docker` and `docker-compose`. Assuming you have those two items, here are the commands you can use.

> Note: You will need to have the `SIRBOT_TOKEN` set to your Slack API token in the local environment. 

```
# Build the local environment
$ make build

# If you already have SIRBOT_TOKEN set
# Start up the local environment
$ make serve

# To set the `SIRBOT_TOKEN` before running make serve
$ SIRBOT_TOKEN=xoxo-34343534343-232323 make serve
```
