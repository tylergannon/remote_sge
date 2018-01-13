import pytest
import pytest_mock
import os

os.environ['SGE_ROOT'] = '/opt'
os.environ['SGE_ARCH'] = 'amd64'
import sge.submit

RESPONSE = """Some stuff about a warning.
Your job 35305 ("sleeper.sh") has been submitted
"""

@pytest.fixture
def mega_job_request():
    import datetime
    request = sge.submit.JobRequest()
    request.command_path = '/usr/local/bin/quuxtable'
    request.arguments = ['foo', 'baz', 'quux']
    request.deadline_time = datetime.datetime(2018, 1, 5)
    request.start_time = datetime.datetime(2018, 1, 4)
    request.environment = {'bax' : 'qaax', 'foot' : 'head'}
    request.job_submission_state = sge.submit.JobSubmissionState.HOLD_STATE
    request.join_files = True

    request.name = 'bartholomew'
    request.output_path = "/tmp"
    request.working_directory = '/home/funkytron/mywd'

    return request

@pytest.fixture
def basic_job_request():
    request = sge.submit.JobRequest()
    request.command_path = '/usr/local/bin/quuxtable'
    return request

    

EXPECTED_ARGS = ['/opt/bin/amd64/qsub', '-dl', '201801050000.00', '-a', '201801040000.00', 
                 '-v', 'bax=qaax,foot=head', '-h', '-j', 'yes', '-N', 'bartholomew', 
                 '-o', '/tmp', '-wd', '/home/funkytron/mywd', 
                 '/usr/local/bin/quuxtable', 'foo', 'baz', 'quux']
def test_do_something_cool(mega_job_request, mocker):
    mocker.patch('sge.shell.run')
    sge.shell.run.return_value = RESPONSE
    job_id = mega_job_request.submit()
    sge.shell.run.assert_called_once_with(*EXPECTED_ARGS)
    assert job_id == 35305

EXPECTED_ARGS2 = ['/opt/bin/amd64/qsub', '/usr/local/bin/quuxtable']
def test_do_something_basic(basic_job_request, mocker):
    mocker.patch('sge.shell.run')
    sge.shell.run.return_value = RESPONSE
    job_id = basic_job_request.submit()
    sge.shell.run.assert_called_once_with(*EXPECTED_ARGS2)
    assert job_id == 35305
