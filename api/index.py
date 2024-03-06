from flask import Flask, render_template, request, abort, redirect, json
from os import path
import sqlite3 as sql
import math
import schoolkitchen as shk
import datetime as dt

app = Flask(__name__)

# 좋아요, 싫어요, flask_app.py
c = path.dirname(__file__)
ip = path.join(c, 'database')

login = False
page = 0

def User_data():
    con = sql.connect(ip+'/login.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from login')

    Userdata = cur.fetchall()
    return Userdata


def notice_data():
    con = sql.connect(ip+'/notice.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from notice')

    noticedata = cur.fetchall()
    return noticedata


def update_data():
    con = sql.connect(ip+'/update.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from updated')

    updatedata = cur.fetchall()
    return updatedata
# 2022/11/06 - 댓글 추가
# 2023/3/16 - 조회수 추가


def write_data():
    con = sql.connect(ip+'/write.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from write')

    all_datas = cur.fetchall()
    return all_datas


def comments():
    con = sql.connect(ip+'/write.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from comment')

    all_comment = cur.fetchall()
    return all_comment

@app.route('/')
def start():
    global page

    all_datas = write_data()
    all_datas.reverse()

    Userdatas = User_data()
    Userdatas.reverse()

    Noticedatas = notice_data()
    Noticedatas.reverse()

    Updatedatas = update_data()
    Updatedatas.reverse()

    if not all_datas:
        all_datas = []

    lens = len(all_datas)
    page = request.args.get("page", 1, type=int)              # 페이지 값
    page = int(page)
    limit = 20                                                # 최대 글 갯수
    page_datas = all_datas[(page - 1) * limit: page * limit]  # 20개의 글 가져오기
    print(page_datas[0]["id"])
    last_page_num = math.ceil(lens / limit)                   # 마지막 페이지의 수
    block_size = 10                                           # 페이지 블럭 10개
    block_num = int((page - 1) / block_size)                  # 현재 블럭 위치 첫번째 -> 0
    block_start = (block_size * block_num) + 1                # 현재 블럭의 맨 처음 페이지 숫자
    block_end = block_start + (block_size - 1)                # 현재 블럭의 맨 끝 페이지 숫자

    return render_template('main.html',
                           page=page,
                           page_datas=page_datas,
                           last_page_num=last_page_num,
                           block_start=block_start,
                           block_end=block_end,

                           all_datas=all_datas,

                           Userdatas=Userdatas,

                           Noticedatas=Noticedatas,

                           Updatedatas=Updatedatas)


@app.route('/writing/')
def writing():
    return render_template('writing.html')


@app.route('/read/<p_id>/')
def read(p_id):

    notice = request.args.get("notice", 1, type=str)
    print(notice)

    if notice == 'false':
        global page

        all_datas = write_data()
        all_comment = comments()

        p_id = int(p_id)

        conn = sql.connect(ip+'/write.db')
        cur = conn.cursor()
        cur.execute("UPDATE write SET view = view+1 WHERE id=?", (p_id,))
        conn.commit()
        cur.close()
        conn.close()

        return render_template('read.html',
                               p_id=p_id,
                               page=page,
                               all_datas=all_datas,
                               all_comment=all_comment,

                               notice=notice)
    else:
        NoticeData = notice_data()

        now = dt.datetime.now()
        weeknum = now.weekday()
        weeklist = []

        for i in range(0-weeknum, 5-weeknum, 1):
            days = (now+dt.timedelta(days=i)).strftime('%y-%m-%d').split('-')
            weeklist.append(('20'+days[0]+days[1]+days[2]))

        VitalNoticedatas = []
        VitalNoticedatas.append(shk.findfood())
        if VitalNoticedatas[0][1][0] > 4:
            VitalNoticedatas[0][1][0] = ''
        Vitallen = len(VitalNoticedatas)

        return render_template('read.html',
                               notice=notice,
                               NoticeData=NoticeData,
                               VitalNoticedatas=VitalNoticedatas,
                               Vitallen=Vitallen,

                               weeklist=weeklist)


@app.route('/succese/', methods=['POST', 'GET'])
def succese():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            if title == '' or content == '':
                return '오류'
            else:
                with sql.connect(ip+'/write.db') as con:
                    cur = con.cursor()

                    cur.execute(
                        'INSERT INTO write (title, content, view, good) VALUES (?,?,0,0)',
                        (title, content))

                    con.commit()
                    msg = "글을 작성했습니다!"
        except:
            con.rollback()
        finally:
            return redirect('/')
            con.close()


@app.route('/comment/', methods=['POST', 'GET'])
def comment():
    if request.method == 'POST':
        try:
            comment = request.form['comment']
            write_id = request.args.get("p_id", 0, type=int)
            if comment == '':
                msg = '오류'
            else:
                with sql.connect(ip+'/write.db') as con:
                    cur = con.cursor()
                    cur.execute(
                        'INSERT INTO comment (comment, write_id) VALUES (?,?)',
                        (comment, write_id))
                    msg = '작성하였습니다!'
        except:
            msg = '오류'
        finally:
            return redirect(f'/read/{write_id}/')
            con.close()


@app.route('/login')
def login():
    return render_template('login.html')


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5000)
#     # app.run()
