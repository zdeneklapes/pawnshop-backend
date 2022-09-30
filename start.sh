#!/bin/bash
#set -x # log

RM="rm -rfd"
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'

AUTHOR='Zdenek Lapes'
EMAIL='lapes.zdenek@gmail.com'

PROJECT_NAME='pawnshop'

# Utils
function error_exit() {
    printf "${RED}ERROR: $1${NC}\n"
    usage
    exit 1
}

# Project
function clean() {
    ${RM} *.zip

    # Folders
    for folder in "venv" "__pycache__"; do
        find . -type d -iname "${folder}" | xargs "${RM}"
    done

    # Files
    for file in ".DS_Store" "*.log"; do
        find . -type f -iname "${file}" | xargs "${RM}"
    done
}

function tags() {
    ctags -R .
    cscope -Rb
}

function custom_cloc() {
    cloc --not-match-d=migrations --include-lang=Python src/
}

# Docker
function build_up_docker() {
    docker-compose -f docker-compose.yaml up --build
}

function install_docker_deploy() {
    docker-compose up --build -d -f docker-compose-build.yml
}

function docker_show_ipaddress() {
    for docker_container in $(docker ps -aq); do
        CMD1="$(docker ps -a | grep "$docker_container" | grep --invert-match "Exited\|Created" | awk '{print $2}'): "
        if [ "$CMD1" != ": " ]; then
            printf "$CMD1"
            printf "$(docker inspect ${docker_container} | grep "IPAddress" | tail -n 1)\n"
        fi
    done
}

function rm_docker_images_volumes() {
    docker stop $(docker ps -aq)
    docker system prune -a -f
    docker volume prune -f
}

# Env
function envs_to_samples() {
    cd env || error_exit "cd"

    # Clean all samples
    find . -type f -iname "sample*" -delete

    # Create new samples
    for f in $(find . -type f -iname ".env*" | cut -d/ -f2); do
        cat "${f}" | cut -d '=' -f1 | xargs -I "%" echo "%=" >"sample${f}"
    done

    cd .. || error_exit "cd"
}

function samples_to_envs() {
    cd env || error_exit "cd"

    # Clean all samples
    find . -type f -iname ".env*" -delete

    # Create new samples
    for f in $(find . -type f -iname "sample2" | cut -d/ -f2); do
        cat "${f}" | cut -d '=' -f1 | xargs -I "%" echo "%=" >"sample${f}"
    done

    cd .. || error_exit "cd"
}

# Django
function django_runserver() {
    cd src || error_exit "cd"
    ./entrypoint.sh 'local'
    cd .. || error_exit "cd"
}

function django_createsuperuser() {
    cd src || error_exit "cd"
    python3 manage.py createsuperuser
    cd .. || error_exit "cd"
}

function django_clean_migrations() {
    for path in $(find src -type d -iname "migrations"); do
        find "${path}" -type f | grep --invert-match "__init__.py" | xargs ${RM}
    done
    rm src/db.sqlite3
}

function django_test() {
    cd src || error_exit "cd"
    if [ "$1" == "" ]; then
        python3 manage.py test
    else
        python3 manage.py test "$1"
    fi
    cd .. || error_exit "cd"
}

function django_loaddata() {
    django_clean_migrations
    cd src || error_exit "cd"
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py loaddata "./authentication/fixtures/users.json"
    python3 manage.py loaddata "./authentication/fixtures/attendants.json"
    python3 manage.py loaddata "./authentication/fixtures/customers.json"
    python3 manage.py loaddata "./shop/fixtures/shops.json"
    python3 manage.py loaddata "./product/fixtures/products.json"
    python3 manage.py loaddata "./loan/fixtures/loans.json"
    echo "$(find $(find . -type d -iname 'fixtures') -type f -iname '*.json')"
    cd .. || error_exit "cd"
}

# Others
function usage() {
    echo "USAGE:
    # Project
    '-c' | '--clean') clean ;;
    '--tags') tags ;;
    '--cloc') custom_cloc ;;
        # Docker
    '--rm-docker-images-volumes') rm_docker_images_volumes ;;
    '--build-up-docker') build_up_docker ;;
    '--docker-show-ipaddress') docker_show_ipaddress ;;
        # Env
    '--envs-to-samples') envs_to_samples ;;
    '--samples-to-envs') samples_to_envs ;;
        # Django
    '--runserver') django_runserver ;;
    '--createsuperuser') django_createsuperuser ;;
    '--clean-migrations') django_clean_migrations ;;
    '--test')
        shift
        django_test \$1
        ;;
        # Others
    '-h' | '--help') usage ;;
"
}

# Main arguments loop
[[ "$#" -eq 0 ]] && usage && exit 0
while [ "$#" -gt 0 ]; do
    case "$1" in
    # Project
    '-c' | '--clean') clean ;;
    '--tags') tags ;;
    '--cloc') custom_cloc ;;
        # Docker
    '--rm-docker-images-volumes') rm_docker_images_volumes ;;
    '--build-up-docker') build_up_docker ;;
    '--docker-show-ipaddress') docker_show_ipaddress ;;
        # Env
    '--envs-to-samples') envs_to_samples ;;
    '--samples-to-envs') samples_to_envs ;;
        # Django
    '--runserver') django_runserver ;;
    '--createsuperuser') django_createsuperuser ;;
    '--clean-migrations') django_clean_migrations ;;
    '--loaddata') django_loaddata ;;
    '--test')
        shift
        django_test $1
        ;;
        # Others
    '-h' | '--help') usage ;;
    esac
    shift
done
