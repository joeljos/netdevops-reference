import sys
import subprocess
import re

#cmd = "source /home/cisco/pyats_sandbox/bin/activate ; python /home/cisco/netdevops1/Tests/pyats_tests.py --testbed pyats_testbed.yaml"

cmd = "python3 Tests/pyats_tests.py --testbed Tests/pyats_testbed.yaml"

output = subprocess.run(cmd, shell=True, executable='/bin/bash', capture_output=True, text=True)
result = output.stdout
error = output.stderr
print(error,result)

x = re.search("Success Rate\s+100.0%", result)
if(x):
    print("Testcases have passed..")
else:
    print("Testcases have failed!!")
    sys.exit(True)
