import unittest
from unittest.mock import Mock, MagicMock
from unittest.mock import patch
from os.path import abspath
import sge_server

class SubmitJobTests(unittest.TestCase):
    "Test the views class"
    def setUp(self):
        self.mockDrmaa()
        sge_server.app.testing = True
        self.app = sge_server.app
        self.client = sge_server.app.test_client()

    def test_get_root(self):
        "Basic verification that we can do things."
        with sge_server.app.app_context():
            response = sge_server.views.root_path()
            self.assertRegex(response, "Restful SGE.  Don't use this app")

    def mockDrmaa(self):
        mock_class = Mock(name="DrmaaSession_Class")
        mock_instance = mock_class()
        mock_instance.jobStatus.return_value = "queued_active"
        sge_server.job_control.DrmaaSession = mock_class

    # @patch("sge_server.qsub_wrapper.shell_command.run")
    def test_upload_job(self):
        job_id = 213415
        qstat_mock = MagicMock(return_value=XML_NO_WD)
        mock_qsub = MagicMock(return_value="Your job %s (\"sleeper.sh\") has been submitted" % job_id)
        with patch('sge_server.job_detail.qstat', qstat_mock):
            with patch('sge_server.qsub_wrapper.qsub', mock_qsub):
                "Actually upload a file"
                data = {
                    "name" : "sleeper.sh",
                    "command" : "sleeper.sh",
                    "file" : (get_file(), "sleeper.sh.tgz")
                }
                self.client.post("/jobs", data=data)
        
        qstat_call = qstat_mock.call_args_list[0][0][0]
        self.assertEqual("-u \"*\" -j %s -xml" % job_id, qstat_call)


    def test_propagate_arguments(self):
        job_id = 213415
        job_control = MagicMock(name="job_control")
        job_control.__enter__.return_value = job_control
        job_control.get_job_detail.return_value={}
        arguments = ["12", "96"]
        remote_job = MagicMock(return_value=job_control)
        with patch("sge_server.qsub_wrapper.QSubWrapper.remote_job", remote_job):
            data = {
                "name" : "sleeper.sh",
                "command" : "sleeper.sh",
                "arguments" : arguments,
                "file" : (get_file(), "sleeper.sh.tgz")
            }
            self.client.post("/jobs", data=data)
        self.assertEqual(remote_job.call_args[-1]['arguments'], arguments)
