from setuptools import setup

setup(
    name='allthingstalk',
    version='0.1.5',
    description='AllThingsTalk Python SDK',
    url='https://github.com/allthingstalk/python-sdk',
    download_url='https://github.com/allthingstalk/python-sdk/archive/0.1.5.tar.gz',
    author='Danilo Vidovic',
    author_email='dv@allthingstalk.com',
    license='Apache 2.0',
    packages=['allthingstalk'],
    keywords=['allthingstalk', 'iot', 'sdk'],
    install_requires=[
        'paho-mqtt',
        'requests',
        'python-dateutil',
        'six'
    ]
)
