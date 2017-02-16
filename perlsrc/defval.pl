#! /usr/bin/env perl

use strict;
use Getopt::Long;

sub Usage($$)
{
	my ($ec,$fmt)=@_;
	my ($fp)=\*STDERR;

	if ($ec == 0) {
		$fp =\*STDOUT;
	}

	if (length($fmt) > 0) {
		print $fp "$fmt\n";
	}

	print $fp "$0 [OPTIONS]  [values]...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\n";
	print $fp "\t[values]                test value if not zero length\n";

	exit($ec);
}

my ($logo)="defval";

my ($verbose)=0;


sub Debug($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose > 0) {
		if ($verbose >= 3) {
			my ($p,$f,$l) = caller;
			$fmtstr = "[$f:$l] ";
		}
		$fmtstr .= $fmt;
		print STDERR "$fmtstr\n";
	}
}

my %opts;
my ($cnt)=0;
my ($idx)=0;
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		${opts{"verbose"}} ++;
	});

if (defined($opts{"help"})) {
	Usage(0,"");
}

if (defined($opts{"verbose"})) {
	$verbose = $opts{"verbose"};
}

foreach(@ARGV) {
	my ($c) = $_;
	Debug("[$idx]=[$c]");
	if (length($c) > 0) {
		print "$c";
		$cnt ++;
		last;
	}
	$idx ++;
}
if ($cnt > 0 && -t STDOUT) {
	print "\n";
}