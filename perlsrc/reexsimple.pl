#! /usr/bin/perl

use strict;
sub extract_string($$$)
{
    my ($restr,$eval,$instr) = @_;
    my ($outstr)="";
    if ($instr =~ m/$restr/) {
        if (length($eval) > 0) {
            $outstr= eval $eval;
        } else {
            $outstr= $instr;
        }
    }
    return $outstr;
}

if (scalar(@ARGV) == 1 && 
    ($ARGV[0] eq "-h" || $ARGV[0] eq "--help")) {
    print "$0 [restr] [evalstr] [instr]...\n";
    exit(0);
}

if (scalar(@ARGV) < 3) {
    print "$0 [restr] [evalstr] [instr]...\n";
    exit(3);
}
my ($restr) = shift @ARGV;
my ($evalstr) = shift @ARGV;
foreach (@ARGV) {
    my $outstr;
    $outstr = extract_string($restr,$evalstr,$_);
    print STDOUT "$outstr\n";
}