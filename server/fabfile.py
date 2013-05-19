from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.operations import run, put

env.user = 'ubuntu'
deploy_user = 'deploy'
deploy_user_home = '/home/deploy'
postgres_user = 'postgres'
database = "grazing"
git_repo = "git@github.com:JesseCrocker/GrazingDB.git"
manage_command = "%s/GrazingDB/webapp/manage.py " % deploy_user_home
app_dir = deploy_user_home + "/GrazingDB/"
#commands to use
def deploy():
    """ deploy a new server from scratch """
    if not env.githubKey:
        #crash if the key isnt specified, because we will need it later
        return
    aptUpdate()
    installSystemSoftware()
    gitclone()
    setupDeployUser()
    postgres()
    installPythonRequirements()
    syncDB()
    upgradeDb()
    nginx()
    collectStatic()
    restart()


def update():
    gitPull()
    installPythonRequirements()
    collectStatic()
    upgradeDb()
    restart()


def aptUpdate():
    sudo("apt-get -q -y update")
    sudo("apt-get -q -y upgrade")


#system setup
def installSystemSoftware():
    sudo("apt-get -q -y install git-core nginx python-pip python-dev python-flup duplicity s3cmd")


def postgres():
    """Install postgres and postGIS"""
    #increased shared memory limit
    sudo("echo kernel.shmmax=457954944 >> /etc/sysctly.conf")
    sudo("apt-get -q -y install python-software-properties")
    sudo("apt-add-repository -y ppa:ubuntugis/ppa")
    sudo("apt-get -q -y update")
    sudo("apt-get -q -y install postgresql-9.1-postgis")
    sudo("psql -f %s/server/createdb.sql" % app_dir, user=postgres_user)
    sudo("psql -d %s -c 'CREATE EXTENSION postgis;CREATE EXTENSION postgis_topology'" % database, user=postgres_user)
    #make sure the extension installed correctly
    sudo("psql -d %s -c 'SELECT name, default_version,installed_version FROM pg_available_extensions'" % database, user=postgres_user)


def nginx():
    """Configure nginx and restart"""
    sudo("rm /etc/nginx/nginx.conf /etc/nginx/sites-available/default")
    with cd("%s/server" % app_dir):
        sudo("ln -s %s/server/nginx/nginx.conf /etc/nginx/nginx.conf" % app_dir)
        sudo("ln -s %s/server/nginx/default /etc/nginx/sites-available/default" % app_dir)
    sudo("/etc/init.d/nginx restart")


def gitclone():
    """clone repo to ubuntu user home dir"""
    put(env.githubKey, "/home/ubuntu/id_rsa")
    run("chmod 600 id_rsa")
    run("mv id_rsa .ssh")
    #put('known_hosts', ".ssh/")
    run("git clone %s" % git_repo)


def gitPull():
    with cd(app_dir):
        sudo("git pull", user=deploy_user)


def gitCheckout():
    with cd(app_dir):
        sudo("git checkout %s" % (env.branch), user=deploy_user)


def setupDeployUser():
    """Setup deploy user"""
    sudo("useradd -d %s -m -s /bin/bash %s" % (deploy_user_home, deploy_user))
    sudo("cp -r GrazingDB/ %s" % deploy_user_home)
    sudo("chown %s.%s -R %s" % (deploy_user, deploy_user, app_dir))
    #cp ssh keys to deploy user so it can pull
    sudo("mkdir %s/.ssh" % deploy_user_home, user=deploy_user)
    sudo("cp /home/ubuntu/.ssh/id_rsa /home/ubuntu/.ssh/known_hosts %s/.ssh" % (deploy_user_home))
    sudo("chown %s.%s -R %s/.ssh" % (deploy_user, deploy_user, deploy_user_home))


def syncDB():
    sudo(manage_command + " syncdb", user=deploy_user)


def collectStatic():
    sudo(manage_command + "collectstatic --noinput", user=deploy_user)


def restart():
    sudo("%s/server/restart.sh" % (app_dir), user=deploy_user)


def upgradeDb():
    sudo(manage_command + " migrate", user=deploy_user)


def installPythonRequirements():
    sudo("pip -q install -r %s/requirements.txt" % app_dir)
