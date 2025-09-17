import numpy as np
import csv
import os

# Generate stats from raw data such as mean, total, and std from each iteration
# Write stats to a csv 
# Write raw data to a csv as well to retain all data (not that we use it)

# These methods could be generalized/optimized further, but this is good enough

def write_raw_data_to_csv(data: list, file_name: str) -> None:
    # data[headers[], actual data[]*]
    file_path = os.path.join('testing', 'outputs', file_name)
    if os.path.exists(file_path):
        os.remove(file_path) # clean out data
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(data[0]) # write headers
        iteration_counter=1

        for row in data[1:]: # Skip headers
                for i in range(len(row[0])):
                    sublist = [item[i] for item in row]
                    sublist.insert(0, iteration_counter)
                    writer.writerow(sublist)  
                    iteration_counter+=1

def write_compiled_data_to_csv(data: list, file_name: str) -> None:
    # data[headers[], actual data[]*]
    file_path = os.path.join('testing', 'outputs', file_name)
    if os.path.exists(file_path):
        os.remove(file_path) # clean out data
    
    iteration_counter = 0
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(data[0]) # write headers
        iteration_counter=1

        for row in data[1:]: # Skip headers
                for i in range(len(row[0])):
                    sublist = [item[i] for item in row]
                    sublist.insert(0, iteration_counter)
                    writer.writerow(sublist)  
                    iteration_counter+=1

def npyCompileData(data: list) -> None:
    # data[headers[], iteration[generation_time[], write_time[], read_time[]]*]
    # There has to be a more efficient way to do this
    write_raw_data_to_csv(data, 'npy_raw_output.csv')

    average_generation_time_by_iteration = []
    total_generation_time_by_iteration = []
    std_generation_time_by_iteration = []

    average_write_time_by_iteration = []
    total_write_time_by_iteration = []
    std_write_time_by_iteration = []

    average_read_time_by_iteration = []
    total_read_time_by_iteration = []
    std_read_time_by_iteration = []

    for iteration in data[1:]: # Skip headers
        generation_times = np.array(iteration[0], dtype=np.float16)
        write_times = np.array(iteration[1], dtype=np.float16)
        read_times = np.array(iteration[2], dtype=np.float16)

        average_generation_time_by_iteration.append(np.average(generation_times))
        total_generation_time_by_iteration.append(np.sum(generation_times))
        std_generation_time_by_iteration.append(np.std(generation_times))

        average_write_time_by_iteration.append(np.average(write_times))
        total_write_time_by_iteration.append(np.sum(write_times))
        std_write_time_by_iteration.append(np.std(write_times))

        average_read_time_by_iteration.append(np.average(read_times))
        total_read_time_by_iteration.append(np.sum(read_times))
        std_read_time_by_iteration.append(np.std(read_times))

    write_compiled_data_to_csv([
        ['iteration', 'gen_avg_time', 'gen_total_time', 'gen_std', 'write_avg_time', 'write_total_time', 'write_std', 
         'read_avg_time', 'read_total_time', 'read_std'], 
        [average_generation_time_by_iteration, total_generation_time_by_iteration, std_generation_time_by_iteration, 
        average_write_time_by_iteration, total_write_time_by_iteration, std_write_time_by_iteration,
        average_read_time_by_iteration, total_read_time_by_iteration, std_read_time_by_iteration]], 'npy_compiled_output.csv')


def binCompileData(data: list) -> None:
    # data[headers[], iteration[generation_time[], write_time[], convert_time[], read_time[]]*]
    # There has to be a more efficient way to do this
    write_raw_data_to_csv(data, 'raw_bin_output.csv')

    average_generation_time_by_iteration = []
    total_generation_time_by_iteration = []
    std_generation_time_by_iteration = []

    average_write_time_by_iteration = []
    total_write_time_by_iteration = []
    std_write_time_by_iteration = []

    average_read_time_by_iteration = []
    total_read_time_by_iteration = []
    std_read_time_by_iteration = []

    average_convert_time_by_iteration = []
    total_convert_time_by_iteration = []
    std_convert_time_by_iteration = []

    for iteration in data[1:]: # Skip headers
        generation_times = np.array(iteration[0], dtype=np.float16)
        write_times = np.array(iteration[1], dtype=np.float16)
        convert_times = np.array(iteration[2], dtype=np.float16)
        read_times = np.array(iteration[3], dtype=np.float16)

        average_generation_time_by_iteration.append(np.average(generation_times))
        total_generation_time_by_iteration.append(np.sum(generation_times))
        std_generation_time_by_iteration.append(np.std(generation_times))

        average_write_time_by_iteration.append(np.average(write_times))
        total_write_time_by_iteration.append(np.sum(write_times))
        std_write_time_by_iteration.append(np.std(write_times))

        average_convert_time_by_iteration.append(np.average(convert_times))
        total_convert_time_by_iteration.append(np.sum(convert_times))
        std_convert_time_by_iteration.append(np.std(convert_times))

        average_read_time_by_iteration.append(np.average(read_times))
        total_read_time_by_iteration.append(np.sum(read_times))
        std_read_time_by_iteration.append(np.std(read_times))

    write_compiled_data_to_csv([
        ['iteration', 'gen_avg_time', 'gen_total_time', 'gen_std', 'write_avg_time', 'write_total_time', 'write_std',
         'con_avg_time', 'con_total_time', 'con_std', 'read_avg_time', 'read_total_time', 'read_std'], 
        [average_generation_time_by_iteration, total_generation_time_by_iteration, std_generation_time_by_iteration, 
        average_write_time_by_iteration, total_write_time_by_iteration, std_write_time_by_iteration,
        average_convert_time_by_iteration, total_convert_time_by_iteration, std_convert_time_by_iteration,
        average_read_time_by_iteration, total_read_time_by_iteration, std_read_time_by_iteration]], 'bin_compiled_output.csv')
