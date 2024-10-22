import subprocess
import os

# Updated list of files
files = [
    "WGS_0131_CKDN240007558-1A_AA7YLSDXCX_L1_1.fq.gz",
    "WGS_0131_CKDN240007558-1A_AA7YLSDXCX_L1_2.fq.gz",
    "WGS_0131_CKDN240007558-1A_BA7YLSDXCX_L1_1.fq.gz",
    "WGS_0131_CKDN240007558-1A_BA7YLSDXCX__L1_2.fq.gz"
]

# Function to execute terminal commands
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('latin1', errors='ignore')
    stderr = stderr.decode('latin1', errors='ignore')
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
    else:
        print(f"Command executed successfully: {command}")

# Step 1: Quality Control with FastQC
fastqc_command = "fastqc " + " ".join(files)
run_command(fastqc_command)

# Step 2: Filtering and Adapter Removal with Trimmomatic
sample_pairs = [
    ("WGS_0131_CKDN240007558-1A_AA7YLSDXCX_L1", "AA7YLSDXCX_L1"),
    ("WGS_0131_CKDN240007558-1A_BA7YLSDXCX_L1", "BA7YLSDXCX_L1")
]

for sample, suffix in sample_pairs:
    trimmomatic_command = f"trimmomatic PE -phred33 {sample}_1.fq.gz {sample}_2.fq.gz " \
                          f"{sample}_1_paired.fq.gz {sample}_1_unpaired.fq.gz " \
                          f"{sample}_2_paired.fq.gz {sample}_2_unpaired.fq.gz " \
                          "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"
    run_command(trimmomatic_command)

# Step 3: Combine filtered files
combined_1 = "combined_1_paired.fq.gz"
combined_2 = "combined_2_paired.fq.gz"

with open(combined_1, 'wb') as outfile_1:
    for sample, _ in sample_pairs:
        with open(f"{sample}_1_paired.fq.gz", 'rb') as infile_1:
            outfile_1.write(infile_1.read())

with open(combined_2, 'wb') as outfile_2:
    for sample, _ in sample_pairs:
        with open(f"{sample}_2_paired.fq.gz", 'rb') as infile_2:
            outfile_2.write(infile_2.read())

# Step 4: Assembly with SPAdes
spades_command = f"spades.py --isolate -1 {combined_1} -2 {combined_2} -o spades_output --threads 4 --memory 8"
run_command(spades_command)

# Step 5: Quality Assessment with QUAST
quast_command = "quast.py -o quast_output spades_output/contigs.fasta"
run_command(quast_command)
