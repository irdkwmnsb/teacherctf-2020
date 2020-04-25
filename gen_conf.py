#!/usr/bin/env python3
conf = """ssl_certificate /etc/letsencrypt/live/2020.teacherctf.com-0001/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/2020.teacherctf.com-0001/privkey.pem;
ssl_trusted_certificate /etc/letsencrypt/live/2020.teacherctf.com-0001/chain.pem;
server {
        listen 80;
        listen [::]:80;
        server_name *.2020.teacherctf.com;
        add_header Strict-Transport-Security "max-age=31536000";
        return 301 https://$host$request_uri;
}
"""

import os

n_tasks = 0
for task_name in os.listdir("tasks"):
    nginx_path = "tasks/" + task_name + "/server/nginx.conf"
    if os.path.exists(nginx_path):
        with open(nginx_path) as f:
            conf += f.read()
        n_tasks += 1

# print(conf)
with open("*.2020.teacherctf.com.conf", "w") as f:
    f.write(conf)

print(conf)
print(n_tasks, "service tasks found")