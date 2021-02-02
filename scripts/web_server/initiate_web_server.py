import sys

systemd_file = '''

[Unit]
Description=Django Application for My Website
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/ubuntu/*****replace_with_project_name*****/manage.py runserver 127.0.0.1:1337
StandardInput=tty-force
User=ubuntu

[Install]
WantedBy=multi-user.target
'''

systemd_file = systemd_file.replace("*****replace_with_project_name*****",sys.argv[1])

with open("website_server.service","w+") as f:
    f.write(systemd_file)