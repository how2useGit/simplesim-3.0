import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import get_data, plot_data


# Directory containing result files
results_dir = "results"

# Test result files
test_files = [
    "sim-outorder_anagram_nottaken.cfg.out.csv",
    "sim-outorder_anagram_taken.cfg.out.csv",
    "sim-outorder_anagram_bimod.cfg.out.csv",
]

# Full paths to the test files
test_files = [f"{results_dir}/{file}" for file in test_files]

# Labels to compare
labels = [
    "bpred_addr_rate",
    "bpred_dir_rate",
    # "sim_total_loads",
    # "sim_total_stores",
    # "sim_total_branches",
]

# Initialize a DataFrame to store values
data = pd.DataFrame()

print("labels:", "|".join(labels))

# Ensure consistent order and index for the DataFrame
data = get_data(test_files, labels)

plot_data(
    data,
    test_files,
    filename="plots/branch_prediction_metrics.png",
    title="Comparison Across Tests",
    xlabel="Values",
    ylabel="Metrics",
)

# Print DataFrame for debugging
print("Data:")
print(data.head())
