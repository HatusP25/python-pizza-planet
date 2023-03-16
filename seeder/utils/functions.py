import random
from typing import Any
from datetime import datetime, timedelta


def pick_random_list(curr_list: list) -> Any:
    return random.choice(curr_list)


def pick_many_random_list(curr_list: list) -> list:
    number = random.randint(1, len(curr_list))
    return random.sample(curr_list, number)


def pick_random_dict(curr_dict: dict) -> Any:
    return random.choice(list(curr_dict.values()))


def get_random_price() -> float:
    return round(random.uniform(1, 10), 2)


def get_random_date() -> datetime:
    initial_date = datetime(2022, 1, 1)
    final_date = datetime(2022, 12, 31)
    delta = final_date - initial_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return initial_date + timedelta(seconds=random_second)
