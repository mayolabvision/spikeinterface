#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --time=0-09:00:00
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:2
#SBATCH --cluster=gpu
#SBATCH --partition=a100
#SBATCH --constraint=80g
#SBATCH --job-name=si
#SBATCH --error=/ix1/pmayo/kilosort/outfiles/out_%A.out
#SBATCH --output=/ix1/pmayo/kilosort/outfiles/out_%A.out
#SBATCH --mail-type=end,fail
#SBATCH --mail-user=knoneman@pitt.edu

# INPUTS = FILENAME, IMEC
module purge
conda activate /ihome/pmayo/knoneman/.conda/envs/kilosort

SPIKEGLX_PATH="/ix1/pmayo/lab_NHPdata/${1}"
IMEC=${2}
DRIFT_PRESET="dredge"
PLOT_FIGS=True

echo "SPIKEGLX_PATH= $SPIKEGLX_PATH"
echo "IMEC= $IMEC"
echo "DRIFT_PRESET= $DRIFT_PRESET"
echo "PLOT_FIGS= $PLOT_FIGS"

export OPENBLAS_NUM_THREADS=1

# Run the SI_H2P function from the imported file
python -c "import sys; sys.path.append('/ihome/pmayo/knoneman/Packages/Kilosort4'); from SI_H2P import si_h2p; si_h2p('$SPIKEGLX_PATH', IMEC=int('$IMEC'), drift_preset='$DRIFT_PRESET', plot_figs=('$PLOT_FIGS' == 'True'))"

echo "DONE"

crc-job-stats
