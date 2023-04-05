import datetime
import json
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
from locustio.jira.requests_params import jira_datasets
import random

logger = init_logger(app_type='jira')

PAGE_ENDPOINT = "/rest/simplewiki/latest/page"

@jira_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')
def app_specific_action(locust):
    jira_dataset = jira_datasets()

    projects = jira_dataset['projects']
    project = random.choice(projects)
    project_id = project[1]

    get_hashed_timestamp = lambda: hash(datetime.datetime.today().timestamp())

    key = f"page{get_hashed_timestamp()}"
    page = {
        "key": key,
        "permissions": [],
        "project": {
            "id": project_id
        },
        "title": key,
        "type": "STANDARD",
    }

    # Create page
    r = locust.post(PAGE_ENDPOINT, json=page, catch_response=True)
    assert r.status_code == 200

    content = json.loads(r.content.decode('utf-8'))
    page_id = content["id"]

    # View
    r = locust.get(PAGE_ENDPOINT + f'?pageId={page_id}', catch_response=True)
    assert r.status_code == 200

    # Edit
    payload = {
        "id": page_id,
        "title": get_hashed_timestamp(),
        "type": "STANDARD"
    }
    r = locust.put(PAGE_ENDPOINT, json=payload, catch_response=True)
    assert r.status_code == 200

    # Delete
    r = locust.delete(PAGE_ENDPOINT + f'/{page_id}', catch_response=True)
    assert r.status_code == 200

    content = json.loads(r.content.decode('utf-8'))
    assert content["success"]
