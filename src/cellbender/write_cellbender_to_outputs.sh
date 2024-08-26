#!/bin/bash

# Benjamin Adam Catching
# NIA-CARD/Data Tecnica
# 2024-08-22

"""
This is the working file for creating a swarm job that processes Cellranger->Cellbender.
Currently the main issue is that the checkpoint file only writes to the directory from 
which the command was executed. Workaround is using cellbender_array.sh, as a Sbatch 
array job. When Cellbender is updated such that the checkpoint file can be written 
to another folder this script will work. 
"""


# Find the sample locations where CellRanger has been run
input_file_base=/data/CARD_singlecell/Brain_atlas/SN_Multiome/
input_file_locs=$(echo /data/CARD_singlecell/Brain_atlas/SN_Multiome/*/Multiome/*/outs/)
# Define where the output files will be
output_file_base=/data/CARD_singlecell/SN_atlas/cellbender

# Rewrite the file with your changes
rm $output_file_base/cellbender.swarm
#touch $output_file_base/cellbender.swarm

# Turn list of Cellranger output folders into a list of locations
input_array=(`echo ${input_file_locs}`);

#for i in $(seq 1 $((${#input_array[@]}-1))); do
#    # Write all Cellranger output locations
#    echo ${input_array[i]}filtered_feature_bc_matrix.h5 >> \
#    /data/CARD_singlecell/SN_atlas/cellbender/all_cellranger_file_locs.txt
#done

# Read in the sample sheet for each batch
#cat /data/CARD_singlecell/SN_atlas/data/SNsamples.csv
while IFS="," read -r Sample_ID Homogenizing_batch Library_batch Sequencing_batch Repeated Use_batch Age \
PMI Ethnicity Race Brain_bank Short Diagnosis
do
    # Create directories of the samples (ONLY RUN ONCE)
    # mkdir $output_file_base"/"$Sample_ID"-ARC"

    # Inititiate the script file
    touch $output_file_base"/"$Sample_ID"-ARC/cellbender.sh"
    # Write out the Cellranger command to this bash script
    echo "module load cellbender; module load CUDA; cellbender remove-background --input "\
    $input_file_base"batch"$Use_batch"/Multiome/"$Sample_ID"-ARC/outs/raw_feature_bc_matrix.h5"\
    " --output "$output_file_base"/"$Sample_ID"-ARC/cellbender_gex_counts.h5 --checkpoint "\
    $output_file_base"/"$Sample_ID"-ARC/ckpt.tar.gz --fpr 0 --cuda" >>\
    $output_file_base"/"$Sample_ID"-ARC/cellbender.sh"

    # Holdover when all files were written to one swarm file
    #$output_file_base"/cellbender.swarm"
done < <(tail -n +2 /data/CARD_singlecell/SN_atlas/data/SNsamples.csv)

# Repeat the cellbender command one last time (fix this later)

# Creat the directory of the file sample
# mkdir $output_file_base"/"$Sample_ID"-ARC"
# Initiate the file
touch $output_file_base"/"$Sample_ID"-ARC/cellbender.sh"
# Write out the Cellranger command to the bash script
echo "module load cellbender; module load CUDA; cellbender remove-background --input "\
$input_file_base"batch"$Use_batch"/Multiome/"$Sample_ID"-ARC/outs/raw_feature_bc_matrix.h5"\
" --output "$output_file_base"/"$Sample_ID"-ARC/cellbender_gex_counts.h5 --checkpoint "\
$output_file_base"/"$Sample_ID"-ARC/ckpt.tar.gz --fpr 0 --cuda " >>\
$output_file_base"/cellbender.swarm"
#$output_file_base"/"$Sample_ID"-ARC/cellbender.sh"