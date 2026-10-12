# Data & Reproducibility Guide

Raw data is not committed to this repository (licensing and `.gitignore` rules).
The analysis uses the **Speed Dating Experiment** dataset (Ray Fisman and Sheena Iyengar, Columbia Business School), mirrored on Kaggle as `annavictoria/speed-dating-experiment`.

## Option 1: Kaggle (recommended)

1. Open the notebook on Kaggle.
2. **+ Add Input** → search for `Speed Dating Experiment` (slug `annavictoria/speed-dating-experiment`).
3. The notebook reads `/kaggle/input/datasets/annavictoria/speed-dating-experiment/Speed Dating Data.csv`.

## Option 2: Run locally

1. Download the dataset from Kaggle.
2. Save the main file as `data/Speed_Dating_Data.csv` (the notebook looks for this exact name).
3. Run `pip install -r requirements.txt`, then execute the notebook top to bottom.

The file is encoded as ISO-8859-1.
