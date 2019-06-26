#!/bin/bash

PROFILE_NAME=${PROFILE_NAME:-"AppSrv01"}
SERVER_NAME=${SERVER_NAME:-"server1"}
UPDATE_HOSTNAME=${UPDATE_HOSTNAME:-"true"}
# echo $UPDATE_HOSTNAME $SERVER_NAME $PROFILE_NAME
update_hostname()
{
  /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/wsadmin.sh -lang jython -conntype NONE -f /work/updateHostName.py ${NODE_NAME:-"maximoNode"} $(hostname)
  touch /work/hostnameupdated
  echo "updated hostname"
}

setup_http_server()
{
    cd /opt/IBM/HTTPServer/
    bin/postinst -t setupadm -i $PWD
    ./setupadm -create -usr wasadmin -grp wasadmin -cfg ../conf/httpd.conf -adm ../conf/admin.conf
# ./htpasswd -cm ../conf/admin.passwd wasadmin
}

set -e

if [ "$UPDATE_HOSTNAME" = "true" ] && [ ! -f "/work/hostnameupdated" ]; then
  update_hostname
fi

/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startServer.sh server1

tail -f /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/server1/SystemOut.log

exec "$@"