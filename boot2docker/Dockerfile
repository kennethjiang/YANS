FROM boot2docker/boot2docker
ADD . $ROOTFS/data/
WORKDIR /

RUN git clone https://git.kernel.org/pub/scm/linux/kernel/git/shemminger/bridge-utils.git && \
    cd bridge-utils && \
    autoconf && \
    ./configure && \
    make && \
    make DESTDIR=$ROOTFS install

RUN /tmp/make_iso.sh
CMD ["cat", "boot2docker.iso"]

