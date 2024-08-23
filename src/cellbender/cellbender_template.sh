#/bin/sh

#SBATCH -o cellbender.out
#SBATCH -e cellbender.err
#SBATCH --mem=32g
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL,TIME_LIMIT_50

module load cellbender


# Define the location of the input and output (for later looping)
input_location=$1
output_location=$2
checkpoint_location=$3

# Run the remove-background command
cellbender remove-background --input $input_location --output $output_location --checkpoint $checkpoint_location--fpr 0 --cuda
