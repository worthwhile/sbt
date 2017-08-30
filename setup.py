import os
from setuptools import find_packages, setup

VERSION = __import__('sbt').__version__
NAME = 'sbt'
URL = 'https://github.com/worthwhile/wbt/'

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

install_requires = ['requests']

setup(
    name=NAME,
    version=VERSION,
    author='Robert Roskam',
    author_email='rroskam@worthwhile.com',
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,  # declarations in MANIFEST.in
    license='MIT',
    url=URL,
    download_url=URL+'/tarball/'+VERSION,
    description="A partial implementation of solutions by text",
    long_description=read_file('README.md'),
    keywords=['REST api', 'integration', 'SMS'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6,
    ],
    zip_safe=False
)
