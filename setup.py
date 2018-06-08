from constants import *
import paramiko

def setupCamera():
    sshClient = paramiko.SSHClient()
    sshClient.load_system_host_keys()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.connect(PI_HOST, username=PI_USER, password=PI_PASS)
    channel = sshClient.get_transport().open_session()
    if channel is not None:
        command = "raspivid -vf -n -w 640 -h 480 -o - -t 0 -b 2000000 | nc "+ MY_IP + " " + str(PI_PORT)
        channel.exec_command(command)
        print(" Connected to camera.")
    else:
        print(" Could not connect to PI. Quitting...")
        exit(0)

def calibrate():
    pass
