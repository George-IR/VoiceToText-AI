import subprocess
import time
import multiprocessing
import csv
import re

whisper_exe =   location
audio_file =    location
model =         location

# Detect maximum number of threads available
max_threads = multiprocessing.cpu_count()

# Define thread counts to test (adjust as needed)
thread_options = [2, 4, 6, 8, 10 ,max_threads)
results = []

print("Benchmarking Whisper with different thread counts...")

for threads in thread_options:
    print(f"Running with {threads} threads...")
    start_time = time.time()
    
    #print(whisper_exe, "-f", audio_file, "-t", str(threads), "-p", "4", "-m", model)
    # Run Whisper CLI with selected thread count
    process = subprocess.run(
        [whisper_exe, "-f", audio_file, "-t", str(threads), "-p", "4", "-m", model],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # Extract total processing time from Whisper output
    # print("\n--- Whisper Output Debug ---\n")
    # print(process.stderr)
    # print("\n--- End of Debug Output ---\n")

    # Extract total processing time from Whisper output
    print("\n--- Whisper Transcript ---\n")
    print(process.stdout)
    print("\n--- End of Transcript ---\n")

    match = re.search(r"whisper_print_timings:\s+total time =\s+([\d.]+) ms", process.stderr)

    whisper_time = float(match.group(1)) / 1000 if match else None
    
    # Compute error if Whisper provided a valid time
    error = abs(elapsed - whisper_time) if whisper_time else None
    
    # Store results
    results.append({"Threads": threads, "ScriptTime": elapsed, "WhisperTime": whisper_time, "Error": error})

# Save results to CSV
csv_filename = f"whisper_benchmark_results_{audio_file.split('/')[1]}.csv"
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["Threads", "ScriptTime", "WhisperTime", "Error"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

# Display results
print("\nBenchmark complete. Results:")
for result in sorted(results, key=lambda x: x["ScriptTime"]):
        whisper_time_str = f"{result['WhisperTime']:.2f} sec" if result['WhisperTime'] is not None else "N/A"
        error_str = f"{result['Error']:.2f} sec" if result['Error'] is not None else "N/A"

        print(f"Threads: {result['Threads']} | Script Time: {result['ScriptTime']:.2f} sec | "
              f"Whisper Time: {whisper_time_str} | Error: {error_str}")

print(f"Results saved to {csv_filename}")