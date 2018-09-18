FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python-virtualenv build-essential pkg-config libc6-dev libssl-dev libexpat1-dev libavcodec-dev libgl1-mesa-dev 

ADD http://www.makemkv.com/download/makemkv-oss-1.12.3.tar.gz /src/
ADD http://www.makemkv.com/download/makemkv-bin-1.12.3.tar.gz /src/

RUN tar xf /src/makemkv-bin-1.12.3.tar.gz -C /src


RUN mkdir /src/makemkv-bin-1.12.3/tmp/
RUN echo 'accepted' > /src/makemkv-bin-1.12.3/tmp/eula_accepted

RUN  sed -ie 's#DESTDIR=#DESTDIR=/build#g' /src/makemkv-bin-1.12.3/Makefile

RUN cd /src/makemkv-bin-1.12.3 && make install

RUN tar xf /src/makemkv-oss-1.12.3.tar.gz -C /src

RUN cd /src/makemkv-oss-1.12.3 && ./configure --prefix /build/usr --disable-gui && make install

CMD ["tar", "cz", "/build"]
