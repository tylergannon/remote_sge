import json
import falcon
from sge.submit import JobRequest

class Job(object):
    def on_post(self, req, resp):
        job_request = JobRequest(**json.load(req.stream))
        # job_id = job_request.submit()
        job_id = 12345
        resp.body = json.dumps(dict(job_id=job_id))
        resp.status = falcon.HTTP_CREATED
