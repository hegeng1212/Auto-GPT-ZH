import requests
import json
from autogpt.logs import logger
from autogpt.config import Config
from autogpt.llm_utils import create_chat_completion

cfg = Config()

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


def get_daily_report(session_id, date) -> str:
    url = "http://bsp.babytree.com/open/dingtalk/GetDailyReport"
    data = {
        "session_id": session_id,
        "date": date,
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
        if res_data["data"] == "" or res_data["data"]["data"] == "":
            # 钉钉消息
            logger.dingtalk_log(
                session_id,
                "指定时间没有日报，请更改时间",
            )
            print("指定时间没有日报，请更改时间\n" + f"时间：{date}\n")
            return {}

        prompt = get_report_prompt(res_data["data"]["data"], date)
        model = cfg.fast_llm_model
        current_context = [
            create_chat_message("system", prompt),
            create_chat_message("user", "请按上述要求，输出日报内容："),
        ]

        assistant_reply = create_chat_completion(
            model=model,
            messages=current_context,
            session_id=session_id,
        )

        # 钉钉消息
        logger.dingtalk_log(
            session_id,
            assistant_reply,
        )
        print("日报查询成功\n" + assistant_reply)
        return "日报查询成功"
    else:
        # 钉钉消息
        logger.dingtalk_log(
            session_id,
            "日报查询失败",
            res_data["msg"],
        )
        print("日报查询失败\n" + res_data["msg"])
        return "日报查询失败"

def get_report_prompt(daily, date) -> str:
    prompt = "你是一个智能助理，帮助撰写工作日报。\n"
    prompt += "下面是"+date+"日工作日报内容：\n"
    prompt += daily + "\n\n"
    prompt += """
约束：
    1.姓名只能出现在"参与人"，其他部分不要出现
    2.对工作内容进行提炼和总结，突出重点，相似的事项请合并，不能出现用户姓名
    3.按项目聚合，相同项目的内容，参与人等信息请合并
    4.进度只显示一个项目整体百分比，不能显示百分比时，显示"进行中"
    5.通过对工作内容进行分析，把风险相关的事项，在"风险"部分汇报
    6.通过对工作内容进行分析，给出一些对工作有益的建议
    7.在项目名称相同的情况下，请明确区分不同的参与人和工作内容，避免混淆。

每个项目按照下面格式进行输出：

    项目：
        工作内容：
          - 
    参与人：
    进度：
    风险：
    建议：
"""
    return prompt

def create_chat_message(role, content):
    """
    Create a chat message with the given role and content.

    Args:
    role (str): The role of the message sender, e.g., "system", "user", or "assistant".
    content (str): The content of the message.

    Returns:
    dict: A dictionary containing the role and content of the message.
    """
    return {"role": role, "content": content}