#!/bin/bash

# Benjamin Adam Catching
# NIA-CARD/Data Tecnica
# 2024-08-22

# Find the sample locations where CellRanger has been run
input_file_locs=$(echo /data/CARD_singlecell/Brain_atlas/SN_Multiome/*/Multiome/*/outs/)
output_file_base=/data/CARD_singlecell/SN_atlas/cellbender

# Rewrite the file with your changes
rm $output_file_base/cellbender.swarm
touch $output_file_base/cellbender.swarm

# Turn list of Cellranger output folders into a list of locations
input_array=(`echo ${input_file_locs}`);

for i in $(seq 1 $((${#input_array[@]}-1))); do
    # Write all Cellranger output locations
    echo ${input_array[i]}filtered_feature_bc_matrix.h5 >> /data/CARD_singlecell/SN_atlas/cellbender/all_cellranger_file_locs.txt
done

# Read in the sample sheet for each batch
cat /data/CARD_singlecell/SN_atlas/data/SNsamples.csv
while IFS="," read -r Sample_ID Homogenizing_batch Library_batch Sequencing_batch Repeated Use_batch Age \
PMI Ethnicity Race Brain_bank Short Diagnosis
do
    # Filter for only the batches where the batch it is in matches the right batch to use
    for i in $(seq 1 $((${#input_array[@]}-1))); do
        if [[ ${input_array[i]} == *$Use_batch*$Sample_ID* ]]; then
            echo "batch"$Use_batch"*"$Sample_ID": is in : "${input_array[i]}
            echo "module load ; cellbendercellbender remove-background --input "\
            ${input_array[i]}filtered_feature_bc_matrix.h5\
            " --output "$output_file_base${input_array[i]:61:20}"cellbender_gex_counts.h5 --checkpoint \
            $output_file_base${input_array[i]:61:20}ckpt.tar.gz --localcores=1 --localmem=32 " >>\
            $output_file_base/cellbender.swarm
        #else
        #echo "batch"$Use_batch"/"$Sample_ID": is in : "${input_array[i]}
        fi
    done
done < /data/CARD_singlecell/SN_atlas/data/SNsamples.csv

# Iterate through the list of locations
#for i in $(seq 1 $((${#input_array[@]}-1))); do
#echo ${input_array[i]}

#
#echo ${input_array[i]}
#done
