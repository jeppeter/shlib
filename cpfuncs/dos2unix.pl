#! /usr/bin/env perl -w

use strict;

sub dos2unix($)
{
	my ($file) =@_;
	my ($rfp,$wfp);
	my (@lines)=();
	undef($rfp);
	undef($wfp);

	open($rfp,"<$file") || die "can not open($file) for read ($!)";
	while(<$rfp>) {
		my ($l) = $_;
		$l =~ s/\r//g;
		push(@lines,$l);
	}
	close($rfp);
	undef($rfp);
	open($wfp,">$file") || die "can not open($file) for write($!)";
	while(scalar(@lines) > 0) {
		my ($l) = shift @lines;
		print $wfp "$l";
	}
	close($wfp);
	undef($wfp);
	return;
}

foreach(@ARGV) {
	dos2unix($_);
}