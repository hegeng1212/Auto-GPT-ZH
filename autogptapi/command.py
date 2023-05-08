import asyncio

async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    return (stdout.decode().strip(), stderr.decode().strip(), process.returncode)

async def autogpt(session_id: str, ai_goal: str):
    await run_command("python -m autogpt --gpt3only --session-id="+session_id+" -c --continuous-limit=4 --ai-goal="+ai_goal)


def async_autogpt(session_id: str, ai_goal: str):
    asyncio.run(autogpt(session_id, ai_goal))

