from fabric.api import env, roles, run, cd

# Define sets of servers as roles
env.roledefs = {
    'web': ['refstack.org'],
}

# Set the user to use for ssh
env.user = 'refstack'

@roles('web')
def get_version():
    run('cat /etc/issue')
    
    
@roles('web')
def deploy():
    with cd('/var/www/refstack'):
        run('git checkout master')
        run('git pull')
        run('sudo pip install -r requirements.txt')
        run('sudo python -c "from refstack import web; web.db.create_all()"')
        run('alembic upgrade head')
        run('sudo uwsgi --reload /tmp/project-master_refstack.pid')