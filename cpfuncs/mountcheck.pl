#! /usr/bin/env perl -w

use strict;
use Getopt::Long;

my ($prog)=$0;
my ($version)="0.0.1";

sub Usage
{
	my ($ec) = shift @_;
	my ($fmt) = "";
	my ($fp) = \*STDERR;
	if (scalar(@_) > 0) {
		$fmt = shift @_;
	}

	print $fp "$prog [OPTIONS] subcommand [FILTERS]...\n";
	print $fp "\t-h|--help                to display this help information\n";
	print $fp "\t-V|--version             to print version\n";
	print $fp "subcommand:\n";
	print $fp "\t[mntpnt]   [devices]...  to get mount point ,if null display all the mount points\n";
	print $fp "\t[sharemnt]               to get mount point of shared on\n";

	exit($ec);
}

sub print_version()
{
	print \*STDOUT "$prog version $version\n";
	exit(0);
}

sub mntpnt_handler
{
	my (@dirs)=@_;
	my ($osname)=`uname -r`;
	my ($fh);
	my (@mntpnt);
	chomp($osname);
	$osname = lc $osname;

	open($fh,"mount |") || die "could not make mount";
	while (<$fh>) {
		my $l=$_;
		chomp($l);
		foreach()
	}
	close($fh);
	return @mntpnt;
}

my ($help,$)