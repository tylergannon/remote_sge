"""
Responsible for filesystem IO associated with packaging and unpacking
SGE jobs.
"""
import tarfile

def extract_job(iobase, destination):
    """
    Receives a readable stream containing a tgz archive and extracts it to
    the given destination.

    Args:
        iobase (io.IOBase): a readable IOBase object to extract.  Note that this
            is the base class of the :class:`~urllib3.response.HTTPResponse` class,
            which is given by the ``raw`` attribute of the :class:`~requests.models.Response`
            returned by :func:`~requests.get`.
        destination (str): filesystem location in which to extract the archive.
            Path must exist and be writable by this process
    Returns:
        None
    """
    with tarfile.open(mode="r|gz", fileobj=iobase) as archive:
        archive.extractall(destination)
