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

FROM ubuntu:16.04 as builder

RUN apt-get update \
    && apt-get install -y wget unzip vim \
    && rm -rf /var/lib/apt/lists/*
# resolve - can not start profile
RUN echo "dash dash/sh boolean false" | debconf-set-selections && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

WORKDIR /tmp/wasinstall/
COPY was.repo.9000.base.zip \
    was.repo.9000.ihs.zip \
    was.base.9.xml \
    agent.installer.lnx.gtk.x86_64_1.8.5.zip \
    ibm-java-sdk-8.0-5.36-linux-x64-installmgr.zip \
    9.0.0-WS-WAS-FP009.zip \
    was.repo.9000.plugins.zip \
    ./

RUN cd /tmp/wasinstall/ && \
  unzip agent.installer.lnx.gtk.x86_64_1.8.5.zip -d installer && \
  /tmp/wasinstall/installer/installc -acceptLicense -showProgress input /tmp/wasinstall/was.base.9.xml && \
  rm -rf /tmp/wasinstall/

# Final image
FROM ubuntu:16.04

COPY --from=builder /opt/IBM /opt/IBM

COPY deploy.py createprofile.txt docker-entrypoint.9.sh /

RUN apt-get update \
    && apt-get install -y vim \
    && rm -rf /var/lib/apt/lists/*
# resolve - can not start profile
RUN echo "dash dash/sh boolean false" | debconf-set-selections && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

ENV TINI_VERSION 0.9.0
ENV TINI_SHA fa23d1e20732501c3bb8eeeca423c89ac80ed452

# Use tini as subreaper in Docker container to adopt zombie processes 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static /bin/tini 
RUN chmod +x /bin/tini \
  && echo "$TINI_SHA  /bin/tini" | sha1sum -c \
  && /opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -response /createprofile.txt \
  && chmod 755 /docker-entrypoint.9.sh

ENTRYPOINT ["/bin/tini", "--","/docker-entrypoint.9.sh"]




