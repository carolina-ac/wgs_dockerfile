# Data Analysis Pipeline with Docker

This repository contains a pipeline for analyzing whole-genome sequencing (WGS) data, including quality control, adapter trimming, genome assembly, and quality assessment, all executed within a Docker container.

## Steps of the Analysis

1. **Quality Control (FastQC)**: FastQC is used to assess the quality of raw sequencing data.
2. **Adapter Removal (Trimmomatic)**: Trimmomatic is used to remove adapters and filter low-quality reads.
3. **Combining Filtered Reads**: Filtered reads from different sequencing runs are combined into a single file.
4. **Genome Assembly (SPAdes)**: SPAdes is used to assemble the genome from the filtered reads.
5. **Quality Assessment (QUAST)**: QUAST is used to assess the quality of the assembled genome.

## Prerequisites

Make sure you have Docker installed on your system. You can install Docker on Ubuntu with the following commands:

```bash
# Update the system and install Docker
sudo apt-get update
sudo apt-get install -y docker.io

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
```

# Using the Dockerfile

I have provided a Dockerfile that contains all the dependencies required for the pipeline. Here's how to build and run the Docker container.

## Step 1: Build the Docker Image

```
git clone https://github.com/your-username/wgs_dockerfile.git
cd wgs-wgs_dockerfile
```

### Build the Docker image:

```
docker build -t wgs_pipeline:latest .
```

## Step 2: Running the Pipeline

Once the image is built, you can run the container and execute the WGS pipeline. First, make sure your WGS data files and TruSeq3-PE.fa adapter file are in the working directory.

### To run the container, use the following command:

```
docker run -v /path/to/your/data:/data -it wgs_pipeline:latest bash
```
### This command will:

* Mount your local data directory to the /data directory inside the container.
* Start an interactive terminal session inside the container.

## Step 3: Execute the Pipeline
Once inside the container, you can run the Python script that performs the analysis:

```
python /data/wgs_analysis.py
```

## This will:

* Run FastQC for quality control.
* Use Trimmomatic to remove adapters and filter low-quality reads.
* Combine the filtered paired-end reads.
* Assemble the genome using SPAdes.
* Evaluate the assembly quality using QUAST.

## Output
The results of each step will be saved in respective output directories:

* FastQC results: fastqc_output/
* Trimmed files: paired and unpaired .fq.gz files
* SPAdes assembly: spades_output/
* QUAST quality report: quast_output/

## Additional Notes
* Ensure that your TruSeq3-PE.fa adapter file is in the /data directory.
* If you need to change any configuration, make sure to modify the wgs_analysis.py script.
