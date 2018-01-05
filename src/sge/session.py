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

from sge.const import (JobState, JobControlAction)
from sge.helpers import (BoolConverter, IntConverter, CmdOptionAttr, 
                           DictionaryConverter, DateTimeConverter)


JobInfo = namedtuple("JobInfo",
                     """jobId hasExited hasSignal terminatedSignal hasCoreDump
                        wasAborted exitStatus resourceUsage""")




class Session(object):

    """
    The DRMAA Session.

    This class is the entry point for communicating with the DRM system
    """

    def __init__(self, contactString=None):
        self.contactString = contactString


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

