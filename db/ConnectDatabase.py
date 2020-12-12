import pymysql.cursors
#config thong tin ket noi database trong file nay
def getConnection():
    connection = pymysql.connect(host='34.123.234.51',
                                 user='teamlang',
                                 password='123456_Lang',
                                 db='project_ai_db' ,
                                 charset= 'utf8mb4' ,
                                 cursorclass= pymysql.cursors.DictCursor)
    return connection

