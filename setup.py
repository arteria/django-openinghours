# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import openinghours as app

setup(
    name="django-openinghours",
    version=app.__version__,
    description=open('DESCRIPTION').read(),
    long_description=open('README.rst').read(),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, app, openinghours, shop, store',
    author='arteria GmbH, fmalina',
    author_email='admin@arteria.ch, fmalina@gmail.com',
    url="https://github.com/arteria/django-openinghours",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django', 'django-threadlocals', 'django-compat'],
)
