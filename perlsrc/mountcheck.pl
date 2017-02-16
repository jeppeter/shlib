#! /usr/bin/env perl -w

use strict;
use Getopt::Long;

my ($prog)=$0;
my ($version)="0.0.1";
my ($verbose)=0;

my $(logo)= "mountcheck";

sub Debug($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose > 0) {
		if ($verbose >= 3) {
			my ($p,$f,$l) = caller;
			$fmtstr .= "[$f:$l] ";
		}
		$fmtstr .= $fmt;
		print STDERR "$fmtstr\n";
	}
}

sub Usage
{
	my ($ec) = shift @_;
	my ($fmt) = "";
	my ($fp) = \*STDERR;

	if ($ec == 0) {
		$fp = \*STDOUT;
	}

	if (scalar(@_) > 0) {
		$fmt = shift @_;
	}

	if (length($fmt) > 0) {
		print $fp "$fmt\n";
	}

	print $fp "$prog [OPTIONS] subcommand [FILTERS]...\n";
	print $fp "\t-h|--help                to display this help information\n";
	print $fp "\t-v|--verbose             to add verbose\n";
	print $fp "\t-k|--version             to print version\n";
	print $fp "\t-p|--prog progname       to specify progname\n";
	print $fp "subcommand:\n";
	print $fp "\t[mntpnt]   [devices]...  to get mount point ,if null display all the mount points\n";
	print $fp "\t[sharemnt]               to get mount point of shared on\n";

	exit($ec);
}

sub print_version()
{
	print STDOUT "$prog version $version\n";
	exit(0);
}

sub get_dev($)
{
	my ($l) = @_;
	my ($ml) = $l;
	my ($retl) = "";
	my ($tmpretl);
	my $cont=1;
	while ($cont) {
		$cont = 0;
		if ($ml =~ m/(.*?)\s+on\s+(.*?)/o) {
			$retl .= $1;
			$tmpretl = $1;
			if ($retl =~ m/\\/o) {
				$tmpretl =~ s/\\/\\\\/g;
				$ml =~ s/^$tmpretl //;
				Debug("ml [$ml] retl[$retl] tmpretl [$tmpretl]");
				$retl .= " ";
				if ($ml =~ m/^on/o) {
					$retl .= "on ";
					$ml =~ s/^on //;
					$cont = 1;
				}
			}
		}
	}
	if (length($retl) == 0) {
		$retl = $l;
	}
	return $retl;
}


sub get_mac_mntpnt($)
{
	my ($l) = @_;
	my ($ml) = $l;
	my ($cont);
	my $retl="";
	my ($tmpmnt);
	$cont = 1;
	while ($cont) {
		$cont = 0;
		if ($ml =~ m/(.*?)\((.*?)/o) {
			$retl .= $1;
			$tmpmnt = $1;

			if ($tmpmnt =~ m/\\$/o) {
				$tmpmnt =~ s/\\/\\\\/g;
				$ml =~ s/^$tmpmnt\(//;
				$retl .= "(";
				$cont = 1;
			} elsif ($tmpmnt =~ m/ $/o) {
				$retl =~ s/ $//;
			}
		}
	}
	if (length($retl) == 0) {
		$retl = $l;
	}
	return $retl;
}

sub get_linux_mntpnt($)
{
	my ($l) = @_;
	my ($ml) = $l;
	my ($cont);
	my $retl="";
	my ($tmpmnt);
	$cont = 1;
	while ($cont) {
		$cont = 0;
		if ($ml =~ m/(.*?) type\s+(.*?)/o) {
			$retl .= $1;
			$tmpmnt = $1;
			Debug("retl [$retl]");
			if ($tmpmnt =~ m/\\$/o) {
				$tmpmnt =~ s/\\/\\\\/g;
				$ml =~ s/^$tmpmnt type//;
				$retl .= " type";
				$cont = 1;
			} elsif ($tmpmnt =~ m/ $/o) {
				$retl =~ s/ $//;
			}
		}
	}
	if (length($retl) == 0) {
		$retl = $l;
	}
	return $retl;
}


sub mntpnt_handler
{
	my (@dirs)=@_;
	my ($osname)=`uname -s`;
	my (@mntpnt)=();
	my ($mntpart);
	my ($partmnt);
	my ($getdev,$tmpdev);
	chomp($osname);
	$osname = lc $osname;

	while(<STDIN>){
		my $l=$_;
		chomp($l);
		$getdev = get_dev($l);
		foreach (@dirs) {
			my ($p) = $_;
			if ($osname eq "darwin"){
				if ($p =~ m/^\/\//o) {
					$partmnt = $p;
					$partmnt =~ s/^\/\///;
					Debug("partmnt [$partmnt]");
					if ($getdev =~ m/\/\/(.*@)?$partmnt/) {
						$mntpart = $l;
						$getdev =~ s/\\/\\\\/g;
						$mntpart =~ s/^$getdev//;
						Debug("mntpart [$mntpart]");
						$mntpart =~ s/^ on //;
						Debug("mntpart [$mntpart]");
						push(@mntpnt,get_mac_mntpnt($mntpart));						
					}
				} else {
					if ($getdev eq $p) {
						$mntpart = $l;
						$p =~ s/\\/\\\\/g;
						$mntpart =~ s/^$p//;
						$mntpart =~ s/^ on //;
						push(@mntpnt,get_mac_mntpnt($mntpart));
					}
				}
			} elsif ($osname eq "linux") {
				if ($getdev eq $p) { 
					$mntpart = $l;
					$getdev =~ s/\\/\\\\/g;
					$mntpart =~ s/^$getdev//;
					$mntpart =~ s/^ on //;
					push(@mntpnt,get_linux_mntpnt($mntpart));
				}
			} else {
				die "[$osname] not supported";
			}
		}
	}
	return @mntpnt;
}

sub sharemnt_handler
{
	my ($osname)=`uname -s`;
	my (@mntpnt)=();
	my ($partmnt);
	my ($mntpart);
	my ($getdev,$tmpdev);
	chomp($osname);
	$osname = lc $osname;

	while(<STDIN>){
		my $l=$_;
		chomp($l);
		$getdev = get_dev($l);
		if ($getdev =~ m/^\/\//) {
			if ($osname eq "darwin"){
				$mntpart = $l;
				$getdev =~ s/\\/\\\\/g;
				$mntpart =~ s/^$getdev//;
				$mntpart =~ s/^ on //;
				push(@mntpnt,get_mac_mntpnt($mntpart));						
			} elsif ($osname eq "linux") {
				$mntpart = $l;
				$getdev =~ s/\\/\\\\/g;
				$mntpart =~ s/^$getdev//;
				$mntpart =~ s/^ on //;
				push(@mntpnt,get_linux_mntpnt($mntpart));
			} else {
				die "[$osname] not supported";
			}
		}
	}
	return @mntpnt;	
}

my ($versionmode)=0;
my ($help)=0;
GetOptions("v|verbose" => sub {
		$verbose ++;
	},
	"K|version" => sub {
			$versionmode ++;
		},
	"h|help" => sub {
		$help ++;
	},
	"p|prog=s" => \$prog);

if ($help > 0) {
	Usage(0,"");
} elsif ($versionmode > 0) {
	print_version();
}

my $subcommand;
if (scalar(@ARGV) == 0) {
	print STDERR "$prog no subcommand not set\n";
	exit(3);
}
$subcommand = shift @ARGV;
if ($subcommand eq "mntpnt") {
	my @mntpnt;
	@mntpnt=mntpnt_handler(@ARGV);
	foreach(@mntpnt) {
		print STDOUT "$_\n";
	}
} elsif ($subcommand eq "sharemnt") {
	my @mntpnt;
	@mntpnt =sharemnt_handler();
	foreach(@mntpnt) {
		print STDOUT "$_\n";
	}	
} else {
	print STDERR "[$subcommand] not supported\n";
	exit(4);
}