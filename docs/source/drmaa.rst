Working with DRMAA and qstat
============================

The :mod:`drmaa` module provided by python-drmaa_ has proven difficult to work with.

If it can be eliminated, this may be a worthwhile move.

Steps for replacing DRMAA with the shell utilities for SGE:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Replace the means of getting current state of job.
    DRMAA will straightforwardly return the job state, whereas qstat does not give the
    job state in the detail for the job.

    There are only basically three states we are interested in:

    - Running jobs, which would be suspended,
    - Queued, with or without a hold, which will have a user hold placed on them,
    - Suspended jobs.

    Using a command like this one: ``qstat  -u "*" -s p | grep 33377``
    will quickly determine whether the job is queued/waiting, and should be held.
    
    Could be that such is the only state that we really want to deal with.






Reasons for replacing DRMAA
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. When submitting a job on cfncluster, if there are currently no execution hosts
    then the request will fail.  The behavior of qsub_ is to queue the job and
    return a job id (and then cfncluster will begin adding hosts to process the work.

    This means that the code written to use DRMAA for submitting jobs was not usable
    in the end because of that important edge case.
2. The incompleteness of the API means the need to maintain two different interfaces
    to gridengine: :mod:`drmaa` and the shell utilities of SGE.
3. It's easy enough to stub out calls to shell commands, but ``drmaa`` has turned out
    to be pretty annoying in the development and testing environments, because the 
    python module can't even be imported unless the C components are available on the
    system.


.. _python-drmaa: https://github.com/pygridtools/drmaa-python
.. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html