import datetime
date_entry = '2018-6-04'
year, month, day = map(int, date_entry.split('-'))
required = datetime.date(year, month, day)
today = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
print(str(today.date()) + ' today')
after_five = today + datetime.timedelta(days=4)
print(str(after_five.date()) + ' after five days')
print(str(required) + ' required')
if after_five.date() < required or today.date() > required:
    print('False')
else:
    print('True')

