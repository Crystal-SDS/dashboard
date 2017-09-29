import os

host = "10.30.233.251"
user = "crystal"
password = "crystal"

print "Copying api to S2CAIO"

os.system('sshpass -p %s scp -r %s %s@%s:%s' % (password, 'crystal_dashboard/*', user, host, '/home/crystal/crystal/dashboard/crystal_dashboard'))
print "FINISH!"
