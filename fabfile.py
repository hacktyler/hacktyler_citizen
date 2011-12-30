#!/usr/bin/env python

from fabric.api import *

"""
Base configuration
"""
env.project_name = 'citizen'
env.repository_url = "git@github.com:hacktyler/hacktyler_citizen.git"
env.phonegap_repo = "git@git.phonegap.com:onyxfish/59359_HackTylerCitizen.git"

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.s3_bucket = 'media.hacktyler.com'
    env.app_s3_bucket = 'citizen.hacktyler.com'

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.s3_bucket = 'media-beta.hacktyler.com'
    env.app_s3_bucket = 'citizen-beta.hacktyler.com'
    
"""
Commands - deployment
"""   
def deploy_phonegap():
    require('settings', provided_by=[production, staging])
    local('DEPLOYMENT_TARGET=%(settings)s PHONEGAP_REPO=%(phonegap_repo)s ./update_phonegap.sh' % env)

def gzip_assets():
    """
    GZips every file in the assets directory and places the new file
    in the gzip directory with the same filename.
    """
    local('python gzip_assets.py')

def deploy():
    """
    Deploy the latest project site media to S3.
    """
    require('settings', provided_by=[production, staging])

    gzip_assets()

    env.gzip_path = 'gzip/'
    local('s3cmd -P --add-header=Content-encoding:gzip --guess-mime-type --rexclude-from=s3exclude sync %(gzip_path)s s3://%(app_s3_bucket)s/' % env)
    local('s3cmd put -P app/config-%(settings)s.js s3://%(app_s3_bucket)s/js/config.js' % env)

def runserver():
    """
    Runs a local web server to test the web app
    """
    local('cd app/web && python -m SimpleHTTPServer 8000')

