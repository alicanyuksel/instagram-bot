# Instagram BOT

To do this, I used the following repository : [instagrapi](https://github.com/adw0rd/instagrapi)

The goal of this project is to post earthquakes photos captured with **MapBox** on Instagram with the details like location, magnitude, depth, etc.

This is a personal project and it's coded with our configuration.

**There are no commercial purposes.**

## Requirements

    pip install -r requirements.txt

### To run

    python run.py

## Config file

To test our bot, you should change the config file by adding:

- Path for images that will be generated (optional)

- Path for json file that will store the earthquakes detected and posted (optional)

- You can put your hashtags if you want (optional)

## Environment variables

- ACCESS_TOKEN : Your mapbox access token (you need just sign up on **[MapBox](http://mapbox.com)**)

- ACCOUNT_USERNAME, ACCOUNT_PASSWORD :
Your Instagram account (username and password)

## Data

The data comes from the site [depremneredeoldu.com](https://depremneredeoldu.com) which use itself the data of **Kandilli Observatory and Earthquake Research Institute**.
