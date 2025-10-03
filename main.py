import re
from datetime import datetime, timedelta, date
from random import sample


# region 1. Get days from today

def get_days_from_today(date_string: str):
    try:
        target_date = datetime.strptime(date_string, '%Y-%m-%d')  # parse date from string
        difference = datetime.today() - target_date  # get timedelta
        return difference.days  # return day delta (get from timedelta)
    except ValueError as e:  # handle value error
        return f'Value error: {e}'
    except Exception as e:  # handle common error
        return f'Unexpected error: {e}'


print('-' * 10, 'Get days from today', '-' * 10)
print(get_days_from_today('1999.02.12'))  # expect error message
print(get_days_from_today('1999-02-12'))
print(get_days_from_today('2025-10-03'))
print(get_days_from_today('2030-02-12'), '\n')


# endregion

# region 2. Get numbers tickets

def get_numbers_ticket(min: int, max: int, quantity: int):
    if min < 1 or max > 1000:
        return 'Min must be greater than or equal to 1' if min < 1 else 'Max must be less than or equal to 1000'
    elif min == max:
        return 'Min must not be equal to max'
    elif (max - min + 1) < quantity:
        return f'Can\'t get unique numbers, quantity must be less than {max - min + 1}'

    numbers_range = list(range(min, max + 1))  # generate number list (max + 1 to include max value to range)
    return sample(numbers_range, k=quantity)  # get k unique numbers from list


print('-' * 10, 'Get numbers tickets', '-' * 10)
print(get_numbers_ticket(1, 1332, 3))
print(get_numbers_ticket(1, 100, 400))
print(get_numbers_ticket(1, 100, 5))
print(get_numbers_ticket(500, 1000, 6), '\n\n')


# endregion

# region 3. Normalize phones

def normalize_phone(phone: str) -> str:
    phone = re.sub('[^\+\d]', '', phone)  # replace not numbers and not '+' with ''

    if phone.startswith('+'):
        return phone
    elif phone.startswith('38'):
        return '+' + phone
    else:
        return '+38' + phone


print('-' * 10, 'Get raw phone numbers', '-' * 10)
raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers, '\n\n')


# endregion

# region 4. Get upcoming birthdays

def is_user_to_congratulate(user: dict, today):
    seven_days_ahead = today + timedelta(days=7)
    return today <= user['next_birthday'] <= seven_days_ahead


def get_work_day_or_next_monday(bd_date):
    weekday = bd_date.weekday()
    if weekday == 5:
        return bd_date + timedelta(days=2)  # get monday date for saturday
    elif weekday == 6:
        return bd_date + timedelta(days=1)  # get monday date for sunday
    else:
        return bd_date


def get_upcoming_birthdays(users: list):
    today = datetime.today().date()
    for user in users:
        birthday = datetime.strptime(user['birthday'], '%Y.%m.%d').date()  # parse user birthday date
        # get next bd year if birthday passed
        next_birthday_year = today.year if birthday.month > today.month or (
                birthday.month == today.month and birthday.day >= today.day) else today.year + 1

        # get next date for leap/non-leap year
        if birthday.month == 2 and birthday.day == 29 and next_birthday_year % 4 != 0:
            user['next_birthday'] = date(next_birthday_year, 3, 1)
        else:
            user['next_birthday'] = birthday.replace(year=next_birthday_year)

    # filter users with upcoming bd
    users_to_congratulate = list(filter(lambda u: is_user_to_congratulate(u, today), users))
    # map users with to { name, congratulation_date }
    users_to_congratulate = list(
        map(lambda u: {'name': u['name'],
                       'congratulation_date': get_work_day_or_next_monday(u['next_birthday']).strftime('%Y.%m.%d')},
            users_to_congratulate))

    return users_to_congratulate


all_users = [
    {"name": "John Doe", "birthday": "1985.01.01"},
    {"name": "Jane Smith", "birthday": "1990.10.07"},
    {"name": "Iben Ziya", "birthday": "2000.10.09"},
    {"name": "Yusri Dosia", "birthday": "1999.05.23"},
    {"name": "Siddiqa Sawney", "birthday": "1992.12.30"},
    {"name": "Gul Farrukh", "birthday": "1990.12.28"},
    {"name": "Sabah Svetomir", "birthday": "1982.10.11"},
    {"name": "Ranjit Tricia", "birthday": "2004.02.29"}
]

print('-' * 10, 'Get upcoming birthdays', '-' * 10)
print("Список привітань на цьому тижні:")
for user in get_upcoming_birthdays(all_users):
    print(user)

# endregion
