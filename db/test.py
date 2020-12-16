import repository as DB
from pprint import pprint

if __name__ == '__main__':
    user = DB.login("nam", "123456Nam")
    # date = DB.getHistory(user['user_id'])
    print(user)
    # pprint(date.strftime('%m/%d/%Y'))
    # date = DB.search_songs("what")
    # pprint(date)
    # print(DB.get_playlist_1(user['user_id'],10))



