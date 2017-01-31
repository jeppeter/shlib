#! /usr/bin/env perl -w

use strict;
use Cwd "abs_path";

my ($basepath)="";
if (scalar(@ARGV) > 0) {
	$basepath=shift @ARGV;
}
if ( -e "$basepath" ) {
	$basepath = abs_path($basepath);
}
while(<STDIN>){
	my ($l)=$_;
	my ($subpath)="";
	chomp($l);
	if ( -e "$l") { 
		$l = abs_path($l);
	}
	$subpath = $l;
	$subpath =~ s/$basepath//;
	#print STDERR "basepath[$basepath] l[$l] subpath[$subpath]\n";
	if (length($subpath) == 0) {
		$subpath = ".";
	} 
	while(substr($subpath,0,1) eq "/") {
		$subpath =~ s/\///;
	}
	print "$subpath\n";
}