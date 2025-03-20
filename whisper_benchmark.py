import subprocess
import time
import multiprocessing

# Whisper CLI executable path
whisper_exe =   
audio_file =    
model =         

# Detect maximum number of threads available
max_threads = multiprocessing.cpu_count()

# Define thread counts to test (adjust as needed)
thread_options = [2, 4, 6, 8, 10, max_threads]
results = []

print("Benchmarking Whisper with different thread counts...")

for threads in thread_options:
    print(f"Running with {threads} threads...")
    start_time = time.time()
    
    # Run Whisper CLI with selected thread count
    process = subprocess.run(
        [whisper_exe, "-f", audio_file, "-t", str(threads), "-p", "4", "-m", model],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )
    if process.returncode != 0:
        print(f"Error with {threads} threads:\n", process.stderr)

    end_time = time.time()
    elapsed = end_time - start_time
    
    # Store results
    results.append({"Threads": threads, "TimeTaken": elapsed})

# Display results
print("\nBenchmark complete. Results:")
for result in sorted(results, key=lambda x: x["TimeTaken"]):
    print(f"Threads: {result['Threads']} | Time Taken: {result['TimeTaken']:.2f} sec")
