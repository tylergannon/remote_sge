"""
Helper method for making calls through the BASH shell.
"""
import subprocess
from subprocess import PIPE, STDOUT

COMMAND = ['/bin/bash', '-c']

def run(command, *arguments):
    "Runs the specified command through BASH and returns the STDOUT output as a string."
    command_string = ' '.join([command, *arguments])
    process = subprocess.run([*COMMAND, command_string], stdout=PIPE, stderr=STDOUT)
    return process.stdout.decode()
