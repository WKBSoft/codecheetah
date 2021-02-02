import sys
import secrets
import os

systemd_file = '''

[Unit]
Description=Django Application for My Website
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/ubuntu/*****replace_with_github_repo*****/manage.py runserver 127.0.0.1:1337
StandardInput=tty-force
User=ubuntu

[Install]
WantedBy=multi-user.target
'''

shell_file = '''
sudo apt -y install nginx;
sudo unlink /etc/nginx/sites-enabled/default;
curl https://raw.githubusercontent.com/bellemanwesley/devsite/master/scripts/web_server/nginx-reverse-proxy.conf -o reverse-proxy.conf;
sudo cp reverse-proxy.conf /etc/nginx/sites-available/reverse-proxy.conf;
sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf;
sudo nginx -s reload;
git clone *****replace_with_github_url*****;
sudo apt update;
sudo apt -y install python3-pip;
sudo apt -y install awscli;
pip3 install -r *****replace_with_github_repo*****/requirements.txt;
sudo cp website_server.service /etc/systemd/system/website_server.service;
sudo systemctl daemon-reload;
sudo systemctl enable website_server;
sudo systemctl start website_server;
'''

github_repo = sys.argv[2]
github_url = github_url = "https://github.com/"+sys.argv[1]+"/"+github_repo+".git"

systemd_file = systemd_file.replace("*****replace_with_github_repo*****",github_repo)

shell_file = shell_file.replace("*****replace_with_github_repo*****",github_repo)
shell_file = shell_file.replace("*****replace_with_github_url*****",github_url)

with open("website_server.service","w+") as f:
    f.write(systemd_file)
    
with open("keys/django_key.txt","w+") as f:
    f.write(secrets.token_hex(64))
    
with open("initiate.sh","w+") as f:
    f.write(shell_file)
    
os.system("at now + 1 minutes -f initiate.sh")