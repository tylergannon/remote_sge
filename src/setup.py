"sge_client setup file"
from os.path import dirname, join
from glob import glob
from setuptools import setup

with open(join(dirname(__file__), '..', 'README.rst'), 'r') as file:
    long_description = file.read()

data_files = glob('etc/*')

setup(name='remote_sge',
      description='Utilities for remote submission and collection of GridEngine jobs.',
      long_description=long_description,
      version=open(join(dirname(__file__), 'VERSION.txt')).read(),
      include_package_data=True,
      url='https://github.com/tylergannon/remote_sge',
      author='Tyler Gannon',
      author_email='tyler.gannon@interxinc.com',
      license='Apache2',
      package_data={'' : [
          'bin/remote_sge_job_wrapper.sh'
      ]},
      data_files=[
          (join('etc', 'remote_sge'), data_files),
          ('bin', ['bin/gunicorn_init.d.sh', 'bin/sleeper.sh', 'bin/remote_sge_job_wrapper.sh'])
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      packages=['sge', 'sge.io', 'sge_client', 'sge_server', 'sge.util',
                'sge_client.io', 'sge_server.util', 'sge_client.util'],
      install_requires=[
          'requests>2.18',
          'filelock>=2.0',
          'falcon>=1.4.0rc2',
          'gunicorn>=19.7.1'
      ],
      scripts=[
          'bin/remote_sge_job_wrapper.sh'
      ],
      entry_points={
          'console_scripts': [
              'remote_sge=sge.util.entrypoint:main'
          ]
      }
)
