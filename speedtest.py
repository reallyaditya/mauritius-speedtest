# LION - Reunion, Madagascar
# SAFE - Cochin (India), Melkbosstrand (Using Durban instead, South Africa), Mtunzini (Using Durban instead, South Africa), Penang (Malaysia), Reunion
# MARS - Port Mathurin (Rodrigues)

import subprocess
import json
import os
import logging
import glob
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Get Date in format "YYYY-MM-DD"
date = (datetime.now()).strftime('%Y-%m-%d')

# Open config file to get project directory
with open('config.json', 'r') as config_file:
    project_dir = json.load(config_file)

project_directory = project_dir['projectPath']

# dictionary holding speedtest servers and their respective codes
with open('./data/servers.json', 'r') as server_json:
    server_dict = json.load(server_json)


def detect_os():
    import platform

    current_os = platform.system().lower()

    if (current_os == 'linux'):
        speedtest_binary = './binaries/speedtest-linux_x86_64'
    elif (current_os == 'darwin'):
        speedtest_binary = './binaries/speedtest-macos'
    elif (current_os == 'windows'):
        speedtest_binary = './binaries/speedtest_win64.exe'
    elif (current_os == 'freebsd'):
        speedtest_binary = './binaries/speedtest_freebsd_x86_64'
    else:
        logging.error('OS not supported')

    return (speedtest_binary)


# launch a process for initiating speedtest
# must install official speedtest-cli from Ookla (https://www.speedtest.net/apps/cli)
def speedtest(server_code):

    # Run speedtest-cli from subprocess
    speedtest = subprocess.run([str(binary), "-s", str(server_code), "-f",
                                "json-pretty", "-P", "8"], capture_output=True)

    # Load stdout from subprocess to a JSON object
    result = json.loads(speedtest.stdout)
    # Pop out private info (MAC/IP-ADDR, interface,...)
    result.pop('interface', None)

    return (result)


# Save speedtest result in a JSON file.
def save_speedtest(cable, server_code):

    # Get Time in format "HH:MM:SS" (24-hour time)
    time = (datetime.now()).strftime('%H:%M:%S')

    # Create directory and subdirectory based on cable and date
    # Catch error if directory is already created
    try:
        os.makedirs(f'./data/{cable}/{date}/')
    except FileExistsError:
        logging.warning('Folder already exists')
        pass

    # Call speedtest function and get result as JSON object
    result = speedtest(server_code)

    # Save result dict to JSON file. File name based on datetime test was run.
    with open(f'./data/{cable}/{date}/{str(time)}.json', 'w+') as shell_file:
        json.dump(result, shell_file, indent=4)

    return (result)


# Run speedtest and concat all JSON results
def get_json(cable):

    # Run speedtest on dictionary above

    # JSON results path
    extension = 'json'
    path = f'./data/{cable}/{date}/*'

    # List of all JSON files in directory. Path is based on the cable and datetime
    all_json_files = [i for i in glob.glob(path.format(extension))]

    # Open JSON file to concat all results. Name is current date.
    # Save all loaded JSON file in array and save array as JSON file. File is overwritten each time.
    result = []
    with open(f'./data/{cable}/{date}.json', 'w+') as concat_file:
        for fname in all_json_files:
            with open(fname) as single_test_json:
                result.append(json.load(single_test_json))

        json.dump(result, concat_file, indent=4)


def sync_to_github():

    # Change current working directory to project directory
    os.chdir(str(project_directory))

    # Commit message is current datetime
    commit_message = f'{datetime.now()}'

    # Add and track generated files to git.
    subprocess.run(['git', 'add', '.'])
    # Commit current files with commit message.
    subprocess.run(['git', 'commit', '-m', str(commit_message)])
    # Push changes to github repo
    subprocess.run(['git', 'push'])


def main(server_list):

    realtime = []
    realtime_dict = {'LION': None, 'SAFE1': None, 'SAFE2': None,
                     'SAFE3': None, 'MARS': None}

    # Iterate on server_dict. Unpack first level key-value pairs
    for cable, country in server_list.items():

        # Iterate on server_dict. Unpack second level key-value pairs.
        for server in country:
            # Assign server code to variable
            server_code = country[server]

            logging.info(f'Speedtest running on {cable} cable in {server}')
            # Run speedtest and save result to array.
            result = save_speedtest(cable, server_code)
            realtime.append(result)

            # Call get_json function to concat all JSON results for one day.
            get_json(cable)

    count_realtime = 0
    for key in realtime_dict:
        realtime_dict[key] = realtime[count_realtime]
        count_realtime += 1

    # Save latest results to JSON file
    with open('./data/realtime.json', 'w+') as realtime_json:
        json.dump(realtime_dict, realtime_json, indent=4)

    # Sync files to GitHub repo
    sync_to_github()


if __name__ == "__main__":
    # Run main. Pass in dictionary of servers.
    global binary
    binary = detect_os()

    main(server_dict)
