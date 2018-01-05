# -----------------------------------------------------------
#  Copyright (C) 2008 StatPro Italia s.r.l.
#
#  StatPro Italia
#  Via G. B. Vico 4
#  I-20123 Milano
#  ITALY
#
#  phone: +39 02 96875 1
#  fax:   +39 02 96875 605
#
#  This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE. See the license for more details.
# -----------------------------------------------------------
#
#  Author: Enrico Sirola <enrico.sirola@statpro.com>
'''
Everything related to sessions and jobs.
'''

from __future__ import absolute_import, print_function, unicode_literals

import sys
from collections import namedtuple
from ctypes import byref, c_int, create_string_buffer, pointer, POINTER, sizeof

from sge.const import (JobState, JobControlAction,
                         JobSubmissionState)
from sge.helpers import (BoolConverter, IntConverter, QSubOption, QSubOptions, 
                           DictionaryConverter, DateTimeConverter)


JobInfo = namedtuple("JobInfo",
                     """jobId hasExited hasSignal terminatedSignal hasCoreDump
                        wasAborted exitStatus resourceUsage""")


class JobTemplate(object):

    # @property
    # def attributeNames(self):
    #     """
    #     The list of supported DRMAA scalar attribute names.

    #     This is apparently useless now, and should probably substituted by the
    #     list of attribute names of the JobTemplate instances.
    #     """
    #     return list(attribute_names_iterator())

    # scalar attributes
    remoteCommand = None
    """The command to be executed."""

    @property
    def job_submission_state(self):
        """
        Whether the job should be submitted with a hold, or queued/active.
        Use the constants from :class:`drmaa.JobSubmissionState`.
        """
        if QSubOptions.HOLD in self.qsub_options:
            return JobSubmissionState.HOLD_STATE
        else:
            return JobSubmissionState.ACTIVE_STATE

    @job_submission_state.setter
    def job_submission_state(self, value):
        """
        Since -h is a binary flag, setting the value here will either add or remove
        the flag from `qsub_options`.
        """
        if value == JobSubmissionState.HOLD_STATE:
            self.qsub_options[QSubOptions.HOLD] = None
        elif QSubOptions.HOLD in self.qsub_options:
            del self.qsub_options[QSubOptions.HOLD]
    

    """The job status."""
    working_directory = QSubOption(QSubOptions.WORKING_DIR)

    """The job working directory."""
    # jobCategory = None  #: The job category.  Ignored here.
    native_specification = None #: Raw command-line options for qsub.
    """
    A (DRM-dependant) opaque string to be passed to the DRM representing
    other directives.
    """
    # blockEmail = Attribute(BLOCK_EMAIL, type_converter=BoolConverter)
    """False if this job should send an email, True otherwise."""

    start_Time = QSubOption(QSubOptions.START_TIME, type_converter=DateTimeConverter)#: Start time

    """The job start time, a partial timestamp string."""
    job_name = QSubOption(QSubOptions.JOB_NAME)
    """The job Name."""
    # inputPath = None # But we're not supporting reading from STDIN
    """The path to a file representing job's stdin."""
    output_path = QSubOption(QSubOptions.OUTPUT_PATH)
    """The path to a file representing job's stdout."""
    # errorPath = Attribute(ERROR_PATH) #  Not supported in this version.
    """The path to a file representing job's stderr."""
    join_files = QSubOption(QSubOptions.JOIN, BoolConverter)
    """True if stdin and stdout should be merged, False otherwise."""
    # the following is available on ge6.2 only if enabled via cluster
    # configuration
    # transferFiles = Attribute(TRANSFER_FILES) # Not supporting this.
    """
    True if file transfer should be enabled, False otherwise.

    This option might require specific DRM configuration (it does on SGE).
    """
    # the following are apparently not available on ge 6.2
    # it will raise if you try to access these attrs
    deadline_time = QSubOption(QSubOptions.DEADLINE_TIME, DateTimeConverter)
    """The job deadline time, a partial timestamp string."""
    # hardWallclockTimeLimit = Attribute(WCT_HLIMIT, IntConverter)
    """
    'Hard' Wallclock time limit, in seconds.

    The job will be killed by the DRM if it takes more than
    'hardWallclockTimeLimit' to complete.
    """
    # softWallclockTimeLimit = Attribute(WCT_SLIMIT, IntConverter)
    """
    'Soft' Wallclock time limit, in seconds.

    The job will be signaled by the DRM if it takes more than
    'hardWallclockTimeLimit' to complete.
    """
    # hardRunDurationLimit = Attribute(DURATION_HLIMIT, IntConverter)
    # softRunDurationLimit = Attribute(DURATION_SLIMIT, IntConverter)

    # vector attributes
    # email = VectorAttribute(V_EMAIL)
    """email addresses to whom send job completion info."""
    command_arguments = [] #: The arguments to be given to the command.
    """The job's command argument list."""
    # dict attributes
    job_environment = QSubOption(QSubOptions.ENV, DictionaryConverter)
    """The job's environment dict."""

    _as_parameter_ = None

    def __init__(self, **kwargs):
        """
        Builds a JobTemplate instance.

        Attributes can be passed as keyword arguments.
        """
        self.qsub_options = {}
        for aname in kwargs:
            setattr(self, aname, kwargs.get(aname))


class Session(object):

    """
    The DRMAA Session.

    This class is the entry point for communicating with the DRM system
    """

    def __init__(self, contactString=None):
        self.contactString = contactString

    # returns JobTemplate instance
    @staticmethod
    def createJobTemplate():
        """
        Allocates a new job template.

        The job template is used to set the environment for jobs to be
        submitted. Once the job template has been created, it should also be
        deleted (via deleteJobTemplate()) when no longer needed. Failure to do
        so may result in a memory leak.
        """
        return JobTemplate()

    # takes JobTemplate instance, no return value
    @staticmethod
    def deleteJobTemplate(jobTemplate):
        """
        Deallocate a job template.

        :Parameters:
          jobTemplate : JobTemplate
            the job temptare to be deleted

        This routine has no effect on running jobs.
        """
        jobTemplate.delete()

    # takes JobTemplate instance, returns string
    @staticmethod
    def runJob(jobTemplate):
        """
        Submit a job with attributes defined in the job template.

        :Parameters:
          jobTemplate : JobTemplate
            the template representing the job to be run

        The returned job identifier is a String identical to that returned
        from the underlying DRM system.
        """
        pass

    # takes JobTemplate instance and num values, returns string list
    @staticmethod
    def runBulkJobs(jobTemplate, beginIndex, endIndex, step):
        """
        Submit a set of parametric jobs, each with attributes defined in the job
        template.

        :Parameters:
          jobTemplate : JobTemplate
            the template representng jobs to be run
          beginIndex : int
            index of the first job
          endIndex : int
            index of the last job
          step : int
            the step between job ids

        The returned job identifiers are Strings identical to those returned
        from the underlying DRM system.  The JobTemplate class defines a
        `JobTemplate.PARAMETRIC_INDEX` placeholder for use in specifying paths.
        This placeholder is used to represent the individual identifiers of
        the tasks submitted through this method.
        """
        pass

    # takes string and JobControlAction value, no return value
    @staticmethod
    def control(jobId, operation):
        """
        Used to hold, release, suspend, resume, or kill the job identified by jobId.

        :Parameters:
          jobId : string
            if jobId is `Session.JOB_IDS_SESSION_ALL` then this routine acts on
            all jobs submitted during this DRMAA session up to the moment
            control() is called. The legal values for
            action and their meanings are
          operation : string
            possible values are:
                `JobControlAction.SUSPEND`
                  stop the job
                `JobControlAction.RESUME`
                  (re)start the job
                `JobControlAction.HOLD`
                  put the job on-hold
                `JobControlAction.RELEASE`
                  release the hold on the job
                `JobControlAction.TERMINATE`
                  kill the job

        To avoid thread races in multithreaded applications, the DRMAA
        implementation user should explicitly synchronize this call with
        any other job submission calls or control calls that may change
        the number of remote jobs.

        This method returns once the action has been acknowledged by the DRM
        system, but does not necessarily wait until the action has been
        completed.  Some DRMAA implementations may allow this method to be
        used to control jobs submitted external to the DRMAA session, such as
        jobs submitted by other DRMAA session in other DRMAA implementations
        or jobs submitted via native utilities.
        """
        pass


    # takes string, returns JobState instance
    @staticmethod
    def jobStatus(jobId):
        """
        returns the program status of the job identified by jobId.

        The possible values returned from
        this method are:

        * `JobState.UNDETERMINED`: process status cannot be determined,
        * `JobState.QUEUED_ACTIVE`: job is queued and active,
        * `JobState.SYSTEM_ON_HOLD`: job is queued and in system hold,
        * `JobState.USER_ON_HOLD`: job is queued and in user hold,
        * `JobState.USER_SYSTEM_ON_HOLD`: job is queued and in user and
                                          system hold,
        * `JobState.RUNNING`: job is running,
        * `JobState.SYSTEM_SUSPENDED`: job is system suspended,
        * `JobState.USER_SUSPENDED`: job is user suspended,
        * `JobState.DONE`: job finished normally, and
        * `JobState.FAILED`: job finished, but failed.

        The DRMAA implementation should always get the status of the job from
        the DRM system unless the status has already been determined to be
        FAILED or DONE and the status has been successfully cached. Terminated
        jobs return a FAILED status.
        """

