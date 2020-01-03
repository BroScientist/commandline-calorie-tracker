import re
import backend
import datetime

"""
the program takes 4 arguments: amount of calorie, name of food, grams of protein and date of entry (this one is automatically set as date.today()
feed in data like '300cal cereal 10g' or '50cal coffee', the 'cal' is not required
for foods that has multiple words like 'chicken breast', use 'chicken_breast' instead
"""

# TODO configure program to handle mistypes and shit
# TODO add a new table to record total daily intakes and shit

run = True
while run:

    query = input('Feed me: ')

    if query == 'quit':
        run = False
    elif query == 'history':
        backend.print_history(datetime.date.today())
    else:
        try:
            # if entry has protein
            calorie = query.split()[0]
            food = ' '.join(query.split()[1:-1])
            protein = query.split()[-1]
            calorie = int(re.search('\d+', calorie).group())
            protein = int(re.search('\d+', protein).group())
            backend.add_entry(calorie, food, protein, datetime.date.today())
        except:
            # if entry has no protein
            calorie = query.split()[0]
            food = ' '.join(query.split()[1:])
            calorie = int(re.search('\d+', calorie).group())
            backend.add_entry(calorie, food, 0, datetime.date.today())

        backend.print_daily_report(datetime.date.today())


