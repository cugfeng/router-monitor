# router-monitor

Sometimes at midnight router lost network connection. If it happens, reboot the router.

There are two ways to run the monitor, one is from supervisor, another is from docker.


** supervisor **

sudo pip install -r requirements.txt
sudo cp router-monitor.conf /etc/supervisor/conf.d/
sudo service supervisor restart


** docker **

sudo docker build -t routermonitor:latest -t routermonitor:v0.1 .
sudo docker run -d -v /etc/localtime:/etc/localtime:ro -v /var/log:/var/log --name routermonitor routermonitor
