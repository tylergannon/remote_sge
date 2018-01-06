from os.path import dirname, abspath, join
import string
import pytest
import sge.shell
import sge.status

@pytest.fixture
def job_details():
    return dict(JOB_ID=12345, USER='tyler', JOB_NAME='quux',
                ENVVAR='bazvar', ENVVAL='213423', SCRIPT_PATH='/path/to/script.sh')
    

@pytest.fixture
def job_detail_xml(job_details):
    fixtures_path = join(dirname(abspath(__file__)), 'fixtures')
    detail_xml = open(join(fixtures_path, 'job_detail.xml'), 'r').read()
    template = string.Template(detail_xml)
    return template.substitute(**job_details)

def test_job_detail(job_detail_xml, job_details, mocker):
    mocker.patch('sge.shell.run')
    sge.shell.run.return_value = job_detail_xml
    job_detail = sge.status.get_job_detail(job_details['JOB_ID'])

    assert job_detail.gid == 500
    assert job_detail.uid == 500
    assert job_detail.command_path == job_details['SCRIPT_PATH']
    assert job_detail.owner == job_details['USER']
    assert job_detail.job_name == job_details['JOB_NAME']
    assert job_detail.job_environment[job_details['ENVVAR']] == job_details['ENVVAL']
    assert job_detail.job_arguments == ['50000']
