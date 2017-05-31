#!/usr/bin/perl
my $a1 = "source /opt/spark/bigdata_env";
my $a2 = "/opt/spark/KrbClient/kerberos/bin/kinit -kt /opt/user.keytab -p shiepuser";

my $a = "";
foreach $str (@ARGV) {
    $a .= "$str ";
}

my $r = int(rand(1000000));
my $file = "/tmp/tmpord_$r.sh";
open TMPORD, '>', $file;
print TMPORD "$a1\n$a2\n$a\n";
close TMPORD;
print `/bin/bash $file`;
unlink glob $file;
