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

	print $fp "$0 [OPTIONS]  [targets]...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\t-i|--input              to input for file default stdin\n";
	print $fp "\n";
	print $fp "\t[targets]               targets to filter\n";

	exit($ec);
}

my $logo="maketarget";

my ($verbose)=0;

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

sub GetMakeTarget($)
{
	my ($input) = @_;
	my ($fp) = \*STDIN;
	my (@targets)=();
	my ($macromode)=0;
	my ($emptyline)=0;
	my ($l);
	my $idx=0;
	my $tgt;


	if ($input ne "-") {
		open($fp,"< $input") || die "could not open ($input)($!)";
	}

	while (<$fp>) {
		$idx ++;
		$l = $_;
		chomp($l);
		#Debug("[$idx][$l]macromode[$macromode]emptyline[$emptyline]");
		if ($macromode > 0) {
			if ($l =~ m/^endef\s*$/o){
				#Debug("[$idx]endef");
				$macromode = 0;
			}
			next;
		} elsif ($emptyline > 0) {
				
				if ($l =~ m/(.*?):/o && !($l =~ m/^\#/o)) {
					$tgt = $1;
					Debug("[$idx]$l ($tgt)");
					push(@targets,$tgt);
				} 
		

		}
		if ($l =~ m/^define\s+/o) {
			#Debug("[$idx]define");
			$macromode = 1;
		}

		$emptyline = 0;
		if ($l =~ m/^\s*$/o) {
			#Debug("[$idx]emptyline");
			$emptyline = 1;
		} 


	}
	if ($fp != \*STDIN) {
		close($fp);
	}
	undef($fp);
}

my %opts;
my ($inputfile)="-";
my @targets;
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		${opts{"verbose"}} ++;
	},
	"input|i=s");

if (defined($opts{"help"})) {
	Usage(0,"");
}

if (defined($opts{"verbose"})) {
	$verbose = $opts{"verbose"};
}

if (defined($opts{"input"})) {
	$inputfile=$opts{"input"};
}

@targets = GetMakeTarget($inputfile);