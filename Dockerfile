FROM ubuntu:20.04

RUN apt-get update

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /tmp/

ADD https://downloads.eggplantsoftware.com/downloads/Linux/Eggplant_ubuntu.tgz .

RUN tar -xf Eggplant_ubuntu.tgz

RUN dpkg -i /tmp/Eggplant_debian/Eggplant22.2.0.deb

ADD http://ppa.launchpad.net/linuxuprising/libpng12/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~focal_amd64.deb .
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN apt-get install python3.9 -y
RUN add-apt-repository "deb http://mirrors.kernel.org/ubuntu/ xenial main"
RUN apt-get update
RUN apt-get install libssl1.0.0 libnettle6 libhogweed4 -y
RUN dpkg -i libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~focal_amd64.deb
RUN apt-get install -y libxtst6 libxcb-render-util0 libxcb-shm0-dev libavahi-common-dev libavahi-client-dev libxt6 libjbig-dev libgomp1 libgmp10 libidn11

RUN rm /tmp/Eggplant_debian/Eggplant22.2.0.deb
RUN rm libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~focal_amd64.deb

#RUN /usr/local/bin/runscript -driveport 5400 -BonjourDiscoveryEnabled 0 -RedirectOutputToFile Yes -GSBackend libgnustep-back-headless -LicenserHost 172.31.0.226

ADD config_dai.ini /eggplant/
ADD create_agent.py /eggplant/

CMD ["/eggplant/create_agent.py"]

ENTRYPOINT ["python3"]
