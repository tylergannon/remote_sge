import datetime
import sge.submit

job = sge.submit.JobRequest()
job.command_path = '/home/tgannon/sleeper.sh'
job.job_submission_state = sge.submit.JobSubmissionState.HOLD_STATE
job.join_stdout_and_stderr = True
job.environment = {'QUUX' : 'asdfalskdj;lkjasdf'}
job.deadline_time = datetime.datetime(2018, 1, 10)
print(job.submit())


barth = """
#!/bin/bash
echo FART
SCRIPT=/home/tgannon/sleeper.sh
ARCHIVE_DIR=/home/tgannon
$SCRIPT master blaster
SCRIPT_EXIT=$?
sleep 5

if [ $SCRIPT_EXIT -eq 0 ]; then
  echo "Archiving to $ARCHIVE_DIR/$JOB_ID.tgz"
  tar -cvzf $ARCHIVE_DIR/$JOB_ID.tgz * 1> /dev/null
else
  echo "Script exited with $SCRIPT_EXIT.  Please have a look."
fi

exit $SCRIPT_EXIT

"""
env = "SCRIPT=/home/tgannon/sleeper.sh,ARCHIVE_DIR=/home/tgannon,"
args = ['qsub', '-shell', 'yes', '-S', '/bin/bash', '-v', 'FOO=BAZ']
import subprocess
subprocess.run(args, input=barth, encoding='utf-8')
