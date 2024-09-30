import datetime as dt
import statistics
import typing as tp

from homework07.vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends_list = get_friends(user_id, fields=["bdate"])
    date_list = [friend.get("bdate", None) for friend in friends_list.items if isinstance(friend, dict)]

    friends_ages = []
    for d in date_list:
        try:
            date_of_birth = dt.datetime.strptime(d.replace(".", ""), r"%d%m%Y").date()
        except (ValueError, AttributeError):
            continue
        else:
            age = (dt.datetime.now().date() - date_of_birth).days // 365
            friends_ages.append(age)

    if friends_ages:
        median_friends_age = statistics.median(friends_ages)
        return median_friends_age
    else:
        return None

if __name__ == "__main__":
    print(age_predict(user_id=570320117))