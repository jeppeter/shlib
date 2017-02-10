#! /usr/bin/env perl

use strict;
use Getopt::Long;
use Data::Dumper;

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

	print $fp "$0 [OPTIONS] [subcommands] ...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\t-T|--target target      to specify target lists\n";
	print $fp "\t-i|--input inputfile    to specify input default (STDIN)\n";
	print $fp "[subcommands]\n";
	print $fp "\t[disk]                  to get information of disk\n";

	exit($ec);
}

sub disk_Usage($$)
{
	my ($ec,$fmt)=@_;
	my ($fp)=\*STDERR;

	if ($ec == 0) {
		$fp =\*STDOUT;
	}

	if (length($fmt) > 0) {
		print $fp "$fmt\n";
	}

	print $fp "$0  disk [OPTIONS] ...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";

	exit($ec);
}

sub disk_get($$)
{
	my ($targetref,$input)=@_;
	my ($fp);
	my %diskpairs=();
	if (!defined($targetref)){
		disk_Usage(3,"please specify a target at least by --target|-T");
	}
	if ($input eq "-") {
		$fp = \*STDIN;
	} else {
		open($fp,"< $input") || die "can not open <$input> error<$!>";
	}
	while(<$fp>) {
		
	}
	if ($fp != \*STDIN) {
		close($fp);
	}
	undef($fp);
	return %diskpairs;
}

my %args=();
my @oldargv=@ARGV;
my ($subcommand);

Getopt::Long::Configure("no_ignorecase","bundling");

Getopt::Long::GetOptions(\%args,
	"help|h",
	"target|T=s@",
	"input|i=s",
	"verbose|v" => sub {
			if (!defined($args{'verbose'})) {
				$args{'verbose'} = 0;
			}
			$args{'verbose'} ++;
		}) || die "can not parse [@oldargv]";


if (scalar(@ARGV) == 0) {
	if (defined($args{'help'})) {
		Usage(0,"");
	}	
	Usage(3 , "please specify a subcommand");
} 

$subcommand = shift @ARGV;

if ($subcommand eq "disk") {
	my ($targetref,$input);
	my (%diskp);
	undef($targetref);
	$input="-";
	if (defined($args{'help'})) {
		disk_Usage(0,"");
	}

	if (defined($args{'target'})) {
		$targetref = $args{'target'};
	}
	if (defined($args{'input'})) {
		$input = $args{'input'};
	}
	%diskp = disk_get($targetref,$input);
	print Dumper(%diskp);
} else {
	usage(3,"unknown subcommand [$subcommand]");
}

