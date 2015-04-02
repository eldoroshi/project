import subprocess
import time

output = subprocess.check_output(["ps","-A"])

if not 'mysqld' in  output:

	p = subprocess.Popen(["sudo", "service", "mysql", "start"], stderr=subprocess.PIPE)
	output, err = p.communicate()
	print time.strftime("%Y-%m-%d %H:%M")
	print "Mysql Started", output
	
