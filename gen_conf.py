#!/usr/bin/env python3
task_conf = """
server {{ # {task_name}
    listen 443 ssl;
    server_name {task_name}.2020.teacherctf.com;
    location / {{
        proxy_pass http://localhost:{port};
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
}}"""

import os
import yaml

tasks = []
used_ports = {}
tasks_compiled = ""
fatals = 0
for task_name in os.listdir("tasks"):
    task_name = "tasks/"+task_name
    if os.path.isdir(task_name):
        docker_path = os.path.join(task_name, "server/docker-compose.yml")
        if os.path.isfile(docker_path):        
            print("task: ", task_name, "Is a service!")
            with open(docker_path) as f:
                docker = yaml.load(f)
                if "services" not in docker:
                    print("Fatal: no services")
                    fatals += 1
                    continue
                if task_name not in docker["services"]:
                    print("fatal: task_name doesn't match or does not exist")
                    fatals += 1
                    continue
                if "ports" not in docker["services"][task_name]:
                    print("fatal: no ports directive ")
                    fatals += 1
                    continue
                ports = docker["services"][task_name]["ports"]
                if len(ports) != 1:
                    print("fatal: more/less than 1 port")
                    fatals += 1
                    continue
                port = ports[0].split(":")[0]
                if port in used_ports:
                    print("fatal: port is used")
                    fatals += 1
                    continue
                tasks_compiled += task_conf.format(task_name=task_name, port=port)
                print(f"{task_name}.2020.teacherctf.com -> http://localhost:{port}")

conf = tasks_compiled
#print(conf)
with open("*.2020.teacherctf.com.conf", "w") as f:
    f.write(conf)

print(f"{fatals} errors")
