"""
These tests express the 
"""
from os.path import dirname, abspath, join
import string
import pytest
import pytest_mock
from pytest_bdd import scenario, given, when, then, parsers

import sge
from sge.status import SgeJobStateCode
import sge_client.shuttle

STATES = dict(queued=SgeJobStateCode.QUEUED_ACTIVE,
              hold=SgeJobStateCode.QUEUED_HELD)

@scenario("package_job.feature", "Packaging a queued job")
def test_package():
    pass

@given(parsers.parse(r"Job id {job_id:d} is {initial_state} locally"))
def local_queued_job(mocker, job_id, initial_state, job_detail_xml):
    "Stubs out the job_status and job_detail functions"
    mocker.patch('sge.status.get_job_status')
    sge.status.get_job_status.return_value = STATES[initial_state]

@when("I request it to be shuttled")
def request_shuttle(job_id, initial_state, mocker):
    if initial_state == 'queued':
        mocker.patch('sge.control.user_hold')
    sge_client.shuttle.send_job_to_remote(job_id)


@then(parsers.parse(r"It should be placed on hold"))
def local_job_should_be_placed_on_hold(job_id):
    sge.control.user_hold.assert_called_once_with(job_id)

@then("a job manifest should be created")
def job_manifest_should_be_created():
    # Preparing to send the job over, it needs to collect
    # The job details
    pass

@pytest.fixture
def job_detail_xml(job_id):
    fixtures_path = join(dirname(abspath(__file__)), 'fixtures')
    detail_xml = open(join(fixtures_path, 'qstat_detail.xml'), 'r').read()
    script_path = join(fixtures_path, 'sleeper.sh')
    template_vars = dict(JOB_ID=job_id, USER='tyler', JOB_NAME='quux',
                         ENVVAR='bazvar', ENVVAL='213423', SCRIPT_PATH=script_path)
    template = string.Template(detail_xml)
    return template.substitute(**template_vars)

    
    # Then Local job 34567 should be queued
    # When I request job id 34567 to be shuttled
    # And A request should be sent to the remote server
    # And It should include the arguments given to the local command
    # And It should include the command name
    # And It should include the command file itself
    