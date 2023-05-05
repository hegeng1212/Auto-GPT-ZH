import requests
import json
from autogpt.logs import logger

def reserve_meeting_room(session_id, room_name, start_time, end_time):
    url = "http://bsp.babytree.com/open/dingtalk/ReserveMeetingRoom"
    data = {
        "session_id": session_id,
        "room_name": room_name,
        "start_time": start_time,
        "end_time": end_time,
    }

    try:
        response = requests.get(url, params=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print("error:\n"+error)
    except requests.exceptions.RequestException as error:
        print("error:\n" + error)

    res_data = json.loads(json.dumps(response.json()))
    if res_data["code"] == 200:
        # 钉钉消息
        logger.dingtalk_log(
            session_id,
            "会议室预定成功",
            f"会议室：{room_name}\n"
            + f"开始时间：{start_time}\n"
            + f"结束时间：{end_time}",
        )
        print("会议室预定成功\n" + f"会议室：{room_name}\n" + f"开始时间：{start_time}\n" + f"结束时间：{end_time}\n")
    else:
        # 钉钉消息
        logger.dingtalk_log(
            session_id,
            "会议室预定失败",
            res_data["msg"],
        )
        print("会议室预定失败\n" + res_data["msg"])

def search_meeting_room(session_id, start_time, end_time) -> list[str]:
    url = "http://bsp.babytree.com/open/dingtalk/SearchMeetingRoom"
    data = {
        "session_id": session_id,
        "start_time": start_time,
        "end_time": end_time,
    }
    try:
        response = requests.get(url, params=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print("error:\n"+error)
    except requests.exceptions.RequestException as error:
        print("error:\n" + error)

    res_data = json.loads(json.dumps(response.json()))
    if res_data["code"] == 200:
        if "room_name" not in res_data["data"]:
            # 钉钉消息
            logger.dingtalk_log(
                session_id,
                "下列时间段没有空闲的会议室，请更改时间",
                f"开始时间：{start_time}\n"
                + f"结束时间：{end_time}",
            )
            print("下列时间段没有空闲的会议室，请更改时间\n" + f"开始时间：{start_time}\n" + f"结束时间：{end_time}\n")
            return {}

        # 钉钉消息
        logger.dingtalk_log(
            session_id,
            "会议室查询成功",
            f"会议室：" + res_data["data"]["room_name"] + "\n"
            + f"开始时间：{start_time}\n"
            + f"结束时间：{end_time}",
        )
        print("会议室查询成功\n" + f"会议室：" + res_data["data"]["room_name"] + "\n" + f"开始时间：{start_time}\n" + f"结束时间：{end_time}\n")
        return res_data["data"]
    else:
        # 钉钉消息
        logger.dingtalk_log(
            session_id,
            "会议室查询失败",
            res_data["msg"],
        )
        print("会议室查询失败\n" + res_data["msg"])
        return {}
