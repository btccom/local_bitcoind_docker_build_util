FROM phusion/baseimage:0.9.19

ENV HOME /root
ENV TERM xterm
CMD ["/sbin/my_init"]

RUN mkdir -p /root/.bitcoin
# RUN mkdir -p /root/scripts

COPY bitcoind /usr/local/bin
COPY libboost_* /usr/lib/x86_64-linux-gnu/
COPY libevent* /usr/lib/x86_64-linux-gnu/
COPY libdb_cxx-4.8.so /usr/lib/
COPY libprometheus-cpp.so /usr/local/lib/
COPY libprotobuf* /usr/local/lib/

RUN ldconfig

EXPOSE 8011

# scripts
ADD opsgenie-monitor-bitcoind.sh   /root/scripts/opsgenie-monitor-bitcoind.sh

# crontab shell
ADD crontab.txt /etc/cron.d/bitcoind

# logrotate
ADD logrotate-bitcoind /etc/logrotate.d/bitcoind


RUN mkdir    /etc/service/bitcoind
ADD run      /etc/service/bitcoind/run
RUN chmod +x /etc/service/bitcoind/run

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*