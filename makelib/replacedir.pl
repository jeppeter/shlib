#! /usr/bin/env perl

use strict;
use Getopt::Long;
use File::Basename;
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
	print $fp "\t-f|--fromdir dir        to from directory\n";
	print $fp "\t-t|--todir dir          to todir \n";
	print $fp "\t-r|--replace regex      to replace value default s/\.c/\.o/\n";
	print $fp "\n";
	print $fp "\t[dirs]                  replace part from fromdir => todir\n";

	exit($ec);
}
my %opts;
my ($fromdir,$todir,$replace);
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{'verbose'})) {
			$opts{'verbose'} = 0;
		}
		${opts{'verbose'}} ++;
	},
	"todir|t=s",
	"fromdir|f=s");

if (defined($opts{'help'})) {
	Usage( 0,"");
}

if (!defined($opts{'fromdir'})) {
	Usage(3,"please specified --fromdir");
}
$fromdir = $opts{'fromdir'};
if (!defined($opts{'todir'})) {
	$todir = $fromdir;
} else {
	$todir = $opts{'todir'};
}

if (!defined($opts{'replace'})){
	$replace = 's/\.c/\.o/';
} else {
	$replace = $opts{'replace'};
}


foreach (@ARGV) {
	my ($cp) = File::Spec->rel2abs($_);
	my ($estr);
	$cp =~ s/^$fromdir/$todir/	;
	$estr = "\$cp =~ $replace";
	eval $estr;
	print STDOUT "$cp\n";
}

