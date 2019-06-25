# Final image
FROM gbs-iga-docker.artifactory.swg-devops.com/duzhiguo/ibm-was-basic:8.5.5.15

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