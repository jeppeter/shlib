#! /usr/bin/env perl -w
my ($replace) = "";
my (@sarr);

if (scalar(@ARGV) > 0)  {
	$replace = shift @ARGV;
	#print STDERR "replace [$replace]\n";
}
while(<STDIN>){
	my ($l) = $_;
	my ($i);
	if ($l =~ m/(.*:)/o) {		
		$l =~ s/$1/$replace += /;
		chomp($l);
		@sarr = split(/\s+/,$l);
		$l = "";
		for ($i=0;$i<scalar(@sarr);$i++) {
			if ($i == 2) {
				next;
			}
			if ($i > 0) {
				$l .= " ";
			}
			$l .= $sarr[$i];
		}
		$l .= "\n";
	}
	print $l;
}