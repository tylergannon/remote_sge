Installing Remote SGE
=====================

Steps
^^^^^


Details
^^^^^^^
The application runs inside of a virtualenv_ environment, in order to leave
the system Python alone.

The installer will install pyenv_ in the user's home directory, and add pyenv_
properly to the user's profile such that **remote_sge** can run within the
correct version of Python, inside a virtualenv.

It will create a virtualenv called **remote_sge**, and assumes that any
remote_sge programs will inside there.

.. _pyenv: https://github.com/pyenv/pyenv
.. _virtualenv: https://virtualenv.pypa.io/en/stable/


