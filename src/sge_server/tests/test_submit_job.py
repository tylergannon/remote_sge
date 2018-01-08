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

@scenario("submit_job.feature", "Valid job is submitted")
def test_submit_job():
    pass

@when("A new job is submitted")
def new_job_submitted():
    pass

@then("The data should be extracted")
def data_should_be_extracted():
    pass
    