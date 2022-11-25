import os
import random
import string
import json
import requests

from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
from locustio.jira.requests_params import jira_datasets
from PIL import Image

logger = init_logger(app_type='jira')

generate_random_string = lambda size: ''.join(random.choice(string.ascii_letters) for _ in range(size))

def _create_and_save_img(size: int):
    img = Image.new(mode='RGB', size=(size, size), color='red')
    base_path = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    img_path = os.path.join(base_path, generate_random_string(10) + '.jpg')
    img.save(img_path)

    return img, img_path

@jira_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')
def app_specific_action(locust):
    jira_dataset = jira_datasets()

    projects = jira_dataset['projects']
    project = random.choice(projects)
    project_key = project[0]

    locust.get('/rest/s3/1.0/api/settings/NOPREFIX?effective=true', catch_response=True)
    locust.get('/rest/s3/1.0/api/bucket/effective/NOPREFIX', catch_response=True)

    img, img_path = _create_and_save_img(64)
    img_name = os.path.basename(img_path)
    img_size = os.stat(img_path).st_size

    r = locust.get(
        '/rest/s3/1.0/s3/multipartUpload?'
        f'projectKey={project_key}'
        f'&targetPath={img_name}'
        f'&fileSize={img_size}',
        catch_response=True
    )

    assert r.status_code == 200

    content = json.loads(r.content.decode('utf-8'))
    upload_url = content['multiPartUploadParts'][0]
    r = requests.put(upload_url, files={'photo': img.tobytes()})

    assert r.status_code == 200

    etag = r.headers.get('ETag')

    complete_url = content['completeMultiPartUploadUrl']
    r = requests.post(
        complete_url,
        data='<CompleteMultipartUpload>'
             '<Part>'
             '<PartNumber>1</PartNumber>'
             f'<ETag>"{etag}"</ETag>'
             '</Part>'
             '</CompleteMultipartUpload>'
    )

    assert r.status_code == 200

    r = locust.get(f'/rest/s3/1.0/s3/listObject?projectKey={project_key}', catch_response=True)
    content = json.loads(r.content.decode("utf-8"))
    img_obj = [obj for obj in content if obj['path'] == img_name][0]

    assert img_obj

    new_img_name = generate_random_string(10)

    r = locust.post(
        '/rest/s3/1.0/s3/MoveObject?'
        f'projectKey={project_key}'
        f'&pathFrom={img_name}'
        f'&pathTo={new_img_name}',
        catch_response=True
    )

    assert r.status_code == 200

    r = locust.post(
        '/rest/s3/1.0/s3/DeleteObject?'
        f'projectKey={project_key}'
        f'&path={new_img_name}',
        catch_response=True
    )

    assert r.status_code == 200
