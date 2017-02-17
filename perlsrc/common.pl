
use Cwd "abs_path";
use File::Basename;
use File::Spec;


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

sub FinalOutput($)
{
	my ($output) = @_;
	if ($output && -t STDOUT) {
		print "\n";
	}
}

sub GetFullPath($)
{
	my ($c) =@_;
	return File::Spec->rel2abs($c);
}

sub TrimRoot($)
{
	my ($c) = @_;
	my $curch;
	while (length($c) > 0 ) {
		$curch = substr($c,0,1);
		if ($curch eq "/" ||
			$curch eq "\\") {
			$c =~ s/.//;
		} else {
			last;
		}
	}
	return $c;
}
