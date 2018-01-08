from argparse import ArgumentParser, RawTextHelpFormatter
import sge.shell

YUM_PACKAGES = ['nginx', 'sqlite-devel', 'readline-devel', 'bzip2-devel', 
                'git', 'gcc', 'gcc-c++', 'kernel-devel', 'make', 
                'zlib-devel', 'openssl-devel']

ALINUX_ARG_TEXT = """Amazon Linux only, installs requirements via YUM.
Installs the following: nginx sqlite-devel readline-devel bzip2-devel 
git gcc gcc-c++ kernel-devel make zlib-devel openssl-devel

This is enough to ensure that Python will build without warnings, and
that C extensions for required libraries will all compile.

TODO: verify that there are no unneeded dependencies listed here.
"""

def sudo_something():
    args = ['sudo', 'ls', '-la']
    output = sge.shell.run(*args)
    print(output)

def parse_args():
    parser = ArgumentParser(prog="Remote SGE Server Installer",
                            formatter_class=RawTextHelpFormatter)
    parser.description = """
    Installs a working remote SGE server component.
    """
    parser.add_argument('--alinux',
                        help="""Show status of all jobs given, and quit.""",
                        action="store_true")
    

def main():
    print("Hells yeah")
    sudo_something()

if __name__ == '__main__':
    main()


