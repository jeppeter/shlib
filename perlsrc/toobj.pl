#! /usr/bin/env perl

use strict;
use Cwd "abs_path";
use File::Basename;
use Getopt::Long;
use File::Spec;

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

	print $fp "$0 [OPTIONS]  [dirs]...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\t-f|--fromdir [fromdir]  to fromdir\n";
	print $fp "\t-t|--todir   [todir]    to todir\n";
	print $fp "\n";
	print $fp "\t[dirs]                  if will give basename of it\n";

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

sub GetFullPath($)
{
	my ($c) =@_;
	return File::Spec->rel2abs($c);
}

my %opts;
my ($fromdir,$todir);
$fromdir="";
$todir="";
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		${opts{"verbose"}} ++;
	},
	"todir|t=s",
	"fromdir|f=s");

if (defined($opts{"help"})) {
	Usage(0,"");
}

if (defined($opts{"verbose"})) {
	$verbose = $opts{"verbose"};
}

if (defined($opts{"fromdir"})) {
	$fromdir=$opts{"fromdir"};
}

if (defined($opts{"todir"})) {
	$todir = $opts{"todir"};
}

my ($cnt)=0;
foreach(@ARGV) {
	my ($c) = $_;

	if (length($fromdir) > 0 && length($todir) > 0) {
		$c = GetFullPath($c);
		$c =~ s/^$fromdir/$todir/;
	}

	$c =~ s/\.[cS](pp)?$/.o/;
	Debug("in [$c]");
	if ($cnt > 0){
		print " ";
	}
	print "$c";
	$cnt ++;
}

if ($cnt > 0 && -t STDOUT) {
	Debug("in toobj return");
	print "\n";
}