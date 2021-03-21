FROM cae-artifactory.jpl.nasa.gov:16001/gov/nasa/jpl/nisar/sds/pcm/nisar_ade:latest

ENV HOME=/home/jovyan \
    CONDA_DIR=/opt/conda

USER root
RUN $CONDA_DIR/bin/conda install -y nb_conda_kernels
RUN $CONDA_DIR/bin/pip install 'ipykernel<5.0.0'

RUN cd $HOME \
    && git clone https://github.com/hysds/notebook_pge_wrapper.git \
    && cd notebook_pge_wrapper \
    && $CONDA_DIR/bin/pip install -e .

USER jovyan

# copy your repo into the docker container
################################################
#COPY . $HOME/<repo name>
################################################

WORKDIR $HOME

CMD ["/bin/bash", "--login"]
