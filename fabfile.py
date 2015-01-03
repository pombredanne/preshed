from fabric.api import local, run, lcd, cd, env

import os
from os import path
from os.path import exists as file_exists
from fabtools.python import virtualenv


PWD = path.dirname(__file__)
VENV_DIR = path.join(PWD, '.env')


def sdist():
    if file_exists('dist/'):
        local('rm -rf dist/')
    local('mkdir dist')
    with virtualenv(VENV_DIR):
        local('python setup.py sdist')


def publish():
    with virtualenv(VENV_DIR):
        local('python setup.py register')
        local('twine upload dist/*.tar.gz')


def setup():
    if file_exists('.env'):
        local('rm -rf .env')
    local('virtualenv .env')


def install():
    with virtualenv(VENV_DIR):
        local('pip install --upgrade setuptools')
        local('pip install murmurhash')
        local('pip install dist/*.tar.gz')
        local('pip install pytest')


def make():
    with virtualenv(VENV_DIR):
        with lcd(path.dirname(__file__)):
            local('python dev_setup.py build_ext --inplace')


def clean():
    with lcd(os.path.dirname(__file__)):
        local('python dev_setup.py clean --all')

def test():
    with virtualenv(VENV_DIR):
        local('py.test -x')
