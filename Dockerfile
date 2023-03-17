# SQL Server Command Line Tools
FROM mcr.microsoft.com/azureml/curated/lightgbm-3.2-ubuntu18.04-py37-cpu:45

LABEL maintainer="SQL Server Engineering Team"

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
	curl apt-transport-https debconf-utils gnupg2

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers and tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"


RUN apt-get -y install locales \
    && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

RUN apt-get update && \
  apt-get install -y --no-install-recommends python3 python3.7-distutils && \
  ln -sf /usr/bin/python3 /usr/bin/python


# install dependencies
RUN pip install --upgrade pip==20.1.1

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip freeze
RUN conda --version
RUN python3 --version

CMD /bin/bash