"sge_client setup file"
from os.path import dirname, join
from setuptools import setup

with open(join(dirname(__file__), '..', 'README.rst'), 'r') as file:
    long_description = file.read()

setup(name='remote_sge',
      description='Utilities for remote submission and collection of GridEngine jobs.',
      long_description=long_description,
      version=open(join(dirname(__file__), 'VERSION.txt')).read(),
      include_package_data=True,
      #   url='https://github.com/massenz/filecrypt',
      author='Tyler Gannon',
      author_email='tyler.gannon@interxinc.com',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      packages=['sge', 'sge_client', 'sge_server'],
      install_requires=[
        'requests>2.18,<3.0',
        'filelock>=2.0,<3.0'
      ],
      extra_requires={
          'server' : ['flask>=0.12,<0.13','gunicorn>=19.7.1,<20']
      },
      entry_points={
        #   'console_scripts': [
        #       'rqsub=sge_client.rqsub:main',
        #       'rqstat=sge_client.rqstat:main'
        #   ]
      }
)
