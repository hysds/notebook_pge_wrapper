FROM centos:centos7

# Configure environment
ENV CONDA_DIR=/opt/conda \
    # SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

ENV PATH=$CONDA_DIR/bin:$PATH \
	HOME=/home/$NB_USER

RUN yum -y update \
	&& yum -y install curl bzip2 git \
	&& curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
	&& bash /tmp/miniconda.sh -bfp $CONDA_DIR \
	&& rm -rf /tmp/miniconda.sh \
	&& conda install -y python=3 \
	&& conda install nb_conda_kernels \
	&& conda update conda

RUN git clone https://github.com/hysds/notebook_pge_wrapper.git
RUN cd notebook_pge_wrapper \
    && pip install -e .

CMD ["/bin/bash", "--login"]
