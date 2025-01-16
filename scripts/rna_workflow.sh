#!/bin/sh

#SBATCH --cpus-per-task=64
#SBATCH --mem=300g
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:v100x:4
#SBATCH --output=logs/rna_workflow-%j.out 
#SBATCH --partition=gpu

source /data/$USER/conda/etc/profile.d/conda.sh && source /data/$USER/conda/etc/profile.d/mamba.sh

conda activate single_cell_gpu

srun python scripts/rna_workflow.py $1
