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
# Set SPACK_ROOT explicitly because Spack detects qemu-x86_64-static when
# this amd64 image is built under emulation on Apple Silicon.
ENV SPACK_ROOT=/home/spack/spack
ENV PATH=/home/spack/spack/bin:$PATH

RUN git clone --depth=2 --branch=releases/v1.1 https://github.com/spack/spack.git ${SPACK_ROOT}

COPY spack_setup.sh /etc/profile.d/spack_setup.sh
COPY modules.yaml ${SPACK_ROOT}/etc/spack/modules.yaml

USER spack
RUN cd ${SPACK_ROOT} && \
    . ${SPACK_ROOT}/share/spack/setup-env.sh && \
    spack repo update builtin --tag v2025.11.0 && \
    spack tutorial -y && \
    spack bootstrap now && \
    spack compiler find && \
    spack uninstall -ay && \
    spack config add "modules:default:enable:[tcl]" && \
    spack install lmod python openmpi && \
    . $(spack location -i lmod)/lmod/lmod/init/bash && \
    spack module tcl refresh --delete-tree -y
