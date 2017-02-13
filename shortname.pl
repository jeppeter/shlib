#! /usr/bin/env perl

use strict;
use Getopt::Long;
use File::Basename;
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
my %opts;
my ($topdir);
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{'verbose'})) {
			$opts{'verbose'} = 0;
		}
		${opts{'verbose'}} ++;
	},
	"topdir|t=s");

if (defined($opts{'help'})) {
	Usage( 0,"");
}
$topdir = "";
if (defined($opts{'topdir'})) {
	$topdir = $opts{'topdir'};
}

foreach (@ARGV) {
	my ($cp) = abs_path($_);
	if (length($topdir)) {
		$cp =~ s/$topdir//;
	} else {
		$cp = basename($cp);
	}

	$cp =~ s/\./_/g;
	$cp =~ s/\//_/g;
	$cp =~ s/\\/_/g;
	print STDOUT "$cp\n";
}

