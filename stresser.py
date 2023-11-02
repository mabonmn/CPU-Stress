import multiprocessing

def stress_cpu_core(core_id):
    while True:
        pass

if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    processes = []

    print(f"Stressing all {num_cores} CPU cores...")

    for core_id in range(num_cores):
        process = multiprocessing.Process(target=stress_cpu_core, args=(core_id,))
        processes.append(process)
        process.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("Stopping CPU stress...")

