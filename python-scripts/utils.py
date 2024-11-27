import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


def get_data(test_files, labels):
    data = pd.DataFrame()

    print("labels:", "|".join(labels))

    # Extract values from each test file
    for test_file in test_files:
        # Read the CSV file
        df = pd.read_csv(test_file)
        # replace the rows that contain the label with the label

        # Filter rows where 'stat' contains any of the labels

        filtered = df[df["stat"].str.contains("|".join(labels), na=False)]

        # replace the stat with the label that matched it
        for label in labels:
            filtered.loc[filtered["stat"].str.contains(label), "stat"] = label

        # print("filtered 1", filtered.head())
        # Set 'stat' as index and extract 'value'
        filtered = filtered.set_index("stat")["value"].astype(float)

        # print("filtered 2", filtered.head())
        # Add filtered values to the data DataFrame
        print(test_file.split("/")[-1].replace(".cfg.out.csv", ""))
        data[test_file.split("/")[-1].replace(".cfg.out.csv", "")] = filtered
        print("data", data.head())

    # Ensure consistent order and index for the DataFrame
    data = data.reindex(index=filtered.index)
    return data


def plot_data(
    data,
    test_files,
    filename="results/branch_prediction_metrics.png",
    title="Comparison Across Tests",
    xlabel="Values",
    ylabel="Metrics",
):
    # Prepare for plotting
    x = np.arange(len(data.index))  # Label locations based on unique fields
    width = 0.25  # Width of each bar
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each test as a separate set of bars
    for i, column in enumerate(data.columns):
        ax.bar(x + i * width, data[column], width, label=column)

    # add values to the bars
    for i, column in enumerate(data.columns):
        for j, value in enumerate(data[column]):
            ax.text(j + i * width - 0.1, value, str(value), color="black")

    # Add labels, title, and legend
    ax.set_xlabel("Metrics")
    ax.set_ylabel("Values")
    ax.set_title("Comparison of Branch Prediction Metrics Across Tests")
    ax.set_xticks(x + width / len(test_files))
    ax.set_xticklabels(data.index, rotation=45, ha="right")
    ax.legend(title="Test Files")

    # Adjust layout and show plot
    plt.tight_layout()
    plt.savefig(filename)


def parse_simulation_stats(file_path):
    """
    Parses simulation statistics from a file and creates a DataFrame.

    :param file_path: Path to the simulation statistics file.
    :return: DataFrame with columns: stat, value, comment, file_name.
    """
    stats = []
    file_name = os.path.basename(file_path)  # Extract the file name from the path

    # Read file and parse lines after "sim: ** simulation statistics **"
    within_stats = False
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if "sim: ** simulation statistics **" in line:
                within_stats = True
                continue

            if within_stats:
                pattern = re.compile(r"(\S+)\s+(\S+)\s+#\s*(.*)")

                # Match the line
                match = pattern.match(line)

                # match = stat_pattern.match(line)
                if match:
                    stat, value, comment = match.groups()
                    stats.append([stat, value, comment or "", file_name])

    # Create a DataFrame from the parsed statistics
    df = pd.DataFrame(stats, columns=["stat", "value", "comment", "file_name"])
    return df
