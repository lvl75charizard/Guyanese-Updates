import check_percentage
from secrets import Secrets
import praw
import newsroom
import villagevoice
import constants
import random
import time
import dem_boys_seh
from urllib.request import urlopen
from firebase_db import database_read_seh, database_write_seh
import firebase_db


def internet_on():
    try:
        response = urlopen('https://www.google.com/', timeout=1)
        return True
    except:
        return False


def check_internet():
    constants.check_last_agency_exist()
    # constants.check_last_demboysseh_exist()
    if internet_on():
        print('You have internet')
        make_reddit_post(choose_random_agency())
        print("About to sleep for 3hrs... goodnight")
        print('\n\n')
        time.sleep(10800)
        check_internet()
    else:
        while True:
            print("No internet :(, will check again in 100 seconds")
            time.sleep(100)
            check_internet()


def make_reddit_post(article):
    reddit = praw.Reddit(
        client_id=Secrets.client_id,
        client_secret=Secrets.client_secret,
        user_agent=Secrets.user_agent,
        username=Secrets.username,
        password=Secrets.password
    )
    subreddit = reddit.subreddit('watchskunthay')  # .new(limit=10)
    reddit.validate_on_submit = True

    subreddit.submit(article['title'], selftext=f'''{article['short_description']}''')


def choose_random_agency():
    # Will prioritize dem boys seh
    # see if dem boys seh title is the same as the one available
    # if not then post dem boys seh instead of news and write this title in dem boys seh file
    # if its been posted move forward as before
    # for simplicity sake i will make a new file
    try:
        seh_article = dem_boys_seh.get_latest_seh(dem_boys_seh.get_latest_link(dem_boys_seh.url1))
    except IndexError as error:
        return choose_random_agency_ext()

    if database_read_seh().val() is not None:
        # Check similar title
        print('checking Dem Boys seh titles')
        print(f'Current title - {seh_article["title"]}')
        print(f'Current title from database - {database_read_seh().val()["title"]}')
        if check_percentage.check_match_percent(seh_article["title"], database_read_seh().val()["title"]):
            print(seh_article["title"][0:50] + '--- old Dem boys seh skipped going to news')
            seh_article["title"] = ""
            return choose_random_agency_ext()
        data = {'date': firebase_db.c_t_short, 'title': seh_article["title"]}
        database_write_seh(data)
        print('Dem Boys Seh Chosen, written to database')
        return seh_article

    elif seh_article is None or seh_article["title"] == "":
        return choose_random_agency_ext()
    else:
        data = {'date': firebase_db.c_t_short, 'title': seh_article["title"]}
        database_write_seh(data)
        print('Dem Boys Seh Chosen, written to database')
        # # seh_article['short_description'].replace('<br>', '').replace('<br/>', '').replace('<p>', '').replace('</p>', '')
        #
        return seh_article


def choose_random_agency_ext():
    agency_number = random.randrange(0, 2)
    print(f'Agency select {agency_number}')
    if agency_number == 0:
        if constants.last_agency(constants.newsroom_name):
            print(f'{constants.newsroom_name} was last chosen, choosing another...')
            return villagevoice.get_villagevoice_post()
        else:
            print('Newsroom chosen')
            return newsroom.get_newsroom_post()
    elif agency_number == 1:

        if constants.last_agency(constants.villagevoice_name):
            print(f'{constants.villagevoice_name} was last chosen, choosing another...')
            return newsroom.get_newsroom_post()
        else:
            print('Village voice chosen')
            return villagevoice.get_villagevoice_post()


if __name__ == "__main__":
    check_internet()
