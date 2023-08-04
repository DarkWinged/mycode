#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
## Try a real world test with getpass

## import Paramiko so we can talk SSH
import paramiko # allows Python to ssh
import os # low level operating system commands
import getpass # we need this to accept passwords
import yaml
import argparse

def remote_path_exists(sftp, path):
    try:
        sftp.stat(os.path.expanduser(os.path.normpath(path)))
        return True
    except FileNotFoundError:
        print('no path:', path, 'on', f'{sftp.get_channel().transport.get_username()}@{sftp.get_channel().transport.sock.getpeername()[0]}')
        return False


def get_files():
    files = []
    if os.path.exists(args.local_path) and os.path.isdir(args.local_path):
        for entry in os.scandir(args.local_path):
            if entry.is_file():
                files.append(entry.name)
        return files
    return []

def move_files(sftp):
    if remote_path_exists(sftp, args.remote_path):
        files = get_files()
        if files:
            local_path = os.path.expanduser(os.path.normpath(args.local_path))
            remote_path = os.path.expanduser(os.path.normpath(args.remote_path))
            for file_to_move in files:
                sftp.put(f"{local_path}/{file_to_move}", f"{remote_path}/{file_to_move}")

def get_cred_data() -> list[dict[str,any]]:
    path = '~/sshpass.yaml' 
    if args.yaml_path:
        yaml_path = os.path.expanduser(os.path.normpath(args.yaml_path)) 
        if os.path.exists(yaml_path) and os.scandir(yaml_path).is_file():
            path = yaml_path

    with open(os.path.expanduser(os.path.normpath(path))) as passfile:
        data = yaml.load(passfile, Loader=yaml.SafeLoader)
        return data

def main():
    data = get_cred_data()
    for entry in data:
        with paramiko.Transport(entry['ip'], 22) as t:
            passwd = getpass.getpass(f'{entry["un"]}@{entry["ip"]} password:')
            try:
                t.connect(username=entry['un'], password=passwd)
                with paramiko.SFTPClient.from_transport(t) as sftp:
                    move_files(sftp)
            except paramiko.ssh_exception.AuthenticationException as e:
                print(e)
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coppies files from the local host to remote hosts")
    parser.add_argument("-l", "--local_path", type=str, help="Selects the local directory to coppy from.", required=True)
    parser.add_argument("-r", "--remote_path", type=str, help="Selects the remote directory to coppy to.", required=True)
    parser.add_argument("-y", "--yaml_path", type=str, help="Overries the default path to the sshpass.yaml file")
    args = parser.parse_args()

    main()
