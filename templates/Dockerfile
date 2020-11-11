#FROM centos:7
FROM centos/python-38-centos7:latest
#FROM centos:centos7

#RUN useradd -ms /bin/bash ops

#RUN yum groupinstall "Development Tools" \
#    && yum clean all

#USER ops

RUN git clone https://github.com/hysds/notebook_pge_wrapper.git
RUN cd notebook_pge_wrapper \
    && pip install -e .

#WORKDIR /home/ops
CMD ["/bin/bash", "--login"]
