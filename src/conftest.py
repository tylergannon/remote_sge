import os
import pytest

os.environ['SGE_ROOT'] = '/opt'
os.environ['SGE_ARCH'] = 'amd64'

@pytest.fixture
def job_package_str():
    "Returns a string representation of packaged job with sleeper.sh inside."
    return('H4sIACe8WVoC/+3SsQrCMBSF4TvnKSLuNk3S5nXaakqFotK0g29vrOCok6Lwf8vhwlkO3DTGeInTL' +
           'g3yMSarvV8z1NWaxj7ulbdSOmurUAZfBzGlc74SbeQLljS3k9YyX8c4vejlWt+/GZk9809sN0V3PB' +
           'Vdmwal0v0ZtDMq7oezbg7tHBslAAAAAAAAAAAAAAAAAIAfdAN+v52WACgAAA==')
