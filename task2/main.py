import os
from multiprocessing import Process, Pipe
import time
import logging

def search_keywords(file_path, keywords, connection):
    try:
        found_keywords = []
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                amount = content.count(keyword)
                if amount > 0:
                    found_keywords.append(keyword)
        connection.send((file_path, found_keywords))
        connection.close()
    except Exception as e:
        logging.error(f"Processing {file_path}: {str(e)}")

# Main function
def main(files, keywords):
    start_time = time.time()
    parent_connections = []
    processes = []

    # Creating processes
    for file_path in files:
        parent_conn, child_conn = Pipe()
        pr = Process(target=search_keywords, args=(file_path, keywords, child_conn))
        pr.start()
        processes.append(pr)
        parent_connections.append(parent_conn)

    # Collect results from pipes
    results = {}
    for parent_conn in parent_connections:
        file_path, found_keywords = parent_conn.recv()
        for keyword in found_keywords:
            results.setdefault(keyword, []).append(file_path)

    # Wait for all processes
    [pr.join() for pr in processes]

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    return results

# You need to enter files (and create them in directory data) and add keywords
if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(current_directory, '../data')
    files = [os.path.join(data_directory, "file1.txt"), #<---enter file name here
             os.path.join(data_directory, "file2.txt")]
    
    keywords = ["Hello", "second", "*", "FOURTH"] 

    results = main(files, keywords)
    print("Results:")
    for keyword, found_files in results.items():
        print(f"Keyword '{keyword}' found in files: {found_files}")