import repository as DB
from pprint import pprint

if __name__ == '__main__':
    user = DB.login("nam", "123456Nam")
    date = DB.getHistory(user['user_id'])[0]['add_date']
    # pprint(date.strftime('%m/%d/%Y'))
    pprint(DB.getHistory(user['user_id']))