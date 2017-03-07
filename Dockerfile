FROM ubuntu:16.04

COPY /build/* /

RUN echo "deb http://ppa.launchpad.net/stebbins/handbrake-releases/ubuntu xenial main ">/etc/apt/sources.list.d/handbreak.list && apt-get update && apt-get install --allow-unauthenticated -y python-pip handbrake-cli libssl1.0.0 libexpat1 libavcodec-ffmpeg56 libgl1-mesa-glx unzip 
#libavcodec-ffmpeg-extra56


ADD https://github.com/JasonMillward/Autorippr/archive/v1.7.0.zip autorippr-1.7.0.zip
ADD "http://downloads.sourceforge.net/project/filebot/filebot/FileBot_4.7.2/filebot_4.7.2_amd64.deb?r=http%3A%2F%2Fwww.filebot.net%2F&ts=1473715379&use_mirror=freefr" filebot_4.7.2_amd64.deb
RUN pip install tendo pyyaml peewee
RUN unzip /autorippr-1.7.0.zip
RUN dpkg -i filebot_4.7.2_amd64.deb

ADD settings.example.cfg /Autorippr-1.7.0/settings.cfg

ENTRYPOINT ["python", "/Autorippr-1.7.0/autorippr.py"]

