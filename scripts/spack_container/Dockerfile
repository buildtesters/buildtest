FROM spack/tutorial:ecp21

RUN git clone https://github.com/spack/spack ~/spack && \
    cd ~/spack && \
    git checkout releases/v0.16 && \
    . ~/spack/share/spack/setup-env.sh && \
    spack tutorial -y && \
    spack install lmod && \
    spack install python && \
    spack install gcc@6.5.0 gcc@8.3.0 && \
    echo ". ~/spack/share/spack/setup-env.sh" >> ~/.bashrc && \
    echo ". $(spack location -i lmod)/lmod/lmod/init/bash" >> ~/.bashrc

CMD ["bash"]
