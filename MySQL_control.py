import pymysql

# db = None
# try:
#     db = pymysql.connect(
#         host='127.0.0.1',
#         user='root',
#         passwd='1234',
#         db='test',
#         charset='utf8'
#     )
#
#     sql = '''
#     CREATE TABLE tb_student (
#         id int primary key auto_increment not null,
#         name varchar(32),
#         age int,
#         address varchar(32)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8
#     '''
#
#     with db.cursor() as cursor:
#         cursor.execute(sql)
#
# except Exception as e:
#     print(e)
#
# finally:
#     if db is not None:
#         db.close()

db = None
try:
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='1234',
        db='test',
        charset='utf8'
    )

    # sql = '''
    #     INSERT tb_student(name, age, address) values('Kei', 35, 'Korea')
    # '''

    # id = 1
    # sql = '''
    #     UPDATE tb_student set name='케이', age=36 where id=%d
    # ''' % id

    id = 1
    sql = '''
        DELETE from tb_student where id=%d
    ''' % id

    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()