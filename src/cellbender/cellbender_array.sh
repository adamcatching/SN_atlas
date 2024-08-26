#!/bin/bash
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=32G
#SBATCH --time 6:00:00
#SBATCH --array=1-246
#SBATCH --partition=gpu
#SBATCH --gres=gpu:k80:1
#SBATCH --array=1-246

# Load modules
module load cellbender
module load CUDA

# Define the directories to run cell bender within
output_file_base=$(echo /data/CARD_singlecell/SN_atlas/cellbender/*-*/)
# Convert the locations of the directories to an array
out_dirs=(`echo ${output_file_base}`);

# Iterate through the array of sample directories
for i in $(seq 1 $SLURM_ARRAY_TASK_ID); do
    # Move to the sample directory, this is crucial or the checkpoint file won't be written correctly!
    cd ${out_dirs[i]}
    # Run Cellbender with the Cellranger output file, use CUDA or this will take forever
    cellbender remove-background --input raw_feature_bc_matrix.h5  --output cellbender_gex_counts.h5 --fpr 0 --cuda
done