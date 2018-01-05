import datetime
import sge.submit

job = sge.submit.JobRequest()
job.command_path = '/home/tgannon/sleeper.sh'
job.job_submission_state = sge.submit.JobSubmissionState.HOLD_STATE
job.join_files = True
job.job_environment = {'QUUX' : 'asdfalskdj;lkjasdf'}
job.deadline_time = datetime.datetime(2018, 1, 10)
print(job.submit())
