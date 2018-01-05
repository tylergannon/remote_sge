"""
Encapsulates simple calls to the :mod:`drmaa` library.

The conditional import is so that the package will build in environments
where gridengine's drmaa library is not available, such as on *readthedocs*
and *circleci*.

Actually the :mod:`~sge_client.io.fakedrmaa` module should never be used,
since the testing units mock the methods found in the present module.

"""
DRMAA_ERROR = 'Could not find drmaa library.  Please specify its full path using the environment variable DRMAA_LIBRARY_PATH'

try:
    import drmaa
    from drmaa.errors import InvalidJobException
except RuntimeError as runtime_error:
    if runtime_error.args[0] == DRMAA_ERROR:
        import sge_client.io.fakedrmaa as drmaa
        from sge_client.io.fakedrmaa import InvalidJobException
    else:
        raise runtime_error


UNKNOWN_JOB_STATE = "unknown"

def new_session():
    "Instantiates and returns a new :class:`drmaa.Session` object."
    return drmaa.Session()

def get_job_state(job_id, session=None):
    """
    Opens a new DRMAA session if none is given, and gets the current state of
    a scheduled or running job in the cluster.

    Args:
        job_id (str): a string containing an integer ID for the requested job.

        session (:class:`~drmaa.Session`): an opened session object for talking to
            the queue master.

    Returns:
        Integer containing the state code for the job.  If the job is not found,
        returns the string "unknown".
    """
    try:
        if session:
            return session.jobStatus(str(job_id))
        else:
            with drmaa.Session() as session:
                return session.jobStatus(job_id)
    except InvalidJobException as invalid_job_exception:
        print('error checking job')
        print(invalid_job_exception)
        return UNKNOWN_JOB_STATE
