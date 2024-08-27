# SN_atlas

## Cellbender

Due to issues with where the checkpoint file is written, from the cellbender folder use the command

`<sbatch cellbender_array.sh>'

Until cellbender takes in the argument for writting the checkpoint file to somewhere besides the directory the sbatch command is executed this will have to work outside of the larger snakemake file.