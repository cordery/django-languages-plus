from setuptools import setup, find_packages

setup(
    name='django-languages-plus',
    version='0.1.0',
    author='Andrew Cordery',
    author_email='cordery@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/django-languages-plus/',
    zip_safe=False,
    include_package_data=True,
    license='LICENSE.txt',
    description='A django model & fixture containing most of the worlds languages and culture codes',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.2",
    ],
)
