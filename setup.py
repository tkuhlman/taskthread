from setuptools import setup, find_packages

import taskthread


setup(
    name='taskthread',
    version=taskthread.__version__,
    url='http://hpcloud.com',
    license='Apache',
    author='John Herndon',
    author_email='john.herndon@hp.com',
    description='Simple thread module to repetitively perform a task on a single thread',
    long_description=open('README.rst').read(),
    packages=find_packages()
)
