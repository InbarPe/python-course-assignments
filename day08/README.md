### 📄 2-Photon Calcium Imaging Analysis – README
## 📌 Overview

This project performs basic processing and analysis of synthetic 2-photon (2p) calcium imaging data.
The dataset contains:

* 20 neurons

* Neuropil signal per neuron

* ~10-minute recording

* 30 Hz sampling rate

* Repeated stimulus every 30 seconds for 2 seconds

* 18 trials, each trial contains 30 seconds and 1 stimulus

The analysis pipeline performs neuropil subtraction, ΔF/F calculation, trial segmentation, and visualization of neural responses.

## 📁 Input Files

The script expects two CSV files in the project directory:

1. 2p_cells_data.csv: Raw fluorescence signal (neurons)
2. 2p_neuropil_data.csv: Neuropil traces for each neuron

Both files should have shape the same shape.
Here: (20, 16383) → 20 neurons, 16,383 samples.

*Update* the file paths in the script if needed.

## 🔧 Code Structure
# 1. Neuropil subtraction
    
    processed_cells = cells_data - 0.7 * neu_data
   
Baseline is restored per neuron using the median neuropil value.

# 2. Trial segmentation

Each recording is split into trials:

* 30s per trial × 30Hz = 900 samples/trial

# 3. Baseline alignment

The last 2s of the previous trial are added as baseline for the next.

# 4. ΔF/F computation

For every cell × trial:
    
    ΔF/F = (F - F0) / F0
    F0 = mean of first 2 seconds of data
    

# 5. Response comparison

The recording is divided into:

* First half → strong responses

* Second half → adapted/weaker responses

Cells are sorted by response strength.

# 6. Visualization

* Heatmaps of all cells (first vs second half)

* Example excited, inhibited, and non-responsive cells

* Mean response plots with stimulus window markers

Output figures are saved automatically.

## 📊 Output Files

The script saves figures such as:

1. all_cells_mean_heatmap.png: Population activity, first vs second half
2. excited_cell_example.png: Example neuron with increased activity
3. inhibited_cell_example.png: Example neuron with suppressed activity
4. no_response_cell_example.png: Example neuron with no response

## ▶️ How to Run

Install dependencies:

    
    pip install numpy 
    pip install pandas 
    pip install matplotlib 
    pip install seaborn
    

Run the script:

    
    python your_script_name.py
    

Check the output images in the project folder.

## 📌 Requirements

* Python 3.8+

* NumPy

* Pandas

* Matplotlib

* Seaborn
