from facebook_scraper import *  # pip install facebook-scraper
from time import sleep
import os
import csv
import threading
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)
# pip install -U lxml

def fetch_data(fbpage, filepath):

    headers = ("platform", "about", "post_id", "post_url", "post_time", "post_text", "images_lowquality","images_lowquality_desc",
               "video", "shared_post_url", "shared_page", "post_likes_count", "post_comments_count", "post_shares_count", "comment_id",
               "commenter_name", "comment_time", "comment_text")
    header = False

    try:
        print(f"Fetching data from facebook page: {fbpage} ...")
        with open(f"{filepath}/{fbpage}.csv", 'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            """ extra_info is for reactions, allow_extra_requests (True/False) in options is for HD images """
            for post_data in get_posts(fbpage, pages=3, cookies="facebook/cookies.json", extra_info=False,
                                       options={"comments": 100, "posts_per_page": 10, "HQ_images": False, "reactors": False}):
                if not header:
                    writer.writerow(headers)
                    header = True

                for comment in post_data["comments_full"]:
                    # if comment["comment_time"] < datetime.datetime(2021,11,10):
                    #     pass
                    row = ("Facebook", post_data["username"], post_data["post_id"], post_data["post_url"], post_data["time"],
                           post_data["post_text"], post_data["images_lowquality"], post_data["images_lowquality_description"],
                           post_data["video"], post_data["shared_post_url"],post_data["shared_username"], post_data["likes"],
                           post_data["comments"], post_data["shares"], comment["comment_id"], comment["commenter_name"],
                           comment["comment_time"], comment["comment_text"])
                    writer.writerow(row)
                sleep(1)
        f.close()
    except IOError:
        print("File issue")
    except exceptions.TemporarilyBanned:
        print("Temporarily Banned for approx 1 hr")
    except exceptions.InvalidCookies:
        print("Login to facebook and copy valid cookies information using a browser extension (e.g. EditThisCookie). "
              "Paste them in cookies.json under facebook folder")

def async_fetch(fbpages_list, filepath):

    for f in os.listdir(filepath):
        os.remove(os.path.join(filepath, f))

    t1 = threading.Thread(target=fetch_data, args=(fbpages_list[0],filepath))
    t2 = threading.Thread(target=fetch_data, args=(fbpages_list[1],filepath))
    t1.start()
    sleep(1)
    t2.start()
    t1.join()
    t2.join()

    csv1 = pd.read_csv(f'{filepath}/{fbpages_list[0]}.csv')
    csv2 = pd.read_csv(f'{filepath}/{fbpages_list[1]}.csv')
    frames = [csv1, csv2]
    merged = pd.concat(frames)
    merged.to_csv(f'{filepath}/{fbpages_list[0]} {fbpages_list[1]}.csv', index=False)

    for f in os.listdir(filepath):
        if f in [f'{fbpages_list[0]}.csv',f'{fbpages_list[1]}.csv']:
            os.remove(os.path.join(filepath, f))

