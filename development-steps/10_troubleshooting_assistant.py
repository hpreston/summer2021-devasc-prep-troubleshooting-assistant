#! /usr/bin/env python 
"""
This is a script that will run "onbox" on a Nexus Switch 
with the goal of running a series of show commands and 
collecting the output into files stored into date/time 
folders. One file per command. 

Commands to run: 
    show interface ethernet #/# 
    show logging last 50 
    show ip arp vrf all 
    show mac address-table 
    show ip route vrf all 
    show system internal interface ethernet #/# ethernet #/# event-history 

Command Line Argument: Interface ID
"""

from cli import cli, clid, structured_output_not_supported_error
from datetime import datetime
from os import mkdir

def run_command(command, interface): 
    """
    Run a given command and gather both raw and JSON output.
    Return as a tuple. (output_raw, output_json)
    """

    output_raw = cli(command.format(interface_id=interface))
    try: 
        output_json = clid(command.format(interface_id=interface))
    except structured_output_not_supported_error: 
        output_json = False

    return (output_raw, output_json)

if __name__ == "__main__": 
    print("Collecting show commands and storing in bootflash.")

    # Collect interface ID as command line argument 
    import argparse

    # Use argparse to determine the interface id for testing
    parser = argparse.ArgumentParser(description='Run show commands to assist with troubleshooting')
    parser.add_argument('--interface', required=True, type=str, help='Interface of interest. (example: 1/1')
    args = parser.parse_args()

    print("Interface Ethernet {interface_id} will be checked.".format(interface_id = args.interface))
   
    # Run commands and store output 
    # Dict of commands to run. Key will be used for file naming
    commands = {
        "show_interface": "show interface ethernet {interface_id}",
        "show_logging": "show logging last 50",
        "show_ip_arp": "show ip arp vrf all",
        "show_mac_address_table": "show mac address-table",
        "show_ip_route": "show ip route vrf all",
        "show_system_internal_interface": "show system internal interface ethernet {interface_id} ethernet {interface_id} event-history"
    }

    # Output Dict
    output = {}

    # Loop over commands to run function and save output 
    for label, command in commands.items(): 
        output[label] = run_command(command, args.interface)
    
    # for debugging, print output 
    # print(output)

    # Create new folder for output 
    now = datetime.now()
    report_timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    folder_name = "/bootflash/ts_report_{timestamp}_interface{interface_id}".format(
        timestamp=report_timestamp, 
        interface_id=args.interface.replace("/", "_")
        )

    print("Output will be stored in folder {folder_name}/".format(folder_name=folder_name))
    mkdir(folder_name)

    # Create a file for each command output
    for command, results in output.items(): 
        # Unpack the results
        raw_output, json_output = results

        # write raw data file 
        print("Writing file {folder_name}/{command}.txt".format(folder_name=folder_name, command=command))

        # if json_output available, write json file 
        if json_output: 
            print("Writing file {folder_name}/{command}.json".format(folder_name=folder_name, command=command))