
"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
user = api.get_user('Pixel_Dailies')
stuff = api.user_timeline(screen_name = 'Pixel_Dailies', count = 100)
for status in stuff:
    if "Today's theme is" in status.text:
        print status.text, status.created_at
        pd = Pixel_Dailies(status.text, status.created_at)
print user.screen_name
print user.followers_count

class Pixel_Dailies:
    def __init__(theme, date):
        self.theme = theme
        self.date = date
"""
import tweepy
from tweepy import OAuthHandler
import json, re, urllib2, os, errno, logging

logging.basicConfig(filename='pixel-dailies-consumer.log',level=logging.ERROR)

consumer_key    = "PrrQg43wK6Y1PssoBhFdGnNad"
consumer_secret = "6qinO24giQtayuypLiME0zUPHqf6lO0QCfR8esHGtP12coSOgb"
access_token    = "965318088840265729-xKcijExiSem64VWC5cM8P7YsVabixp7"
access_secret   = "7zmkvuBu6afRr2tNVymaxHB7Fk7JCuH0zSycUM5U1l7EH"

theme_pat = "Today's theme is #(?P<theme>\w+), "
theme_rex = re.compile(theme_pat)
theme_folder = 'themes'
if not os.path.exists(theme_folder):
    try:
        os.makedirs(theme_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

class Pixel_Dailies:

    def __init__(self, theme, date):
        self.theme = theme.capitalize()
        self.date = date
        self.media = []
        self.theme_folder = 'themes'
        if not os.path.exists(self.theme_folder):
            try:
                os.makedirs(self.theme_folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        if not os.path.exists(self.theme_folder + "/" + self.theme):
            try:
                os.makedirs(self.theme_folder + "/" + self.theme)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def setMedia(self, newMedia):
        self.media = newMedia

    def getMedia(self):
        return self.media

    def addMedia(self, newMedia):
        seld.media.append(newMedia)

    def popMedia(self):
        return self.media.pop()

    def downloadMedia(self, logfile='file.txt'):
        for pd in self.media:
            try:
                f, extension = os.path.splitext(pd.url)
                filename = self.theme_folder + "/" + str(self.theme).capitalize() + "/" + str(self.theme).lower() + "_" + str(pd.userid) + extension
                if not os.path.isfile(filename):
                    response = urllib2.urlopen(pd.url)
                    html = response.read()
                    with open(filename, "wb") as handle:
                        handle.write(html)
            except OSError as e:
                logging.error(e.message)
                if e.errno != errno.EEXIST:
                    raise

class PixelMedia:
    def __init__(self, userid, caption, url):
        self.userid = userid
        self.caption = caption
        self.url = url

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
tweets = api.user_timeline(screen_name='Pixel_Dailies',
                           count=200, include_rts=True,
                           exclude_replies=True)

last_id = tweets[-1].id

while (True):
    more_tweets = api.user_timeline(screen_name='Pixel_Dailies',
                                count=200,
                                include_rts=True,
                                exclude_replies=True,
                                max_id=last_id-1)
    # There are no more tweets
    if (len(more_tweets) == 0):
          break
    else:
          last_id = more_tweets[-1].id-1
          tweets = tweets + more_tweets

pixel_dailies = []
theme_media_list = []
for status in tweets:
    media = status.entities.get('media', [])
    if "Today's theme is" in status.text:
        try:
            theme_match = theme_rex.match(status.text).group('theme')
            pd = Pixel_Dailies(theme_match, status.created_at)
            pd.setMedia(theme_media_list)
            pd.downloadMedia()
        except (OSError, KeyError, AttributeError, TypeError) as e:
            logging.error(str(e.message))
            pass
        except:
            pass
        theme_media_list = []
    if(len(media) > 0):
        try:
            theme_media_list.append(PixelMedia(media[0]['source_user_id'], status.text, media[0]['media_url']))
        except KeyError as e:
            logging.error("KeyError: "+e.message)
