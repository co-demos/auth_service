---
title : SUPERVISOR
categories:
  - prod
tags:
  - documentation
  - configuration
  - deployment
  - snippets
toc: true
toc_label: " contents"
toc_sticky: true
---

### USING SUPERVISOR TO RUN GUNICORN/PYTHON PROCESS

cf : [tuto medium](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18)
cf : [tuto real python](https://realpython.com/kickstarting-flask-on-ubuntu-setup-and-deployment/#configure-supervisor)


#### install supervisor
```
sudo apt-get install -y supervisor
```

#### create a new supervisor process for gunicorn
```
sudo nano /etc/supervisor/conf.d/toktok_preprod_api.conf
```

```
[program:toktok_preprod]
directory=/var/www/preprod.toktok-auth.com
command=/var/www/preprod.toktok-auth.com/venv/bin/gunicorn wsgi:app --bind 0.0.0.0:4000
autostart=true
autorestart=true

#stderr_logfile=/var/log/toktok-preprod-api/toktok-preprod-api.err.log
#stdout_logfile=/var/log/toktok-preprod-api/toktok-preprod-api.out.log
```

#### check supervisor proces
```
sudo supervisorctl reread
sudo supervisorctl update
sudo service supervisor restart
sudo supervisorctl status
```

#### restart supervisor process
```
sudo systemctl restart toktok_preprod
```


#### be sure firewall allows ngiinx and desired ports
```
sudo ufw delete allow 4100
sudo ufw allow 'Nginx Full'
```

