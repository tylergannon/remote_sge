from collections import OrderedDict
import json
import falcon
from falcon import testing
import pytest

def test_root(client):
    # print(help(client.get("/")))
    response = client.simulate_get("/")
    json_obj = response.json
    assert response.status == falcon.HTTP_OK
    print(response.text)
    assert json_obj['application'] == "Remote SGE"


@pytest.fixture
def job_detail(job_package_str):
    return dict(arguments=['blaz', 'forks'],
                command='sleeper.sh',
                environment=OrderedDict(bazvar='213423', TERM=None),
                name='quux',
                package=job_package_str)

def test_post_basic_job(client, job_detail):
    response = client.simulate_post("/jobs", body=json.dumps(job_detail))
    assert response.status == falcon.HTTP_CREATED
