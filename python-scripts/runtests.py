# execute the command ./sim-bpred ./tests/eio/anagram.eio

import os
import subprocess
from utils import parse_simulation_stats

# Path to the simulator
# simulator = "../sim-outorder"

simulators = ["../sim-bpred"]

# Path to the tests
tests_dir = "../tests/eio"

# path to test configs
test_configs = "configs"

# path to save the results
results_dir = "results"

# create a results directory
if not os.path.exists(results_dir):
    os.makedirs(results_dir)


print("Running tests")
# run the test with different configs
for simulator in simulators:
    # extract the simulator name
    simulator_name = simulator.split("/")[-1]
    print("Running tests with simulator: " + simulator_name)
    for test in os.listdir(tests_dir):
        # extract the test name
        test_name = test.split(".")[0]
        print("Running test: " + test_name)
        for config in os.listdir(test_configs):
            print("Running test with config: " + config)
            args = [
                simulator,
                "-config",
                test_configs + "/" + config,
                "-redir:sim",
                "results/"
                + simulator_name
                + "_"
                + test_name
                + "_"
                + config
                + ".out.txt",
                tests_dir + "/" + test,
            ]
            subprocess.run(args)
            print("")

print("All tests completed")
print("Extracting statistics")

# Process and save statistics for all relevant result files
for result_file in os.listdir(results_dir):
    if result_file.endswith(".out.txt"):  # Ensure only relevant files are processed
        result_path = os.path.join(results_dir, result_file)
        df = parse_simulation_stats(result_path)
        output_csv = os.path.join(results_dir, result_file.replace(".txt", ".csv"))
        df.to_csv(output_csv, index=False)
        print(f"Parsed statistics saved to: {output_csv}")

print("All statistics extracted")
