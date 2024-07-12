import requests
import os, re, random
from FBTools import Start

domain = lambda patch=None: 'https://mbasic.facebook.com/' if patch is None else 'https://mbasic.facebook.com/' + str(patch)
get_name = lambda session, uid: re.search(r'title>(.*?)</', session.get(domain(uid)).text).group(1)

class MassAdd:
    def __init__(self, session, fb):
        self.session = session

        if fb.IsValid: [print('Success send request to'+ name) if fb.AddFriend(id)['status'] else print('Failure send request to '+ name) for id, name in self.scrape_user()]
        else: print('Please check your cookies.')

    def scrape_user(self):
        mbasic_src = self.session.get(domain('friends/center/mbasic')).text
        return [(id, get_name(self.session, id)) for id in list(set(re.findall(r'uid=(.*?)\&', mbasic_src)))]

class MassReact:
    def __init__(self, session, fb):
        self.session = session

        if fb.IsValid: [print(fb.ReactToPost(post=pid, react=random.choice([2,4,5,6,7]))) for pid in self.scrape_user()]
        else: print('Please check your cookies.')

    def scrape_user(self):
        mbasic_src = self.session.get(domain()).text
        return [id for id in re.findall(r'shared_from_post_id=(.*?)\&', mbasic_src) if not ('Anda dan' in (mbasic_src := self.session.get(domain(id)).text) or get_name(self.session, 'me') in mbasic_src)]


cookie = os.getenv('cookie')
with requests.session() as ses:
    ses.cookies['cookie'] = cookie
    fb = Start(cookie)

    MassAdd(ses, fb)
    MassReact(ses, fb)
