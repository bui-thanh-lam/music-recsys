import pymysql.cursors
#config thong tin ket noi database trong file nay
def getConnection():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='Nam123456Nam',
                                 db='project_ai_db' ,
                                 charset= 'utf8mb4' ,
                                 cursorclass= pymysql.cursors.DictCursor)
    return connection
