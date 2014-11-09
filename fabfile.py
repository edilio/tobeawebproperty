from fabric.api import run, env, task, cd, sudo
from fabric.operations import get

"""
pip install fabric

how to run:
fab deploy -i ~/.ssh/dak-edilio-only.pem -H ubuntu@www.crowdconcerns.com
"""

@task
def deploy():
    prob_home = '/var/django/crowdconcerns.com/concernsprj'
    with cd(prob_home):
        sudo('git pull')
        sudo('./manage.py collectstatic --noinput')
        sudo('./manage.py migrate')
        sudo('/etc/init.d/supervisor restart')