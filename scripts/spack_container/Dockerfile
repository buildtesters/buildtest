FROM ghcr.io/spack/tutorial:sc25

ARG DEBIAN_FRONTEND=noninteractive

# The SC25 tutorial image targets Ubuntu 22.04/x86_64. Keep the build
# environment aligned with the tutorial while adding the shells/tools used
# by buildtest's Spack regression tests.
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends git tcsh zsh && \
    rm -rf /var/lib/apt/lists/*

USER spack

# Follow the Spack version and setup procedure used by the SC25 tutorial.
RUN git clone --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git ~/spack

COPY spack_setup.sh /etc/profile.d/spack_setup.sh
COPY modules.yaml /home/spack/spack/etc/spack/modules.yaml

USER spack
RUN cd ~/spack && \
    . ~/spack/share/spack/setup-env.sh && \
    spack repo update builtin --tag v2025.11.0 && \
    spack tutorial -y && \
    spack bootstrap now && \
    spack compiler find && \
    spack install lmod python openmpi mpich && \
    . $(spack location -i lmod)/lmod/lmod/init/bash && \
    spack module tcl refresh --delete-tree -y
