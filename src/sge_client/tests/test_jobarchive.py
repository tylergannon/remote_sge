
from collections import OrderedDict
import os
from os.path import basename, dirname, abspath, join
from base64 import b64decode, b64encode
from io import BytesIO
import string
import tempfile
import pytest
import pytest_mock
from pytest_bdd import scenario, given, when, then, parsers
import requests
from unittest.mock import ANY

from sge_client.io.jobarchive import package_job, extract_job

@pytest.fixture
def file_path():
    fixtures_path = join(dirname(abspath(__file__)), 'fixtures')
    return join(fixtures_path, 'sleeper.sh')

@pytest.fixture
def tarfile_object(file_path):
    return package_job(file_path)

def test_can_serialize_tarfile(file_path, tarfile_object):
    with tempfile.TemporaryDirectory() as dir:
        extract_job(tarfile_object, dir)
        file1 = open(file_path).read()
        file2 = open(join(dir, basename(file_path))).read()
        assert file1 == file2    

