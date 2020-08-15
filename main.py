import os
import datetime

from dotenv import load_dotenv
import slackweb
import requests

load_dotenv('.env')

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
USER_IDS = os.environ.get("USER_IDS").split(",")
slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)


def get_submissions_api_url(user_id):
    return f"https://kenkoooo.com/atcoder/atcoder-api/results?user={user_id}"


def get_problem_url(contest_id, problem_id):
    return f"https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}"


if __name__ == "__main__":
    now = datetime.datetime.now()
    for user_id in USER_IDS:
        res = requests.get(get_submissions_api_url(user_id))
        messages = []
        for sub in res.json():
            contest_id = sub['contest_id']
            problem_id = sub['problem_id']
            language = sub['language']
            result = sub['result']
            submitted_at = datetime.datetime.fromtimestamp(sub['epoch_second'])
            message = f"{user_id}さんが<{get_problem_url(contest_id, problem_id)}|{problem_id}>を{language}で{result}しました！"
            if result != 'AC':
                continue
            if (now - submitted_at).days > 0:
                continue
            messages.append(message)
        if len(message) > 0:
            message = "\n".join(sorted(messages))
            slack.notify(text=message, username="ac-ntfy", mrkdwn=False)
