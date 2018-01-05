"""
Plumbing for sending the local job to the remote.

Ultimately, a request needs to be sent to the server, with:

* job_name
* job_arguments
* job_files


"""
import sge.control

def send_job_to_remote(job_id):
    """
    Packages the job and sends it to the remote server.
    """
    sge.control.user_hold(job_id)


