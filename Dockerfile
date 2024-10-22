# Use the base image from Miniconda
FROM continuumio/miniconda3:latest

# Update the system and install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    unzip \
    default-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add the necessary conda channels
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

# Install the required packages
RUN conda install -y python=3.8
RUN conda install -y fastqc
RUN conda install -y trimmomatic
RUN conda install -y spades
RUN conda install -y quast

# Set the working directory
WORKDIR /data

# Default command to keep the container running
CMD ["bash"]
