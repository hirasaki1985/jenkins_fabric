FROM jenkins

USER root
#RUN apt-get update && apt-get install -y ruby make more-thing-here
RUN apt-get update -y

## install pip
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python

## install fabric
RUN pip install fabric

## ssh setting
USER jenkins
WORKDIR /var/jenkins_home
RUN mkdir .ssh/
COPY .ssh/ .ssh/

USER root
WORKDIR /var/jenkins_home
RUN chmod 700 .ssh
RUN find .ssh/ -type f -exec chmod 400 {} \; 
RUN find .ssh/ -type d -exec chmod 700 {} \;
RUN chown -R jenkins:jenkins .ssh

USER jenkins






