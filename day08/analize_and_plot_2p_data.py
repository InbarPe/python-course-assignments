import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import join
from pathlib import Path


BASE_PATH = r'...\Python_Course\python-course-assignments\day08'
# Set recording values
REC_HZ = 30  # Recording frequency in Hz
TRIAL_DURATION = 30  # Duration of each trial in seconds
BASELINE_DURATION = 2  # Baseline length in seconds


def neuropil_subtraction(cells_data, neu_data):
    # Subtract 70% of neu_data from cells_data for each neuron
    processed_data = cells_data - 0.7 * neu_data

    # Calculate the median of neu_data along axis 1 (i.e., for each neuron)
    neu_data_median = np.median(neu_data, axis=1)

    # Add the median of neu_data for each neuron to processed_data
    for i in range(processed_data.shape[0]):
        processed_data.iloc[i, :] += neu_data_median[i]

    return processed_data


def compute_dff(cells_by_trials_bl):
    data_dff = []
    for i in range(len(cells_by_trials_bl)):  # i = cell
        current_cell_dff = []
        for j in range(len(cells_by_trials_bl[0])):  # j = trial
            current_trial = cells_by_trials_bl[i][j]
            current_f0 = np.mean(current_trial[0:BASELINE_DURATION*REC_HZ])
            current_dff = (current_trial - current_f0) / current_f0
            current_cell_dff.append(current_dff)
        data_dff.append(current_cell_dff)

    return data_dff


def separate_trials(processed_cells):
    samples_per_trial = REC_HZ * TRIAL_DURATION
    num_trials = processed_cells.shape[1] // samples_per_trial
    cells_by_trials = []

    for cell in range(len(processed_cells)):
        current_cell_data = []
        for trial in range(num_trials):
            start_idx = trial * samples_per_trial
            end_idx = start_idx + samples_per_trial
            cell_trial_data = processed_cells.iloc[cell, start_idx:end_idx]
            current_cell_data.append(cell_trial_data)
        cells_by_trials.append(current_cell_data)

    return cells_by_trials


def add_baseline(cells_by_trials):
    baseline_length = BASELINE_DURATION * REC_HZ
    cells_by_trials_bl = []
    for i in range(len(cells_by_trials)):  # i = cell
        current_trial_with_baseline = []
        for j in range(1, len(cells_by_trials[0])):  # j = trial
            current_trial = list(cells_by_trials[i][j-1][len(cells_by_trials[i][j-1])-baseline_length:]) + list(cells_by_trials[i][j][:-baseline_length])
            current_trial_with_baseline.append(current_trial)
        cells_by_trials_bl.append(current_trial_with_baseline)

    return cells_by_trials_bl


def separate_data(dff_cells):
    first_half_data = []
    second_half_data = []
    for i in range(len(dff_cells)):  # i = cell
        first_half_trials = dff_cells[i][:len(dff_cells[i])//2]
        second_half_trials = dff_cells[i][len(dff_cells[i])//2:]
        first_half_data.append(first_half_trials)
        second_half_data.append(second_half_trials)

    return first_half_data, second_half_data


def rearrange_cells_and_get_order(data, start_response, end_response):
    # Compute mean values for each array
    mean_values = []
    for arr in data:
        mean_values.append(np.mean(arr[start_response:end_response]))

    # Pair arrays with their mean values and sort
    sorted_data_with_indices = sorted(enumerate(data), key=lambda x: mean_values[x[0]], reverse=True)
    sorted_indices = [idx for idx, _ in sorted_data_with_indices]

    # Extract the sorted arrays
    sorted_arrays = [data[idx] for idx in sorted_indices]

    return sorted_arrays, sorted_indices, mean_values


def rearrange_array(data, cell_order):
    sorted_arrays = [data[idx] for idx in cell_order]

    return sorted_arrays


def calculate_mean(cell_data):
    # Find the maximum length of the arrays
    max_length = max(len(arr) for arr in cell_data)

    # Initialize sum and count arrays
    sum_array = np.zeros(max_length)
    count_array = np.zeros(max_length)

    # Accumulate sums and counts for each index
    for arr in cell_data:
        for i, value in enumerate(arr):
            sum_array[i] += value
            count_array[i] += 1

    # Calculate the average
    mean_array = sum_array / count_array  # Divide sum by count

    return mean_array


def average_cell(data):
    all_cells_mean = []
    for cell in data:
        mean_array = calculate_mean(cell)
        all_cells_mean.append(mean_array)

    return all_cells_mean


def visualize_all_cells_mean(data, conditions):
    plt.figure(figsize=[30, 17])
    plt.subplots_adjust(left=0.1, right=0.9, hspace=0.2, wspace=0.3)
    for i, cond in enumerate(conditions):
        plt.subplot(1, len(conditions), i + 1)
        heatmap = sns.heatmap(data[i], vmin=-0.1, vmax=0.1, cbar=False, cmap='coolwarm')
        plt.axvline(x=2 * REC_HZ, color='black', linewidth=3, alpha=0.7) # Add stimulus start line
        plt.axvline(x=4 * REC_HZ, color='black', linewidth=3, alpha=0.7) # Add stimulus end line
        plt.title(f"{conditions[i]}", fontsize=17)
        if i == 0:
            plt.ylabel('Cell', fontsize=15)
        plt.xlabel('Time (sample points)', fontsize=15)
    cbar_ax = plt.gcf().add_axes([0.92, 0.5, 0.02, 0.4])
    plt.colorbar(mappable=heatmap.collections[0], cax=cbar_ax)
    fig = plt.savefig(join(BASE_PATH, 'all_cells_mean_heatmap.png'))
    plt.close()


def find_response_examples(response_values_first_half):
    excited_cell_ind = None
    inhibited_cell_ind = None
    no_response_cell_ind = None

    for i, response in enumerate(response_values_first_half):
        if response > 0.05 and excited_cell_ind is None:
            excited_cell_ind = i
        elif response < -0.05 and inhibited_cell_ind is None:
            inhibited_cell_ind = i
        elif -0.02 <= response <= 0.02 and no_response_cell_ind is None:
            no_response_cell_ind = i

        if excited_cell_ind is not None and inhibited_cell_ind is not None and no_response_cell_ind is not None:
            break

    return excited_cell_ind, inhibited_cell_ind, no_response_cell_ind


def align_for_plot(data):
    max_length = max(len(arr) for arr in data)
    padded_arrays = [np.pad(arr, (0, max_length - len(arr)), constant_values=np.nan) for arr in data]

    return padded_arrays


def visualize_cell(data, data_means, conditions, title, figure_name):
    min_y = np.min(np.concatenate(data))
    max_y = np.max(np.concatenate(data))
    fig = plt.figure(figsize=[30, 17])
    for i in range(len(conditions)):
        plt.subplot(2, len(conditions), i + 1)
        heatmap = sns.heatmap(data[i], vmin=-0.05, vmax=0.05, cbar=False, cmap='coolwarm')
        plt.axvline(x=2 * REC_HZ, color='black', linewidth=3, alpha=0.7)
        plt.axvline(x=4 * REC_HZ, color='black', linewidth=3, alpha=0.7)
        plt.title(f"{conditions[i]} trials", fontsize=17)
        if i == 0:
            plt.ylabel('Trial', fontsize=15)

        plt.subplot(2, len(conditions), i + 1 + len(conditions))
        plt.plot(data_means[i], 'k')
        plt.axvline(x=2 * REC_HZ, color='black', linewidth=3, alpha=0.7)
        plt.axvline(x=4 * REC_HZ, color='black', linewidth=3, alpha=0.7)
        plt.xlim([0, len(data_means[i])])
        plt.ylim([min_y * 1.2, max_y * 1.2])
        if i == 0:
            plt.ylabel(f"Mean signal", fontsize=15)
        plt.xlabel('Time (sample points)', fontsize=15)
    plt.suptitle(title, fontsize=20)
    cbar_ax = plt.gcf().add_axes([0.92, 0.5, 0.02, 0.4])
    plt.colorbar(mappable=heatmap.collections[0], cax=cbar_ax)
    fig.savefig(join(BASE_PATH, figure_name))
    plt.close()

def data_visualization(dff_cells):
    # Separate trials into first and second halves
    first_half_data, second_half_data = separate_data(dff_cells)

    # Calculate mean signal for each cell in each condition
    first_half_cell_means = average_cell(first_half_data)
    second_half_cell_means = average_cell(second_half_data)

    # Rearrange cells by the highest response to stimulus in the first half
    first_half_data_mean_rearranged, cell_order, response_values_first_half = rearrange_cells_and_get_order(first_half_cell_means, 2 * REC_HZ, 4 * REC_HZ)
    second_half_data_mean_rearranged = rearrange_array(second_half_cell_means, cell_order)

    # Visualize heatmap of mean of all trials for each cell in both conditions
    visualize_all_cells_mean([first_half_data_mean_rearranged,second_half_data_mean_rearranged], ['First half','Second half'])

    # Find examples of cells that responded in excitation/inhibition/had no response to the stimulus in the first half
    excited_cell_ind, inhibited_cell_ind, no_response_cell_ind = find_response_examples(response_values_first_half)
    excited_cell_first_half = first_half_data[excited_cell_ind]
    excited_cell_first_half_mean = first_half_cell_means[excited_cell_ind]
    inhibited_cell_first_half = first_half_data[inhibited_cell_ind]
    inhibited_cell_first_half_mean = first_half_cell_means[inhibited_cell_ind]
    no_response_cell_first_half = first_half_data[no_response_cell_ind]
    no_response_cell_first_half_mean = first_half_cell_means[no_response_cell_ind]
    excited_cell_second_half = second_half_data[excited_cell_ind]
    excited_cell_second_half_mean = second_half_cell_means[excited_cell_ind]
    inhibited_cell_second_half = second_half_data[inhibited_cell_ind]
    inhibited_cell_second_half_mean = second_half_cell_means[inhibited_cell_ind]
    no_response_cell_second_half = second_half_data[no_response_cell_ind]
    no_response_cell_second_half_mean = second_half_cell_means[no_response_cell_ind]

    # Plot individual cell examples
    visualize_cell([excited_cell_first_half, excited_cell_second_half], [excited_cell_first_half_mean, excited_cell_second_half_mean], ['First half','Second half'], 'Excited Cell Example', f'excited_cell_example.png')
    visualize_cell([inhibited_cell_first_half, inhibited_cell_second_half], [inhibited_cell_first_half_mean, inhibited_cell_second_half_mean], ['First half','Second half'], 'Inhibited Cell Example', f'inhibited_cell_example.png')
    visualize_cell([no_response_cell_first_half, no_response_cell_second_half], [no_response_cell_first_half_mean, no_response_cell_second_half_mean], ['First half','Second half'], 'No Response Cell Example', f'no_response_cell_example.png')

def main ():
    # Read the 2-photon imaging data
    f_cells_file_path = Path(join(BASE_PATH, '2p_cells_data.csv'))
    f_cells_data = pd.read_csv(f_cells_file_path)
    f_neu_file_path = Path(join(BASE_PATH, '2p_neuropil_data.csv'))
    f_neu_data = pd.read_csv(f_neu_file_path)

    # Prepare data for analysis
    processed_cells = neuropil_subtraction(f_cells_data, f_neu_data)

    # Separate data into trials based on recording frequency
    cells_by_trials = separate_trials(processed_cells)

    # Add baseline
    cells_by_trials_bl = add_baseline(cells_by_trials)

    # Compute stimulus triggered dff for each trial
    dff_cells = compute_dff(cells_by_trials_bl)

    # Visualize data
    data_visualization(dff_cells)

main()
