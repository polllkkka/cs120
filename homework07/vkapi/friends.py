import dataclasses
import math
import time
import typing as tp

from homework07.vkapi import session
from homework07.vkapi.config import VK_CONFIG

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    response = session.get(
        "friends.get",
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        access_token=VK_CONFIG["access_token"],
        v=VK_CONFIG["version"],
    )
    try:
        data = response.json()
        count = data["response"]["count"]
        items = data["response"]["items"]
        return FriendsResponse(count=count, items=items)
    except (KeyError, TypeError):
        return FriendsResponse(count=0, items=[])  # type:ignore


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def _get_mutual_list_from_api(session, query_params) -> tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]:
    mutual_list = []
    for _ in range(query_params["requests_count"]):
        response = session.get(
            "friends.getMutual",
            source_uid=query_params["source_uid"],
            target_uid=query_params["target_uid"],
            target_uids=",".join(str(uid) for uid in query_params["target_uids"])
            if query_params["target_uids"]
            else None,
            order=query_params["order"],
            count=query_params["count"],
            offset=query_params["offset"],
            v="5.131",
            access_token=VK_CONFIG["access_token"],
        )
        if response.status_code == 200:
            response_data = response.json()["response"]
            mutual_list.extend(response_data)
        query_params["offset"] += 100
        time.sleep(1)

    return mutual_list


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    query_params = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
        "requests_count": 1,
    }
    if target_uids is not None:
        t = VK_CONFIG["target_limit"]
        assert isinstance(t, int)
        query_params["requests_count"] = math.ceil(len(target_uids) / t)
    mutual_list = _get_mutual_list_from_api(session, query_params)
    try:
        mutual_friends_list = [MutualFriends(**item) for item in mutual_list]  # type:ignore
    except TypeError:
        return mutual_list  # type:ignore

    return mutual_friends_list

if __name__ == "__main__":
    user_id = 570320117

    session.params = {  # type:ignore
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
    }

    friends_response = get_friends(user_id=user_id, fields=["nickname"])
    if friends_response.count > 0:
        friends_list = friends_response.items
        print(f"User ID: {user_id}")
        print("Friends:")
        for friend in friends_list:
            print(friend)
    mutual_friends = get_mutual(source_uid=user_id, target_uid=user_id, count=len(friends_list))
    print(len(mutual_friends))
    print(mutual_friends)