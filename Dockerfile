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

MAINTAINER Du Zhi Guo <duzhiguo@cn.ibm.com>

RUN apt-get update \
    && apt-get install -y wget unzip vim \
    && rm -rf /var/lib/apt/lists/*

RUN echo "dash dash/sh boolean false" | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

ENV TINI_VERSION 0.9.0
ENV TINI_SHA fa23d1e20732501c3bb8eeeca423c89ac80ed452

# Use tini as subreaper in Docker container to adopt zombie processes 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static /bin/tini 
RUN chmod +x /bin/tini \
  && echo "$TINI_SHA  /bin/tini" | sha1sum -c -

COPY WAS8.5.5_1 /tmp/WAS8.5.5_1
COPY WASFP011 /tmp/was
COPY java8 /tmp/java
COPY Install_Mgr_v1.6.2 /tmp/installer
COPY WASv85.base.install.xml /tmp/WASv85.base.install.xml

COPY createprofile.txt /tmp/createprofile.txt

COPY deploy.py /tmp/deploy.py
COPY maximo.ear /tmp/maximo.ear

COPY docker-entrypoint.sh /
COPY install.sh /tmp/install.sh
COPY update.sh /tmp/update.sh
COPY updateWar.py /tmp/updateWar.py
COPY sharedLib.py /tmp/sharedLib.py
COPY datasource.py /tmp/datasource.py
COPY db2jcc.jar /tmp/SQLLIB/java/db2jcc.jar

RUN chmod 755 /docker-entrypoint.sh && chmod 755 /tmp/*.sh

ENTRYPOINT ["/bin/tini", "--","/docker-entrypoint.sh"]
CMD ["/bin/bash"]





