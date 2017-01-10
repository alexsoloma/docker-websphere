# (C) Copyright IBM Corporation 2015.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04

MAINTAINER Kavitha Suresh Kumar <kavisuresh@in.ibm.com> (@kavi2002suresh)

RUN apt-get update \
    && apt-get install -y wget unzip vim \
    && rm -rf /var/lib/apt/lists/*

## Install JRE
#ENV JAVA_VER=8 \
#    JAVA_REL=0 \
#    JAVA_MF=3.0 \
#    JAVA_URL=https://iwm.dhe.ibm.com/sdfdl/1v2/regs2/linuxjavasdks/java/java6/6/0/16/26/linuxamd64/Xa.2/Xb.N3K5zJziAi47Qv_gscb8BZ42YBMa1KnE9SQqve3D6Ik/#Xc.6/0/16/26/linuxamd64/ibm-java-sdk-6.0-16.26-linux-x86_64.bin/Xd./Xf.LPr.D1vk/Xg.8700886/Xi.swg-sdk6/XY.regsrvs/XZ.gWEJbA2TcA7O8zL44rME5rpqHLg/#ibm-java-sdk-6.0-16.26-linux-x86_64.bin
#RUN wget -q -U UA-IBM-JAVA-Docker -O /tmp/ibm-java.bin $JAVA_URL \
#    && echo "INSTALLER_UI=silent" > /tmp/response.properties \
#    && echo "USER_INSTALL_DIR=/opt/ibm/java" >> /tmp/response.properties \
#    && echo "LICENSE_ACCEPTED=TRUE" >> /tmp/response.properties \
#    && mkdir -p /opt/ibm \
#    && chmod +x /tmp/ibm-java.bin \
#    && /tmp/ibm-java.bin -i silent -f /tmp/response.properties \
#    && rm -f /tmp/response.properties \
#    && rm -f /tmp/ibm-java.bin
#ENV JAVA_HOME=/opt/ibm/java \
#    PATH=/opt/ibm/java/jre/bin:$PATH
#
## Install WebSphere Liberty
#ENV LIBERTY_VERSION 8.5.5_09
#RUN LIBERTY_URL=$(wget -q -O - https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/wasdev/downloads/wlp/index.yml  | grep $LIBERTY_VERSION #-A 6 | sed -n 's/\s*javaee7:\s//p' | tr -d '\r')  \
#    && wget -q $LIBERTY_URL -U UA-IBM-WebSphere-Liberty-Docker -O /tmp/wlp.zip \
#    && unzip -q /tmp/wlp.zip -d /opt/ibm \
#    && rm /tmp/wlp.zip
#ENV PATH=/opt/ibm/wlp/bin:$PATH
#
## Set Path Shortcuts
#ENV LOG_DIR=/logs \
#    WLP_OUTPUT_DIR=/opt/ibm/wlp/output
#RUN mkdir /logs \
#    && ln -s $WLP_OUTPUT_DIR/defaultServer /output \
#    && ln -s /opt/ibm/wlp/usr/servers/defaultServer /config
#
## Configure WebSphere Liberty
#RUN /opt/ibm/wlp/bin/server create \
#    && rm -rf $WLP_OUTPUT_DIR/.classCache
#EXPOSE 9080 9443

# CMD ["/opt/ibm/wlp/bin/server", "run", "defaultServer"]

#dpkg-reconfigure dash
#dpkg-reconfigure -p critical dash

RUN echo "dash dash/sh boolean false" | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

ENV TINI_VERSION 0.9.0
ENV TINI_SHA fa23d1e20732501c3bb8eeeca423c89ac80ed452

# Use tini as subreaper in Docker container to adopt zombie processes 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static /bin/tini 
RUN chmod +x /bin/tini \
  && echo "$TINI_SHA  /bin/tini" | sha1sum -c -

COPY WAS8.5.5_1 /tmp/was
COPY Install_Mgr_v1.6.2 /tmp/installer
COPY WASv85.base.install.xml /tmp/WASv85.base.install.xml


#RUN /tmp/installer/installc -acceptLicense -showProgress input /tmp/WASv85.base.install.xml

COPY createprofile.txt /tmp/createprofile.txt

#RUN /opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -response /tmp/createprofile.txt


#RUN /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startServer.sh server1

#RUN sleep 10s

COPY deploy.py /tmp/deploy.py
COPY maximo.ear /tmp/maximo.ear

#RUN /opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/deploy.py

#RUN rm -f /tmp/WASv85.base.install.xml \
#    && rm -r -f /tmp/was 
#    && rm -r -f /tmp/installer 
#   && rm /tmp/deploy.py \
#   && rm /tmp/maximo.ear
#   && rm -f /tmp/createprofile.txt \

COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh
ENTRYPOINT ["/bin/tini", "--","/docker-entrypoint.sh"]





