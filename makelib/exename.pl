#! /usr/bin/env perl

use strict;
use Getopt::Long;
use File::Basename;

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

	print $fp "$0 [OPTIONS]  [exe]...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\n";
	print $fp "\t[exe]                   fileter out exename without .exe\n";

	exit($ec);
}

my ($verbose)=0;

sub Debug($)
{
	my ($fmt)=@_;
	my ($fmtstr)="";
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
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		$opts{"verbose"}++;
	});

if (defined($opts{"help"})) {
	Usage( 0,"");
}

if (defined($opts{"verbose"})) {
	$verbose=$opts{"verbose"};
}

if (scalar(@ARGV) > 0) {
	foreach (@ARGV) {
		my ($cp) = basename($_);
		Debug("cp [$cp]");
		if ($cp =~ m/\.exe$/o) {
			$cp =~ s/\.exe$//;
		}
		print STDOUT "$cp\n";
	}
}

