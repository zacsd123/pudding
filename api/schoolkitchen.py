import requests
import datetime as dt

def findfood():
    now = dt.datetime.now()

    weeknum = now.weekday()
    kitchen = []

    for i in range(0-weeknum, 5-weeknum, 1):
        days = now+dt.timedelta(days=i)
        days = days.strftime('%y-%m-%d').split('-')
        kitchen.append(food(int('20'+days[0]+days[1]+days[2])))

    meals = [[[],[],[]], []]

    for kit in kitchen:
        try:
            if kit[0]:meals[0][0].append(kit[0])
        except:
            print('can not append1')
        try:
            if kit[1]:meals[0][1].append(kit[1])
        except:
            print('can not append2')
        try:
            if kit[2]:meals[0][2].append(kit[2])
        except:
            print('can not append3')
    meals[1].append(weeknum)
    return meals

def get(url: str, args: dict = {}) -> dict:
    plus = '&'.join(map(lambda t: '='.join(
        t), zip(args.keys(), args.values())))
    if plus:
        url = url + '?' + plus
        resp = requests.get(url)
        return resp.json()
    

def food(day):
    meal = get('https://open.neis.go.kr/hub/mealServiceDietInfo', {
        'Type': 'JSON',
        'ATPT_OFCDC_SC_CODE': 'D10',
        'SD_SCHUL_CODE': '7240189',
        'MLSV_YMD': f'{day}'
    })
    L = []
    try:
        for item in meal['mealServiceDietInfo'][1]['row']:
            meals = []
            S = ''
            for meal in item['DDISH_NM'].split('<br/>'):
                bap = meal.split(' ')[0]
                if bap.startswith('*'):
                    meals.append(bap[1:])
                else:
                    meals.append(bap)
            for s in meals:
                S += s+'\n'
            L.append(S)
        days = ['아침밥', '점심밥', '저녁밥']
        foods=[]
        for data in L:
            foods.append(data.split('\n'))
        for i in range(len(foods)):
            if type(i) is not str:
                foods[i].insert(0, days[i])
                if '' in foods[i]: foods[i].pop(-1)
        return foods
    except:
        return [" "]