from fabric.api import run, env, task, cd, sudo
from fabric.operations import get

"""
pip install fabric

how to run:
fab deploy -H root@demo.jedutils.com
"""

@task
def deploy():
    prob_home = '/var/www/django/tobeawebproperty'
    with cd(prob_home):
        sudo('git pull')
        run('workon haweb && ./manage.py collectstatic --noinput')
        run('workon haweb && ./manage.py migrate')
        run('workon haweb && gunicorn -w 2 -p 8000 -n haweb haweb.wsgi:application &')
        # sudo('/etc/init.d/supervisor restart')