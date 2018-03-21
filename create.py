#! /usr/bin/python

import subprocess
from subprocess import Popen, PIPE, check_output
from shutil import copy, rmtree

import os
#! /usr/bin/python

import sys
import uuid

# default repo name is btc
repo_name = "bitcoind_local"
# assign a random tag
tag_name = str(uuid.uuid1()).split('-')[0]

use_installed_bitcoind = False
bitcoind_path = "./"

arguments = sys.argv
arguments_len = len(arguments)


py_file_path = os.path.dirname(os.path.realpath(__file__))


for i in range(0, arguments_len):
    arg = arguments[i]
    if arg == "--repo":
        repo_name = arguments[i + 1]
    elif arg == "--tag":
        tag_name = arguments[i + 1]
    elif arg == "--sourcedir":
        bitcoind_path = arguments[i + 1]
    elif arg == "--use-installed":
        use_installed_bitcoind = True
    elif arg == "--help":
        print("--repo [reponame]")
        print("--tag [tag]")
        print("--sourcedir [bitcoind source directory]")
        print("--use-installed. Use installed bitcoind. Ignore --sourcedir")
        exit()

if use_installed_bitcoind:
    bitcoind_file = check_output(['which', 'bitcoind']).decode("ascii").rstrip()
    bitcoind_path = os.path.dirname(bitcoind_file)
else:
    bitcoind_file = os.path.join(bitcoind_path, "bitcoind")

if os.path.isfile(bitcoind_file) == False:
    print(bitcoind_file + " is not a file or not found")
    exit()

print("bitcoind file location: " + os.path.realpath(bitcoind_path))
docker_image_name = repo_name + ':' + tag_name
print('docker image name is ' + docker_image_name + " (repo:tag)")

docker_build_dir = 'docker_build/'

if not os.path.exists(docker_build_dir):
    os.makedirs(docker_build_dir)

copy(os.path.join(py_file_path, 'run'), docker_build_dir)
copy(os.path.join(py_file_path, 'Dockerfile'), docker_build_dir)

# copy bitcoind
copy(bitcoind_file, docker_build_dir)

# get bitcoind depedencies
lddresult = check_output(['ldd', docker_build_dir + 'bitcoind']).decode("ascii")

#split to lines
results_line = lddresult.split('\n')

# copy dependencies only from /usr/lib. 
for line in results_line:
    line_words = line.split(' ')
    if len(line_words) >=3:
        file_name = line_words[2] 
        if file_name.find('/usr/lib/') != -1 or file_name.find('/usr/local/lib') != -1:
            # print(file_name)
            # if os.path.islink(file_name):
            #     print("--Link file -> " + os.readlink(file_name))
            copy(file_name, docker_build_dir)

# build docker image
p = Popen(['docker', 'build', '-t', docker_image_name, docker_build_dir])
p.wait()

rmtree(docker_build_dir)