#!/usr/bin/perl

use MIME::Base64;

my $file	= "sniff-traffic.txt";

# Example
# root@bt:/var/www/topsecret# grep "Authorization: Basic" sniff-traffic.txt | tail -1
# Authorization: Basic c3R1ZGVudDpUcnkySDRja00zIQ==

# Only Display the string "Authorization: Basic" from file sniff-traffic.txt
# Use tail -1 to only display the last line
# Use awk to display the third column using a space as the default delimiter
chomp(my $encryption	= `grep "Authorization: Basic" sniff-traffic.txt | tail -1 | awk '{print \$3}'`);

print "Base64 Encryption String: $encryption\n";

if($encryption ne "")
{
	# Decode Base64 Encryption
	my $decoded	= decode_base64($encryption);

	print "Before Parse: $decoded\n";

	# Parse out username and password from the $decoded data using the colon(:) as a delimiter
	my($username,$password) = split(/:/,$decoded);

	print "Decoded:--> [Username:$username] [Password:$password]\n";
}
else
{
	print "Base64 Encryption String: [Not Found]\n";
}
