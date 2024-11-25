import json
import re
import os
import shutil
from datetime import datetime


# Specify the file paths
input_file_path = 'assets/dataset/chat_record.md'  # Input file for processing
staging_directory = 'assets/dataset/staging'
output_directory = 'assets/dataset/output'


def clear_directory(directory_path):
    """
    Clears all files in the specified directory.
    """
    if os.path.exists(directory_path):
        print(f"[INFO] Clearing directory: {directory_path}")
        shutil.rmtree(directory_path)
    os.makedirs(directory_path, exist_ok=True)

def save_staging_data(input_file_path):
    """
    Reads the input file, extracts training data blocks, and saves them in staging files
    for each combination. Handles incomplete blocks for tracking.
    """

    os.makedirs(staging_directory, exist_ok=True)  # Create staging directory if it doesn't exist
    print(f"[INFO] Staging directory set to: {staging_directory}")

    # Regular expression pattern to match start and end delimiters
    start_pattern = r'---------------------start_of_training_data_set_iteration_(\d+)_of_(\d+)---------------------'
    end_pattern = r'---------------------end_of_training_data_set_iteration_(\d+)_of_(\d+)---------------------'

    # Initialize variables
    inside_block = False
    content = []
    incomplete_data = []

    print(f"[INFO] Reading input file: {input_file_path}")
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):

            # Check for the start delimiter
            start_match = re.match(start_pattern, line.strip())
            if start_match:
                # Extract details from the start pattern
                iteration, total_iterations = start_match.groups()
                
                # Log the detection of the start pattern
                print(f"[INFO] Start pattern found: Iteration {iteration}/{total_iterations} at line {line_num}")
                
                # Begin handling the block
                if inside_block:
                    # Handle incomplete block if a previous block wasn't closed
                    incomplete_data.append({
                        "iteration": iteration,
                        "content": ''.join(content).strip()
                    })
                    print(f"[WARN] Incomplete block detected before line {line_num}")
                inside_block = True
                content = []  # Reset content for new block
                continue

            # Check for the end delimiter
            end_match = re.match(end_pattern, line.strip())
            print(f"[INFO] end_pattern: {end_pattern}, line: {line}")
            if end_match and inside_block:
                # Extract details from the end pattern
                end_iteration, end_total_iterations = end_match.groups()
                print(f"[INFO] End pattern found: Iteration {end_iteration}/{end_total_iterations} at line {line_num}")
                # Validate that end matches start
                if end_iteration == iteration and end_total_iterations == total_iterations:
                    staging_file = os.path.join(staging_directory, f'iteration_{iteration}_staging.jsonl')
                    with open(staging_file, 'a', encoding='utf-8') as staging_file:
                        staging_file.write(''.join(content).strip() + '\n')
                    print(f"[INFO] Completed block saved to: {staging_file}")
                else:
                    print(f"[WARN] Mismatch between start and end at line {line_num}")
                inside_block = False  # Reset block state
                content = []
                continue

            # If inside a block, collect non-empty and non-newline content
            if inside_block and line.strip():
                content.append(line.strip())

    # Save incomplete data for tracking
    if incomplete_data:
        incomplete_file_path = os.path.join(staging_directory, 'incomplete_data.jsonl')
        with open(incomplete_file_path, 'w', encoding='utf-8') as incomplete_file:
            for entry in incomplete_data:
                json.dump(entry, incomplete_file)
                incomplete_file.write('\n')
        print(f"[WARN] Incomplete data saved to: {incomplete_file_path}")

    print("[INFO] Staging process completed.")

def process_staging_to_output():
    """
    Processes all staging files to generate a single merged output file in OpenAI format,
    excluding incomplete datasets.
    """
    os.makedirs(output_directory, exist_ok=True)  # Create output directory if it doesn't exist
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

    merged_output_file = os.path.join(output_directory, f"output_{timestamp}.jsonl")
    print(f"[INFO] Processing staging files from: {staging_directory}")
    print(f"[INFO] Merging output into: {merged_output_file}")

    with open(merged_output_file, 'w', encoding='utf-8') as merged_file:
        for filename in os.listdir(staging_directory):
            if filename.endswith('_staging.jsonl'):
                staging_file_path = os.path.join(staging_directory, filename)

                # Check if the file is incomplete by looking for known incomplete markers
                if "incomplete" in filename.lower():
                    print(f"[WARN] Skipping incomplete file: {filename}")
                    continue

                print(f"[INFO] Processing staging file: {staging_file_path}")
                with open(staging_file_path, 'r', encoding='utf-8') as staging_file:
                    for line_num, line in enumerate(staging_file, start=1):
                        try:
                            # Parse the JSON object
                            data = json.loads(line.strip())

                            # # Convert roles to OpenAI format
                            # for message in data["messages"]:
                            #     if message["role"] == "System":
                            #         message["role"] = "system"
                            #     elif message["role"] == "User":
                            #         message["role"] = "user"
                            #     elif message["role"] == "Chatbot":
                            #         message["role"] = "assistant"
                            # Write transformed data to the merged output file
                            for entry in data:
                                json.dump(entry, merged_file, ensure_ascii=False)
                                merged_file.write('\n')
                        except json.JSONDecodeError as e:
                            print(f"[ERROR] JSON decode error at line {line_num} in file {staging_file_path}: {e}")
                        except KeyError as e:
                            print(f"[ERROR] Missing key in data at line {line_num} in file {staging_file_path}: {e}")

    print("[INFO] Output generation process completed.")
    print(f"[INFO] Merged dataset saved to: {merged_output_file}")


def extract_chat_data():
    # Step 0: Clear data
    clear_directory(staging_directory)
    clear_directory(output_directory)

    # Step 1: Save staging data
    save_staging_data(input_file_path)
    # Step 2: Process staging files into OpenAI format
    process_staging_to_output()

extract_chat_data()