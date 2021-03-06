import schedule
import time
import os
import json
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace


# login credentials
with open('credentials.json', 'r') as f:
    data = json.loads(f.read())


# path to your workspace
set_workspace(path=os.getcwd() + '/data/')


users_list = [
    'spotted_mari',
    'spottedmarinoni'
]


def job(username, password):

    session = InstaPy(
        username=username,
        password=password,
        headless_browser=False,
    )

    with smart_run(session):

        # session.set_dont_include(["friend1", "friend2", "friend3"])

        session.set_quota_supervisor(
            enabled=True,
            peak_comments_daily=20,
            peak_comments_hourly=5,
            peak_likes_daily=150,
            peak_likes_hourly=20,
            peak_follows_hourly=10,
            peak_follows_daily=50,
            sleep_after=['likes', 'follows'])

        session.set_action_delays(
            enabled=True,
            randomize=True,
            random_range_from=2,
            random_range_to=10,
        )

        session.set_relationship_bounds(
            enabled=False,
            delimit_by_numbers=True,
            max_followers=1000,
            min_followers=60,
            min_following=400
        )

        session.set_do_like(True, percentage=100)
        # session.set_dont_unfollow_active_users(True)
        session.set_do_follow(True, percentage=50)
        # session.set_do_comment(True, percentage=100)
        # session.set_comments(["hi @{}, have a look", :heart_eyes: :heart_eyes: @{}"])

        session.set_user_interact(amount=3, randomize=True, percentage=100, media='Photo')
        session.interact_user_followers(users_list, amount=20)
        session.like_by_tags(['amici', 'divertente', 'seguimi'], amount=100)


def set_schedule():
    for el in data:
        username = el.get('username')
        password = el.get('password')
        schedule.every().day.at('12:30').do(job, (username, password))
        schedule.every().day.at('17:30').do(job, (username, password))
        print(username, password)
        job(username, password)


if __name__ == '__main__':
    set_schedule()
    while True:
        schedule.run_pending()
        time.sleep(10)
