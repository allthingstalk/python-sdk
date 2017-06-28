from setuptools import setup

setup(
    name='allthingstalk',
    version='0.1.6',
    description='AllThingsTalk Python SDK',
    url='https://github.com/allthingstalk/python-sdk',
    download_url='https://github.com/allthingstalk/python-sdk/archive/0.1.6.tar.gz',
    author='Danilo Vidovic',
    author_email='dv@allthingstalk.com',
    license='Apache 2.0',
    packages=['allthingstalk'],
    keywords=['allthingstalk', 'iot', 'sdk'],
    install_requires=[
        'paho-mqtt==1.2.3',
        'requests',
        'python-dateutil',
        'six'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
