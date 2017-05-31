#!/usr/bin/expect

spawn su - user -c "/usr/local/spark/sbin/start-all.sh"
expect ":"
send "passw0rd\r"
expect eof
