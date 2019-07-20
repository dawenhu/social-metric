 - celery beat -S redbeat.RedBeatScheduler -A social_metrics.celeryapp:app --loglevel=debug
 - celery worker -Q analytic -A social_metrics.celeryapp:app -n metric_upload.%%h --loglevel=info

Scrapyd Daemon
Start

$ daemon --chdir=/home/ubuntu/server/crawler scrapyd
Kill

$ lsof -wni tcp:6800
$ kill -9 {PID}

Celery Daemon
celeryd daemon
sudo nano /etc/init.d/celeryd
sudo chmod 755 /etc/init.d/celeryd
sudo chown root:root /etc/init.d/celeryd
sudo nano /etc/default/celeryd (celeryd.conf)
sudo /etc/init.d/celeryd {start|stop|status|restart}

celerybeat daemon
sudo nano /etc/init.d/celerybeat
sudo chmod 755 /etc/init.d/celerybeat
sudo chown root:root /etc/init.d/celerybeat
sudo nano /etc/default/celerybeat