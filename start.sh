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

function usage() {
    echo "USAGE:
    '-c' | '--clean') clean ;;
    '--rm-docker-images-volumes') rm_docker_images_volumes ;;
    '--clean-django-migrations') clean_django_migrations ;;
    '--build-up-docker') build_up_docker ;;
    '--docker-show-ipaddress') docker_show_ipaddress ;;
    '--envs-to-samples') envs_to_samples ;;
    '--samples-to-envs') samples_to_envs ;;
    '--tags') tags ;;
    '-h' | '--help') usage ;;
"
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

function clean_django_migrations() {
    find "$(find src -type d -iname "migrations")" -type f | grep --invert-match "__init__.py" | xargs ${RM}
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

# Main arguments loop
[[ "$#" -eq 0 ]] && usage && exit 0
while [ "$#" -gt 0 ]; do
    case "$1" in
    '-c' | '--clean') clean ;;
    '--rm-docker-images-volumes') rm_docker_images_volumes ;;
    '--clean-django-migrations') clean_django_migrations ;;
    '--build-up-docker') build_up_docker ;;
    '--docker-show-ipaddress') docker_show_ipaddress ;;
    '--envs-to-samples') envs_to_samples ;;
    '--samples-to-envs') samples_to_envs ;;
    '--tags') tags ;;
    '-h' | '--help') usage ;;
    esac
    shift
done
