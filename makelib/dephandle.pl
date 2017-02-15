#! /usr/bin/env perl -w

use Getopt::Long;

my ($replace) = "";
my (@sarr);

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
	print $fp "\n";
	print $fp "\t[dirs]                  if will give real path of it\n";

	exit($ec);
}

my %opts;
my ($lineno)=0;
my ($linecont)=0;
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		${opts{"verbose"}} ++;
	});

if (defined($opts{"verbose"})) {
	$verbose = $opts{"verbose"};
}

if (scalar(@ARGV) > 0)  {
	$replace = shift @ARGV;
	Debug("replace [$replace]");
}
while(<STDIN>){
	my ($l) = $_;
	my ($i);
	if ($lineno == 0){
		if ($l =~ m/(.*:)/o) {		
			$l =~ s/$1/$replace += /;
			chomp($l);
			@sarr = split(/\s+/,$l);
			$l = "";
			for ($i=0;$i<scalar(@sarr);$i++) {
				if ($i == 2 && $sarr[$i] ne "\\") {
					Debug("[$i]=".$sarr[$i]);
					next;
				}
				if ($i > 0) {
					$l .= " ";
				}
				$l .= $sarr[$i];
			}
			if ($l =~ m/\\$/o) {
				$l =~ s/\\$//;
				$linecont = 1;
				Debug ("[$lineno]($l) continue");
			}
			$l .= "\n";
		}
	} elsif ($linecont > 0) {
		$linecont = 0;
		chomp($l);
		$l = "$replace += $l";
		Debug("[$lineno]=$l");
		if ($l =~ m/\\$/o) {
			$l =~ s/\\$//;
			$linecont = 1;
			Debug ("[$lineno]($l) continue");
		}
		$l .= "\n";
	}
	print $l;
	$lineno ++;
}