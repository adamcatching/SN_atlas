source /data/$USER/conda/etc/profile.d/conda.sh && source /data/$USER/conda/etc/profile.d/mamba.sh

conda activate snapATAC2

# Astro
pyGenomeTracks --tracks /data/CARD_singlecell/SN_atlas/scripts/pyGenomeTracks_marker_genes.ini \
               --region 18:26,852,680-26,866,350 \
               --width 5 \
               -o /data/CARD_singlecell/SN_atlas/figures/astro_marker_tracks.svg

# EC
pyGenomeTracks --tracks /data/CARD_singlecell/SN_atlas/scripts/pyGenomeTracks_marker_genes.ini \
               --region 22:19,523,030-19,524,410 \
               --width 5 \
               -o /data/CARD_singlecell/SN_atlas/figures/EC_marker_tracks.svg