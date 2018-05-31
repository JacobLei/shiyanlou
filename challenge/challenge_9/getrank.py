
import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    
    user_contests =[] 
    user_id_list = []
    for user in contests.find({}):
        if user['user_id'] in user_id_list:
            for d in user_contests:
                if d['user_id'] == user['user_id']:
                    d['score'] += user['score'] 
                    d['submit_time'] += user['submit_time'] 
        else:
            user_id_list.append(user['user_id'])
            d = {}
            d['user_id'] = user['user_id']
            d['score'] = user['score'] 
            d['submit_time'] = user['submit_time'] 
            user_contests.append(d)
    user_contests.sort(key=lambda k: (k.get('submit_time', 0)))
    user_contests.sort(key=lambda k: (k.get('score', 0)), reverse=True)

    if user_id in user_id_list:
        flag = 0
        for d in user_contests:
            flag = flag + 1
            if d['user_id'] == user_id:
                return flag, d['score'], d['submit_time']
    else:
        exit()

if __name__ == '__main__':

    if len(sys.argv) == 2:
        try:
            user_id = int(sys.argv[1])
        except ValueError:
            print("Parameter Error")
            exit()
    else:
        print("Parameter Error")

    userdata = get_rank(user_id)
    print(userdata)
