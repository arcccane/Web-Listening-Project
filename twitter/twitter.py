import csv
import os
import snscrape.modules.twitter as sntwitter
from snscrape.modules.twitter import Photo, Video, Gif


def formatMedia(listOfMediaObjects):
    if isinstance(listOfMediaObjects, list):
        photos = []
        media_dict = {}
        for mediaObject in listOfMediaObjects:
            if isinstance(mediaObject, Photo):
                photos.append(mediaObject.fullUrl)
                media_dict["photo"] = photos
            elif isinstance(mediaObject, (Video,Gif)):
                media_dict["thumbnail"] = mediaObject.thumbnailUrl
                media_dict["video"] = mediaObject.variants[0].url
        return media_dict
    return ""

def fetch_data(keywords_list, filepath, before, limit):

    file = ' '.join(keywords_list)
    headers = ["platform","about","id", "url", "about", "date", "username", "content", "hashtages", "lang", "likeCount", "replyCount",
               "retweetCount", "quoteCount", "quotedTweet", "links", "media", "place", "coordinates", "sourceLabel"]
    header = False
    limit_each = int(limit/2)

    """ Arguments to filter search """
    min_likes = 500
    # since_date =
    until_date = before

    try:
        for f in os.listdir(filepath):
            os.remove(os.path.join(filepath, f))

        for keyword in keywords_list:

            """ Search query to filter out results (use adv_query to filter more) """
            # search_query = f'{keyword} lang:en'
            search_query2 = f'{keyword} lang:en min_faves:{min_likes} until:{until_date}'

            with open(f'{filepath}/{file}.csv', 'a', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not header:
                    writer.writerow(headers)
                    header = True

                print(f"Fetching data from twitter keyword: {keyword} ...")
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query2).get_items()):
                    if i > limit_each:
                        break
                    writer.writerow(("Twitter", keyword, tweet.id, tweet.url, tweet.content, tweet.date,
                                     tweet.user.username, tweet.content, tweet.hashtags, tweet.lang,
                                     tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.quoteCount,
                                     tweet.quotedTweet, tweet.outlinks, formatMedia(tweet.media), tweet.place,
                                     tweet.coordinates, tweet.sourceLabel))
    except IOError:
        print("File issue")

