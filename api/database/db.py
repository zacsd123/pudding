import sqlite3 as sql
import os

C = os.path.dirname(__file__)
ip = C
print(C)
id = os.path.join(C, 'database')
print(id)
conn = sql.connect(f'{C}/write.db')
print('생성')

conn.execute(
    '''
    create table write (id integer primary key, title text, content text, view integer, good integer)
    '''
)
conn.execute(
    '''
    create table comment (id integer primary key, comment text, write_id integer, writerName text)
    '''
)
conn = sql.connect(f'{C}/login.db')

conn.execute(
    '''
    create table login (id integer primary key, Userid text, password integer, Email text)
    '''
)

conn = sql.connect(f'{C}/notice.db')

conn.execute(
    '''
    create table notice (id integer primary key, notice text, NoticeContent text, important integer)
    '''
)

conn = sql.connect(f'{C}/update.db')

conn.execute(
    '''
    create table updated (id integer primary key, Updated text, Updatecontent text)
    '''
)
print('생성')

conn.close()

with sql.connect(ip+'/write.db') as con:
    cur = con.cursor()
    for title in range(5000):
        cur.execute(
            'INSERT INTO write (title, content, view, good) VALUES (?,?,0,0)',
            (title, 'content'))
    print('end')
    con.commit()

with sql.connect(ip+'/notice.db') as con:
    cur = con.cursor()
    cur.execute(
        'INSERT INTO notice (notice, NoticeContent, important) VALUES (?,?,1)',
        ('이번 주 급식', ''))
    print('end')
    con.commit()