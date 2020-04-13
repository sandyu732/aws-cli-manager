from setuptools import setup

setup(
    name='bouncy',
    version='0.1',
    author="Sandeep Upadhyay",
    author_email="sandeepupadhyay732.com",
    description="This is a tool to manage AWS EC2 instances through command line",
    license="GPLv3+",
    packages=['bouncy'],
    url="https://github.com/sandyu732/aws-cli-manager",
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        bouncy=bouncy.bouncy:cli
    ''',
)