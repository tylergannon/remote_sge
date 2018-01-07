from os.path import dirname, abspath, join
import string
import pytest
import sge.shell
import sge.status
from json import dumps

@pytest.fixture
def job_detail_dict():
    return dict(JOB_ID=12345, USER='tyler', JOB_NAME='quux',
                ENVVAR='bazvar', ENVVAL='213423', SCRIPT_PATH='/path/to/script.sh')
    

@pytest.fixture
def job_detail_xml(job_detail_dict):
    fixtures_path = join(dirname(abspath(__file__)), 'fixtures')
    detail_xml = open(join(fixtures_path, 'job_detail.xml'), 'r').read()
    template = string.Template(detail_xml)
    return template.substitute(**job_detail_dict)

@pytest.fixture
def job_detail_object(job_detail_xml, job_detail_dict, mocker):
    mocker.patch('sge.shell.run')
    sge.shell.run.return_value = job_detail_xml
    return sge.status.get_job_detail(job_detail_dict['JOB_ID'])

def test_job_detail_renders_dictionary(job_detail_object):
    "Verify that the JobDetail object is able to render a dictionary to be made into JSON"
    diction = job_detail_object.to_dict()
    assert type(diction) is dict
    assert diction['command_path'] == job_detail_object.command_path
    assert diction['owner'] == job_detail_object.owner
    assert diction['job_name'] == job_detail_object.job_name
    assert diction['arguments'] == job_detail_object.arguments
    assert diction['environment'] == job_detail_object.environment
    assert diction['job_id'] == job_detail_object.job_id
    assert diction['gid'] == 500
    assert diction['uid'] == 500

def test_job_detail_has_correct_attributes(job_detail_object, job_detail_dict):
    assert job_detail_object.gid == 500
    assert job_detail_object.uid == 500
    assert job_detail_object.job_id == job_detail_dict['JOB_ID']
    assert job_detail_object.command_path == job_detail_dict['SCRIPT_PATH']
    assert job_detail_object.owner == job_detail_dict['USER']
    assert job_detail_object.job_name == job_detail_dict['JOB_NAME']
    assert job_detail_object.environment[job_detail_dict['ENVVAR']] == job_detail_dict['ENVVAL']
    assert job_detail_object.arguments == ['50000']

