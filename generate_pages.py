import random
import datetime
import requests

CREATE_PAGE_ENDPOINT = "http://localhost:2990/jira/rest/simplewiki/latest/page"
PROJECTS = [10000, 10001, 10002]
COUNT_PAGES = 1

with requests.session() as s:
    s.auth = ("admin", "admin")
    for _ in range(COUNT_PAGES):
        project = random.choice(PROJECTS)
        hashed_timestamp = hash(datetime.datetime.today().timestamp())
        page = {
            "key": f"page{hashed_timestamp}",
            "permissions": [],
            "project": {
                "id": project
            },
            "title": f"page{hashed_timestamp}",
            "type": "STANDARD",
        }
        response = s.post(CREATE_PAGE_ENDPOINT, json=page)
        if not response.ok:
            print(response.content)
