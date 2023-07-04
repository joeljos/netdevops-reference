import paramiko
import time
import sys


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("connecting to 10.10.20.179...")
ssh.connect('10.10.20.179', username='cisco', password='cisco')
print("connected via ssh to 10.10.20.179")
#print("waiting 60 seconds for convergence and stability")
#time.sleep(60)
cmd = "ping -c 5 172.16.252.30"
print(cmd)
stdin, stdout, stderr = ssh.exec_command(cmd)
time.sleep(5)
result = stdout.readlines()
ssh.close()
print(("\n").join(result))
if(" 0% " in result[-2]):
    print("ping is successfull..")
else:
    print("ping has failed!!")
    sys.exit(True)

    
        

