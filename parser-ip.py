import re
import argparse
import json

# Function to parse log file and extract IP addresses with timestamps
def parse_log_file(log_file_path, unique=False):
    # Define the regex pattern to match log lines containing IP addresses
    # This pattern matches the log message with 'Connected with' and an IP address
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - .+ - INFO - Connected with \('([^']+)',\s*\d+\)")

    # Set to store unique IPs (if unique flag is set)
    ip_set = set()

    # Open the output file for appending
    with open("parsed_ips.txt", "a") as output_file:
        # Open the log file for reading
        with open(log_file_path, 'r') as log_file:
            # Iterate over each line in the log file
            for line in log_file:
                try:
                    # Parse the JSON object from the log line
                    log_entry = json.loads(line.strip())
                    
                    # Extract the "log" field (the actual log message)
                    log_message = log_entry.get('log', '')
                    
                    # Search for matches in the log message using the regex pattern
                    match = pattern.search(log_message)
                    if match:
                        # Extract the date/time and IP address
                        date_time = match.group(1)
                        ip_address = match.group(2)
                        
                        # Add the IP address to the set (to ensure uniqueness)
                        if unique:
                            ip_set.add(ip_address)
                        else:
                            output_file.write(f"{date_time} | {ip_address}\n")
                
                except json.JSONDecodeError:
                    # Handle lines that cannot be parsed as JSON
                    print(f"Skipping non-JSON line: {line.strip()}")
                    continue
        
        # If unique flag is set, write unique IPs to the output file
        if unique:
            for ip in ip_set:
                output_file.write(f"{ip}\n")

    print(f"Parsing complete. {'Unique ' if unique else ''}IP addresses and timestamps saved in 'parsed_ips.txt'.")

# Main function to handle command line arguments using argparse
def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Parse a log file and extract IP addresses with timestamps.")
    
    # Add argument for the log file location
    parser.add_argument('log_file', help="Path to the log file to parse")
    
    # Add argument for unique IPs
    parser.add_argument('--unique', action='store_true', help="If set, only unique IPs will be returned")

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the function to parse the log file with the unique flag if specified
    parse_log_file(args.log_file, unique=args.unique)

if __name__ == "__main__":
    main()
