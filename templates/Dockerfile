FROM centos:centos7

# Configure environment
ENV CONDA_DIR=/opt/conda \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    NB_USER=ops

ENV PATH=$CONDA_DIR/bin:$PATH \
	HOME=/home/$NB_USER

RUN yum -y update \
	&& yum -y install sudo curl bzip2 git \
	&& yum -y clean all

# create ops user
RUN useradd -ms /bin/bash ops \
    && usermod -aG wheel ops \
    && echo "" >> /etc/sudoers \
    && echo "ops ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && echo ""

RUN curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
	&& bash /tmp/miniconda.sh -bfp $CONDA_DIR \
	&& rm -rf /tmp/miniconda.sh \
	&& conda install -y python=3 \
	&& conda install -y nb_conda_kernels \
	&& conda update conda

RUN mkdir -p /data/work \
    && chown -R ops:ops /data/work

USER ops

RUN cd $HOME \
    && git clone https://github.com/hysds/notebook_pge_wrapper.git \
    && cd notebook_pge_wrapper \
    && sudo $CONDA_DIR/bin/pip install -e .

# copy your repo into the docker container
################################################
# COPY . /home/ops/<repo name>
################################################

WORKDIR $HOME

CMD ["/bin/bash", "--login"]
