from fabric.api import run, env, task, cd, sudo
from fabric.operations import get

"""
pip install fabric

how to run:
fab deploy -H root@www.jedutils.com
"""

@task
def deploy():
    prob_home = '/var/www/django/tobeawebproperty'
    with cd(prob_home):
        sudo('git pull')
        sudo('./manage.py collectstatic --noinput')
        sudo('./manage.py migrate')
        # sudo('/etc/init.d/supervisor restart')