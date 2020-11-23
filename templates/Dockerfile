FROM hysds/pge-base:latest

ENV HOME=/home/ops \
    CONDA_DIR=/opt/conda

USER root
RUN $CONDA_DIR/bin/conda install -y nb_conda_kernels

USER ops
RUN $HOME/verdi/bin/pip install 'ipykernel<5.0.0'

RUN cd $HOME \
    && git clone https://github.com/hysds/notebook_pge_wrapper.git \
    && cd notebook_pge_wrapper \
    && $HOME/verdi/bin/pip install -e .

# copy your repo into the docker container
################################################
#COPY . $HOME/<repo name>
################################################

WORKDIR $HOME

CMD ["/bin/bash", "--login"]
