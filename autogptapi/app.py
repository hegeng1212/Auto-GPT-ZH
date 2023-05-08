""" Command and Control """

from flask import Flask, request
import subprocess
import json
import autogptapi.command

app = Flask(__name__)

@app.route('/autogpt', methods=['GET', 'POST'])
def run_autogpt():
    # 获取请求的 URL 和数据
    url = request.url
    session_id = request.args.get('session_id').strip()
    ai_goal = request.args.get('ai_goal').strip()

    err_msg = ""
    status = "success"
    if session_id == "":
        err_msg = "session_id不存在"
        status = "failed"
    elif ai_goal == "":
        err_msg = "ai_goal不存在"
        status = "failed"

    if status=="success":
        autogptapi.command.async_autogpt(session_id, ai_goal)

    # 返回响应
    return get_response(err_msg, status)

def get_response(msg:str, status:str):
    response_data = {
        'message': msg,
        'status': status
    }
    response_json = json.dumps(response_data)
    response = app.make_response(response_json)
    response.headers['Content-Type'] = 'application/json'
    return response

def run_cli(session_id:str, ai_goal:str):
    # 执行 autogpt 命令并指定session_id和目标
    subprocess.run([
        'python',
        '-m',
        'autogpt',
        '--gpt3only',
        '--session-id=' + session_id,
        '-c',
        '--continuous-limit=4',
        '--ai-goal=' + ai_goal,
    ])

def main()->None:
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()
