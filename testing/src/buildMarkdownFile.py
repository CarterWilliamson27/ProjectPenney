import os
import csv
import numpy as np


def generate_comparison_table(method1averages: dict, method2averages: dict) -> str:
    # Vertical stack of methods with field names on the left column

    # First combine write_time and convert_time for method2
    for fieldsuffix in ["avg_time", "total_time"]:
        method2averages["write_"+fieldsuffix] += method2averages["con_"+fieldsuffix]
        method2averages["write_"+fieldsuffix] = round(method2averages["write_"+fieldsuffix], 5) 
    
    # little bit of stats: adding two independent standard deviations a and b = sqrt(a^2 + b^2)
    method2averages["write_std"] = round(np.sqrt((method2averages["con_std"]**2) + method2averages["write_std"]**2), 5)

    # Now generate table
    headers = "| stat | Method 1 | Method 2 |\n" \
    "|---|---|--|\n"

    data_rows = ""
    for field in method1averages:
        if method1averages[field] < method2averages[field]:
            data_rows += field + "|+" + str(method1averages[field]) + "|" + str(method2averages[field]) + "|"
        else:
            data_rows += field + "|" + str(method1averages[field]) + "|+" + str(method2averages[field]) + "|"

        data_rows+="\n"
    
    return headers+data_rows


def generate_table(datapath: str) -> list:
    
    with open(datapath, 'r') as file:
        csv_reader = csv.reader(file) 
        table_headers="|"
        table_divider = "|"

        # Header row
        field_names = next(csv_reader)
        for field_name in field_names:
            table_headers +=" " + str(field_name) + " |"
            table_divider +="---|"
        
        # Actual data
        data_rows = "|"
        average_of_all_data = [0] * len(field_names)
        num_iterations = 0
        for row in csv_reader:
            i = 0
            num_iterations +=1
            for field in row:
                average_of_all_data[i] += float(field)
                data_rows += " " + str(field) + " |"
                i+=1
            data_rows+="\n|"
        
        data_average_row = "| Average |"
        averages_dict = {}
        i = 1 # Skip iteration number
        for field in average_of_all_data[1:]: # Skip iteration number
            average = field/num_iterations
            average = round(average, 5)
            data_average_row += " " + str(average) + " |"
            averages_dict[field_names[i]] = average
            i+=1


        table_headers+="\n"
        table_divider+="\n"
        data_rows = data_rows[:-1] # chop off last |
        table = table_headers + table_divider + data_rows + data_average_row
        return table, averages_dict

def buildMarkdownFile(num_iterations: int, num_decks: int) -> None:

    # Should include all data (see outputs folder) as well as the file sizes
    NPY_FILEPATH = os.path.join("testing", "data", "npydata")
    npydata = os.listdir(NPY_FILEPATH)
    npyfilesize_mb = os.path.getsize(os.path.join(NPY_FILEPATH, npydata[0]))/1000000

    method1results = generate_table(os.path.join("testing", "outputs", "data", "npy_compiled_output.csv"))
    method1table = method1results[0]
    method1averages = method1results[1]
    method1averages['file_size (MB)'] = npyfilesize_mb

    BIN_FILEPATH = os.path.join("testing", "data", "bindata")
    bindata = os.listdir(BIN_FILEPATH)
    binfilesize_mb = os.path.getsize(os.path.join(BIN_FILEPATH, bindata[0]))/1000000

    method2results = generate_table(os.path.join("testing", "outputs", "data", "bin_compiled_output.csv"))
    method2table = method2results[0]
    method2averages = method2results[1]
    method2averages['file_size (MB)'] = binfilesize_mb

    comparetable = generate_comparison_table(method1averages, method2averages)
    
    sections = []
    mdstring = ""
    linebreak = "___"

    # ----- Begin document -----
    title = "## Project Penney Data Generation<br><sup>Carter Williamson & Ruihan Fang</sup>"
    sections.append(title)

    # ----- Compare Methods -----
    comparetitle = "### BLUF: Comparison of Methods"
    sections.append(comparetitle)
    sections.append(linebreak)

    compareheader = "These are the results of the tests (number of iterations:  "+ str(num_iterations) + ", number of decks per iteration: " + str(num_decks) + \
    ") performed on both methods. " \
    "For these tests, decks are saved to files in batches of 10,000, and stats are collected from each time a file was created. <br>" \
    "gen_* represents the amount of time it took to make 10,000 arrays of 52 1s and 0s. <br>" \
    "write_* represents the amount of time it took to write the file to disk. <br>" \
    "read_* represents the amount of time it took to read the file from disk. <br>" \
    r"\*_avg_time is the average amount of time per file. <br>" \
    r"\*_total_time is the total amount of time per iteration (" + str(num_decks) + " decks). <br>" \
    r"\*_std is the standard deviation between times per iteration. <br>" \
    "These values are then averaged across the " + str(num_iterations) + " iterations. <br>" \
    "A \"+\" next to a method's stat indicates that method performed faster/better than the other. <br>" \
    "(Further discussion below)"
    sections.append(compareheader)
    sections.append(comparetable)
    comparebody = "Given these results, Method 2 is the preferred method given its significantly faster read times " \
    " and only a bit slower write times compared to Method 1, since the computationally-heavy part of the project (scoring) involves " \
    " reading the files.  <br> It should be noted that the write times for Method 2 is a combination of the time to convert the numpy array to bytes" \
    " and the time to write those bytes to a binary file.<br> (More detailed information on the methods in sections below)"
    sections.append(comparebody)

    # ----- Method 1 ------

    method1title = "### Method 1: Store arrays in .npy files"
    sections.append(method1title)
    sections.append(linebreak)
    method1body = "The first method was to follow what was shown in class and store the decks in numpy arrays, then save them as .npy files." \
    "<br>Each .npy file contains 10,000 decks, and each is " + str(npyfilesize_mb) + " MB." \
    "<br>Table of results: "
    sections.append(method1body)
    sections.append(method1table)

    sections.append(linebreak)
    # ----- Method 2 ------

    method2title = "### Method 2: Store arrays in .bin files"
    sections.append(method2title)
    sections.append(linebreak)
    method2body = "The second method was to essentially copy the first method, but then use the numpy.ndarray.tobytes method to store the decks in binary files." \
    "<br>Each .bin file contains 10,000 decks, and each is " + str(binfilesize_mb) + " MB." \
    "<br>Table of results: "
    sections.append(method2body)
    sections.append(method2table)

    # ----- Write to file -----

    sections.append("<br> EOF <br>")
    for section in sections:
        mdstring += section+"\n"
    with open(os.path.join('testing', 'outputs', 'DataGeneration.md'), "w") as mdfile:
        mdfile.write(mdstring)

#if __name__=="__main__":
#    buildMarkdownFile(10, 2000000)
