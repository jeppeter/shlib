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

sub disk_get($)
{
	my ($input)=@_;
	my ($fp);
	my %diskpairs=();
	my ($curtarget);
	my ($curdisk);
	if (!defined($input) || $input eq "-") {
		$fp = \*STDIN;
	} else {
		open($fp,"< $input") || die "can not open <$input> error<$!>";
	}
	undef($curtarget);
	while(<$fp>) {
		my ($l) = $_;
		chomp($l);
		if ($l =~ m/^Target:\s+(.*)/o) {
			$curtarget = $1;
		} elsif ($l =~ m/^\s+Attached scsi disk\s+([a-zA-Z_0-9]+)\s+/o) {
			$curdisk = "/dev/$1";
			if (!defined($diskpairs{$curtarget})) {
				my (@arr)=();
				push(@arr,$curdisk);
				$diskpairs{$curtarget} = \@arr;
			} else {
				push(@{diskpairs{$curtarget}},$curdisk);
			}
		}
		
	}
	if ($fp != \*STDIN) {
		close($fp);
	}
	undef($fp);
	return \%diskpairs;
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
	my ($diskp);
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
	$diskp = disk_get($input);
	if (!defined($diskp)) {
		print STDERR "can not parse [$args{'input'}]";
		exit 3;
	} 
	foreach (keys(%{$diskp})) {
		my ($curk) = $_;
		foreach (@{$args{'target'}}) {
			my ($cmpk) = $_;
			my ($i,$j,$curarr);
			if ($curk eq $cmpk) {
				print STDOUT "$curk:\n";
				for ($i=0;$i< scalar(@{$diskp->{$curk}});$i++) {
					print STDOUT "    ".$diskp->{$curk}->[$i]."\n";
				}
			}
		}
	}
} else {
	usage(3,"unknown subcommand [$subcommand]");
}

