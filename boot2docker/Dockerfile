FROM boot2docker/boot2docker
ADD . $ROOTFS/data/
WORKDIR /

RUN git clone https://git.kernel.org/pub/scm/linux/kernel/git/shemminger/bridge-utils.git && \
    cd bridge-utils && \
    autoconf && \
    ./configure && \
    make && \
    make DESTDIR=$ROOTFS install && \
    ln -s ../local/sbin/brctl $ROOTFS/usr/sbin/brctl

RUN curl -fL https://www.kernel.org/pub/linux/utils/util-linux/v2.29/util-linux-2.29.tar.xz | tar -C / -xJ && \
    cd util-linux-2.29 && \
    ./configure && \
    make nsenter && \
    cp nsenter $ROOTFS/usr/local/bin

RUN /tmp/make_iso.sh
CMD ["cat", "boot2docker.iso"]

