#!/bin/bash

#SBATCH --cpus-per-task=64
#SBATCH --mem=2000g
#SBATCH --time=48:00:00
#SBATCH --output=/data/CARD_singlecell/SN_atlas/logs/cistopic_pseudobulk-%j.out 
#SBATCH --partition=largemem

source /data/$USER/conda/etc/profile.d/conda.sh && source /data/$USER/conda/etc/profile.d/mamba.sh

conda activate scenicplus

srun python scripts/cistopic_pseudobulk.py
