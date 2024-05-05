import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../utils/'))
from utils import search_keywords
from threading import Thread
import time



# Main fucntion
def main(files, keywords):
    start_time = time.time()
    results = {}

    # Creating threads
    threads = []
    for i in range(len(files)):
        thread = Thread(target=search_keywords, args=(files[i], keywords, results))
        thread.start()
        threads.append(thread)

    # Wait for all threads
    [str.join() for str in threads]

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