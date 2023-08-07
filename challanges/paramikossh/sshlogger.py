#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/env python3
# James L. Rogers | github.com/DarkWinged

import os
from datetime import datetime
import yaml
import argparse
from netmiko import ConnectHandler
import paramiko

def normalize_path(path: str) -> str:
    return os.path.expanduser(os.path.normpath(path))

def get_cred_data() -> list[dict[str, any]]:
    path = '~/sshpass.yaml'
    if args.yaml_path:
        yaml_path = normalize_path(args.yaml_path)
        if os.path.exists(yaml_path) and os.path.isfile(yaml_path):
            path = yaml_path

    with open(os.path.expanduser(os.path.normpath(path))) as passfile:
        data = yaml.load(passfile, Loader=yaml.SafeLoader)
        return data

def choose_host(creds: list[dict[str, any]]) -> str:
    u_input = -1

    while u_input not in range(len(creds)):
        for index, cred in enumerate(creds):
            print(f'{index})', cred['un'])
        u_input = int(input('> '))
    return creds[u_input]

def get_prompt(connection):
    prompt = connection.find_prompt()
    prompt_parts = prompt.split('@')
    user = prompt_parts[0]
    path = prompt_parts[-1].strip('$ ')
    return f"{user}@{path}$ "

def main():
    """Our runtime code that calls other functions"""
    # describe the connection data
    credz = get_cred_data()

    # harvest private key for all 3 servers
    mykey_path = "/home/student/.ssh/id_rsa"
    cred = choose_host(credz)

    # Load the SSH private key using Paramiko
    mykey = paramiko.RSAKey(filename=mykey_path)

    # create a session object
    with ConnectHandler(
        device_type="linux",  # Or specify the appropriate device type if not Linux
        host=cred.get("ip"),
        username=cred.get("un"),
        pkey=mykey,  # Use the loaded private key
    ) as sshsession:
        # display our connections
        host = cred.get('un') + '@' + cred.get('ip')
        print("Connecting to... " + host)

        # touch the file goodnews.everyone in each user's home directory
        sshsession.send_command_timing("touch /home/" + cred.get("un") + "/goodnews.everyone")
        u_input = ''
        while u_input != 'exit':
            prompt = get_prompt(sshsession)
            shell_str = input(f'{host}:{prompt}')
            u_input = shell_str
            time = datetime.now().time()
            # list the contents of each home directory
            output = sshsession.send_command_timing(u_input)
            if output:
                print(output)
                with open(normalize_path('~/log.txt'), 'a') as log_file:
                    log_str = f"[{host}:{prompt}; {time}]{output.strip('\n')}\n"
                    log_file.write(log_str)

    print("Thanks for looping with Alta3!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Connects to a remote host and logs the interactions.")
    parser.add_argument("-y", "--yaml_path", type=str, help="Overrides the default path to the sshpass.yaml file")
    args = parser.parse_args()

    main()
 