#! /usr/bin/env perl

use strict;
use Getopt::Long;
use File::Basename;
use File::Spec;
use Cwd "abs_path";

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
	print $fp "\t-t|--topdir dir         to make replace dir\n";
	print $fp "\n";
	print $fp "\t[dirs]                  if not set topdir ,it will get the basename\n";

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
my ($topdir);
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		$opts{"verbose"}++;
	},
	"topdir|t=s");

if (defined($opts{"help"})) {
	Usage( 0,"");
}
$topdir = "";
if (defined($opts{"topdir"})) {
	$topdir = $opts{"topdir"};
}

if (defined($opts{"verbose"})) {
	$verbose=$opts{"verbose"};
}

if (scalar(@ARGV) > 0) {
	foreach (@ARGV) {
		my ($cp) = $_;
		if ( -l "$cp") {
			$cp = File::Spec->rel2abs($cp);
		} else {
			$cp = abs_path($cp);
		}
		Debug("cp [$cp]");
		if (length($topdir) > 0) {
			$cp =~ s/$topdir//;
			while (length($cp) > 0 ) {
				if ($cp =~ m/^\//o || 
					$cp =~ m/^\\/o) {
					$cp =~ s/.//;
				} else {
					last;
				}
			}
			Debug("change topdir[$topdir] [$cp]");
		} else {
			$cp = basename($cp);
			Debug("basename");
		}

		$cp =~ s/\./_/g;
		$cp =~ s/\//_/g;
		$cp =~ s/\\/_/g;
		print STDOUT "$cp\n";
	}
}

