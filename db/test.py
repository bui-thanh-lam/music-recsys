import repository as DB
from pprint import pprint

if __name__ == '__main__':
    user = DB.login("nam", "123456Nam")
    pprint(user)