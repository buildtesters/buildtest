FROM spack/tutorial:ecp21

# upgrade git version see https://github.com/actions/checkout/issues/238 and https://phoenixnap.com/kb/add-apt-repository-command-not-found-ubuntu
USER root
RUN apt update && \
    apt-get update && \
    # need to install following package in-order to get apt-get-repository
    apt install -y software-properties-common && \
    add-apt-repository ppa:git-core/ppa -y && \
    apt-get update && \
    apt-get install git -y

USER spack
RUN git clone https://github.com/spack/spack ~/spack

COPY /config.yaml /home/spack/spack/etc/spack/config.yaml
COPY /spack_setup.sh /etc/profile.d/spack_setup.sh
COPY /modules.yaml   /home/spack/spack/etc/spack/modules.yaml
COPY /compilers.yaml /home/spack/spack/etc/spack/compilers.yaml

USER spack
RUN cd ~/spack && \
    git checkout releases/v0.16 && \
    . ~/spack/share/spack/setup-env.sh && \
    spack tutorial -y && \
    spack install lmod && \
    spack install python && \
    spack install gcc@6.5.0 gcc@8.3.0 && \
    echo "source /etc/profile" >> ~/.bashrc

