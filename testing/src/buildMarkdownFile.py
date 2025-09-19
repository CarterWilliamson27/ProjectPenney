import os
import csv
def buildMarkdownFile():
    
    # Build out seperate method to collect variables used in the mdfile
    NPY_FILEPATH = os.path.join("testing", "data", "npydata")
    npydata = os.listdir(NPY_FILEPATH)
    npyfilesize_mb = os.path.getsize(os.path.join(NPY_FILEPATH, npydata[0]))/1000000

    BIN_FILEPATH = os.path.join("testing", "data", "bindata")
    bindata = os.listdir(BIN_FILEPATH)
    binfilesize_mb = os.path.getsize(os.path.join(BIN_FILEPATH, bindata[0]))/1000000

    # Should include all data (see outputs folder) as well as the file sizes and total space taken up by the data dir
    sections = []
    mdstring = ""
    linebreak = "___"
    title = "## Project Penney Data Generation<br><sup>Carter Williamson & Ruihan Fang</sup>"
    sections.append(title)
    method1title = "### Method 1: Store arrays in .npy files"
    sections.append(method1title)
    sections.append(linebreak)
    method1body = "The first method was to follow what was shown in class and store the decks in numpy arrays. " \
    "Each .npy file contains 10,000 decks, and each is " + str(npyfilesize_mb) + " MB.\n" \
    "Table of results: "
    sections.append(method1body)
    # Method to generate table
    method1table = generate_table('npy')
    sections.append(method1table)

    for section in sections:
        mdstring += section+"\n"
    with open("DataGeneration.md", "w") as mdfile:
        mdfile.write(mdstring)

def generate_table(method: str):
    # Header row
    output_file_name=method+"_compiled_output.csv" 
    datapath = os.path.join("testing", "outputs", output_file_name)
    with open(datapath, 'r') as file:
        csv_reader = csv.reader(file) 
        table_headers="|"
        table_divider = "|"
        field_names = next(csv_reader)
        for field_name in field_names:
            table_headers +=" " + str(field_name) + " |"
            table_divider +="---|"
        
        
        data_rows = "|"

        for row in csv_reader:
            for field in row:
                data_rows += " " + str(field) + " |"
            data_rows+="\n|"
        
        table_headers+="\n"
        table_divider+="\n"
        data_rows = data_rows[:-1] # chop off last |
        table = table_headers + table_divider + data_rows
        return table


if __name__=="__main__":
    buildMarkdownFile()
