"""
These tests express the
"""
from collections import OrderedDict
import os
from os.path import dirname, abspath, join
import string
import pytest
import pytest_mock
from pytest_bdd import scenario, given, when, then, parsers
import requests
from unittest.mock import ANY

os.environ['SGE_ROOT'] = '/opt'
os.environ['SGE_ARCH'] = 'amd64'

import sge
from sge.status import SgeJobStateCode
import sge_client.shuttle

STATES = dict(queued=SgeJobStateCode.QUEUED_ACTIVE,
              hold=SgeJobStateCode.QUEUED_HELD)

@scenario("package_job.feature", "Packaging a queued job")
def test_package():
    pass

@given(parsers.parse(r"Job id {job_id:d} is {initial_state} locally"))
def local_queued_job(mocker, job_id, initial_state):
    "Stubs out the job_status and job_detail functions"
    mocker.patch('sge.status.get_job_status')
    sge.status.get_job_status.return_value = STATES[initial_state]

@when("I request it to be shuttled")
def request_shuttle(job_id, initial_state, job_detail_xml, mocker):
    if initial_state == 'queued':
        mocker.patch('sge.control.user_hold')
    mocker.patch('sge.shell.run')
    sge.shell.run.return_value = job_detail_xml
    mocker.spy(requests, 'post')
    print(requests.post.call_args)
    sge_client.shuttle.send_job_to_remote(job_id)


@then(parsers.parse(r"It should be placed on hold"))
def local_job_should_be_placed_on_hold(job_id):
    sge.control.user_hold.assert_called_once_with(job_id)

@then("It should be submitted to the remote")
def request_should_be_placed_to_server():
    "A request should be placed to the server"
    requests.post.assert_called_once_with(
        'http://remote-sge.getsandbox.com/jobs.json', json= {
            'arguments': ['blaz', 'forks'],
            'command': 'sleeper.sh',
            'environment': OrderedDict([('bazvar', '213423'), ('TERM', None)]),
            'name': 'quux',
            'package' : ANY}
        )


@pytest.fixture
def post_method_expected_args(job_details):
    return dict(name=job_details['JOB_NAME'],
                command=job_details['SCRIPT_PATH'],
                arguments=[job_details['ARG1'], job_details['ARG2']],
                environment={job_details['ENVVAR'] : job_details['ENVVAL']})

@pytest.fixture
def job_details(job_id):
    fixtures_path = join(dirname(abspath(__file__)), 'fixtures')
    script_path = join(fixtures_path, 'sleeper.sh')
    return dict(JOB_ID=job_id, USER='tyler', JOB_NAME='quux', ARG1='blaz', ARG2='forks',
                ENVVAR='bazvar', ENVVAL='213423', SCRIPT_PATH=script_path)

@pytest.fixture
def job_detail_xml(job_id, job_details):
    fixtures_path = join(dirname(abspath(__file__)), 'fixtures')
    detail_xml = open(join(fixtures_path, 'qstat_detail.xml'), 'r').read()
    template = string.Template(detail_xml)
    return template.substitute(**job_details)


    # Then Local job 34567 should be queued
    # When I request job id 34567 to be shuttled
    # And A request should be sent to the remote server
    # And It should include the arguments given to the local command
    # And It should include the command name
    # And It should include the command file itself
