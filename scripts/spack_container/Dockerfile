FROM ghcr.io/spack/tutorial:sc23

# upgrade git version see https://github.com/actions/checkout/issues/238 and https://phoenixnap.com/kb/add-apt-repository-command-not-found-ubuntu
USER root
RUN apt update && \
    apt-get update && \
    # need to install following package in-order to get apt-get-repository
    apt install -y software-properties-common && \
    add-apt-repository ppa:git-core/ppa -y && \
    apt-get update && \
    apt-get install -y tcsh zsh && \
    apt-get install -y git 

USER spack
RUN git clone --depth=100 --branch=releases/v0.21 https://github.com/spack/spack.git ~/spack

COPY /spack_setup.sh /etc/profile.d/spack_setup.sh
COPY /modules.yaml   /home/spack/spack/etc/spack/modules.yaml
COPY /compilers.yaml /home/spack/spack/etc/spack/compilers.yaml

USER spack
RUN  cd ~/spack && \
    . ~/spack/share/spack/setup-env.sh && \
    spack tutorial -y && \
    spack install lmod python gcc@12.3.0 openmpi mpich && \
    . $(spack location -i lmod)/lmod/lmod/init/bash \
    spack module tcl refresh --delete-tree -y

