#!/usr/bin/expect

spawn su - user -c "/usr/local/hadoop/sbin/stop-all.sh"
expect ":"
send "passw0rd\r"
expect eof
