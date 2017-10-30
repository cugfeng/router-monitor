# router-monitor

Sometimes at midnight router lost network connection. If it happens, reboot the router.

There are two ways to run the monitor, one is from supervisor, another is from docker.


## supervisor ##

sudo pip install -r requirements.txt<br />
sudo cp router-monitor.conf /etc/supervisor/conf.d<br />
sudo service supervisor restart<br />


## docker ##

sudo docker build -t routermonitor:latest -t routermonitor:v0.1 .<br />
sudo docker run -d -v /etc/localtime:/etc/localtime:ro -v /var/log:/var/log --name routermonitor routermonitor<br />
