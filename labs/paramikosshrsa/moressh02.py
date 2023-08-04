#! /usr/bin/env python3
#James L. Rogers|github.com/DarkWinged

#!/usr/bin/python3
"""Alta3 Research | rzfeeser@alta3.com
   Learning about Python SSH"""

import os
import paramiko
from datetime import datetime
import yaml
import argparse

def normalize_path(path: str) -> str:
    return os.path.expanduser(os.path.normpath(path)) 

def get_cred_data() -> list[dict[str,any]]:
    path = '~/sshpass.yaml' 
    if args.yaml_path:
        yaml_path = normalize_path(args.yaml_path) 
        if os.path.exists(yaml_path) and os.scandir(yaml_path).is_file():
            path = yaml_path

    with open(os.path.expanduser(os.path.normpath(path))) as passfile:
        data = yaml.load(passfile, Loader=yaml.SafeLoader)
        return data

def choose_host(creds: list[dict[str, any]]) -> str:
    u_input = -1

    while u_input not in range(len(creds)):
        for index, cred in enumerate(creds):
            print(f'{index})',cred['un'])
        u_input = int(input('> '))
    return creds[u_input]

def main():
    """Our runtime code that calls other functions"""
    # describe the connection data
    credz = get_cred_data()

    # harvest private key for all 3 servers
    mykey = paramiko.RSAKey.from_private_key_file("/home/student/.ssh/id_rsa")
    cred = choose_host(credz)
        ## create a session object
    with paramiko.SSHClient() as sshsession: 
        ## add host key policy
        sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ## display our connections
        host = cred.get('un') + '@' + cred.get('ip')
        print("Connecting to... " + host)

        ## make a connection
        sshsession.connect(hostname=cred.get("ip"), username=cred.get("un"), pkey=mykey)

        ## touch the file goodnews.everyone in each user's home directory
        sshsession.exec_command("touch /home/" + cred.get("un") + "/goodnews.everyone")
        u_input = ''
        while u_input != 'exit':
            path = sshsession.exec_command('pwd')[1].read().decode('utf-8').strip()
            shell_str = input(f'{host}:{path}$ ')
            u_input = shell_str
            time = datetime.now().time()
            ## list the contents of each home directory
            sessin, sessout, sesserr = sshsession.exec_command(u_input)
            sessout = sessout.read().decode('utf-8')
            sesserr = sesserr.read().decode('utf-8')
            
            #if sessin:
            #    std_in= f"[{host}:std_in; {time}]{sessin.read().decode('utf-8')}"
            if sessout:
                print(sessout)
                std_out= f"[{host}:std_out; {time}]{sessout.strip()}"
            if sesserr:
                print(sesserr)
                std_err= f"[{host}:std_err; {time}]{sesserr.strip()}"
            with open(normalize_path('~/log.txt'), 'a') as log_file:
                log_str = ''
                #if sessin:
                #    log_str = f'{std_in}'
                if sessout:
                    log_str = f'{log_str}{std_out}\n'
                if sesserr:
                    log_str = f'{log_str}{std_err}\n'
                log_file.write(log_str)

    print("Thanks for looping with Alta3!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Connects to a remote host and logs the interactions.")
    parser.add_argument("-y", "--yaml_path", type=str, help="Overries the default path to the sshpass.yaml file")
    args = parser.parse_args()
    
    main()


