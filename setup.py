from setuptools import setup

setup(
    name='allthingstalk',
    version='0.3.0',
    description='AllThingsTalk Python SDK',
    url='https://github.com/allthingstalk/python-sdk',
    download_url='https://github.com/allthingstalk/python-sdk/archive/0.3.0.tar.gz',
    author='AllThingsTalk',
    author_email='support@allthingstalk.com',
    license='Apache 2.0',
    packages=['allthingstalk'],
    keywords=['allthingstalk', 'iot', 'sdk'],
    install_requires=[
        'paho-mqtt>=1.6.0',
        'requests>=2.25.0',
        'python-dateutil>=2.8.0',
        'six>=1.15.0'
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires='>=3.6'
)
