import datetime

import requests
import slackweb

from constants import TARGETS


def get_submissions_api_url(user_id):
    return f"https://kenkoooo.com/atcoder/atcoder-api/results?user={user_id}"


def get_problem_url(contest_id, problem_id):
    return f"https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}"


if __name__ == "__main__":
    now = datetime.datetime.now()
    for target in TARGETS:
        slack_webhook_url = target["slack_webhook_url"]
        USER_IDS = target["user_ids"]
        # slack_webhook_url = "https://hooks.slack.com/services/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"
        print(slack_webhook_url)
        res = requests.post(slack_webhook_url, json={"text": "test"})
        print(res)
        print(res.text)
