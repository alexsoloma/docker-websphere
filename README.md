# docker-websphere

docker build -t docker-websphere .

for download error || preferences-->proxies-->  web proxy
docker build --build-arg HTTP_PROXY=http://proxy.emea.ibm.com:8080 -t docker-websphere .


sudo docker run -i -t --privileged=true --name="wasjdktest" -p 9080:9080 -p 9443:9443 -p 5901:5901 -p 9060:9060 -p 9043:9043 docker-websphere bash


/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/sharedLib.py maximo_spg maximoCell maximoNode server1

/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/datasource.py maximoCell maximoNode server1
