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

#commands to use
def deploy():
    """ deploy a new server from scratch """
    aptUpdate()
    installSystemSoftware()
    gitclone()
    postgres()
    setupDeployUser()
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
    sudo("addgroup trusted")
    sudo("apt-get -q -y install git-core nginx python-pip python-dev python-flup duplicity s3cmd")


def postgres():
    """Install postgres and postGIS"""
    #increased shared memory limit
    sudo("echo kernel.shmmax=457954944 >> /etc/sysctly.conf")
    sudo("apt-get -q -y install python-software-properties")
    sudo("apt-add-repository -y ppa:ubuntugis/ppa")
    sudo("apt-get -q -y update")
    sudo("apt-get -q -y install postgresql-9.1-postgis")
    sudo("psql < /home/ubuntu/GaiaCloud/server/create_database_and_users.sql", user=postgres_user)
    sudo("psql -d %s -c 'CREATE EXTENSION postgis;CREATE EXTENSION postgis_topology'" % database, user=postgres_user)
    #make sure the extension installed correctly
    sudo("psql -d %s -c 'SELECT name, default_version,installed_version FROM pg_available_extensions'" % database, user=postgres_user)


def nginx():
    """Configure nginx and restart"""
    with cd("%s/GrazingDB/server" % deploy_user_home):
        sudo("ln -s nginx/nginx.conf /etc/nginx/nginx.conf")
        sudo("ln -s nginx/default /etc/nginx/sites-available/default")
    sudo("/etc/init.d/nginx restart")


def gitclone():
    """clone gaia cloud repo to ubuntu user home dir"""
    put(env.githubKey, "/home/ubuntu/")
    run("chmod 600 id_rsa")
    run("mv id_rsa .ssh")
    put('known_hosts', ".ssh/")
    run("git clone %s" % git_repo)


def gitPull():
    with cd("%s/GrazingDB/" % (deploy_user_home)):
        sudo("git pull", user=deploy_user)


def gitCheckout():
    with cd("%s/GrazingDB/" % (deploy_user_home)):
        sudo("git checkout %s" % (env.branch), user=deploy_user)


#gaia cloud app setup
def setupDeployUser():
    """Setup deploy user"""
    sudo("useradd -d %s -m -s /bin/bash -G trusted %s" % (deploy_user_home, deploy_user))
    sudo("cp -r GrazingDB/ %s" % deploy_user_home)
    sudo("chown %s.%s -R %s/GaiaCloud/" % (deploy_user, deploy_user, deploy_user_home))
    #cp ssh keys to deploy user so it can pull
    sudo("mkdir %s/.ssh" % deploy_user_home, user=deploy_user)
    sudo("cp /home/ubuntu/.ssh/id_rsa /home/ubuntu/.ssh/known_hosts %s/.ssh" % (deploy_user_home))
    sudo("chown %s.%s -R %s/.ssh" % (deploy_user, deploy_user, deploy_user_home))


def syncDB():
    sudo(manage_command + " syncdb", user=deploy_user)


def collectStatic():
    sudo(manage_command + "collectstatic --noinput", user=deploy_user)


def restart():
    sudo("%s/GrazingDB/server/restart.sh" % (deploy_user_home), user=deploy_user)


def upgradeDb():
    sudo(manage_command + " migrate", user=deploy_user)


def installPythonRequirements():
    sudo("pip install -r /home/gaia/GaiaCloud/gaia/requirements.txt")
