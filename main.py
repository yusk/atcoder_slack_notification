import datetime

import slackweb
import requests

from constants import TARGETS


def get_submissions_api_url(user_id):
    return f"https://kenkoooo.com/atcoder/atcoder-api/results?user={user_id}"


def get_problem_url(contest_id, problem_id):
    return f"https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}"


if __name__ == "__main__":
    now = datetime.datetime.now()
    for target in TARGETS:
        SLACK_WEBHOOK_URL = target["slack_webhook_url"]
        USER_IDS = target["user_ids"]
        slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)
        for user_id in USER_IDS:
            res = requests.get(get_submissions_api_url(user_id))
            messages = []
            for sub in res.json():
                contest_id = sub['contest_id']
                problem_id = sub['problem_id']
                language = sub['language']
                result = sub['result']
                submitted_at = datetime.datetime.fromtimestamp(
                    sub['epoch_second'])
                message = f"{user_id}さんが<{get_problem_url(contest_id, problem_id)}|{problem_id}>を{language}で{result}しました！"
                if result != 'AC':
                    continue
                if (now - submitted_at).days > 0:
                    continue
                messages.append(message)
            if len(messages) > 0:
                message = "\n".join(sorted(messages))
                # print(message)
                slack.notify(text=message, username="ac-ntfy", mrkdwn=False)
