import datetime as dt
import schoolkitchen as sh

def findfood():
    now = dt.datetime.now()

    weeknum = now.weekday()
    weeklist = []

    for i in range(0-weeknum, 5-weeknum, 1):
        days = now+dt.timedelta(days=i)
        days = days.strftime('%y-%m-%d').split('-')
        weeklist.append(int('20'+days[0]+days[1]+days[2]))

    kitchen = []
    meals = [[],[],[]]
    for day in weeklist:
        kitchen.append(sh.food(day))
    for kit in kitchen:
        try:
            if kit[0]:meals[0].append(kit[0])
        except:
            print('can not append1')
        try:
            if kit[1]:meals[1].append(kit[1])
        except:
            print('can not append2')
        try:
            if kit[2]:meals[2].append(kit[2])
        except:
            print('can not append3')
    return meals