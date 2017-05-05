
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

sub Error($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose >= 3) {
		my ($p,$f,$l) = caller;
		$fmtstr .= "[$f:$l] ";
	}
	$fmtstr .= $fmt;
	print STDERR "$fmtstr\n";
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
	if ( -e $c && !( -l $c) ) {
		return abs_path($c);
	}
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

sub format_out($$$@)
{
	my ($simple,$hashref,$notice,@vals)=@_;
	my ($outstr)="";
	my (@arr);
	foreach (@vals) {
		my ($curval) = $_;
		if (defined($hashref->{$curval})) {
			if ($simple) {
				if (ref ($hashref->{$curval}) eq "ARRAY") {
					@arr = @{$hashref->{$curval}};
					foreach (@arr) {
						$outstr .= "$_\n";	
					}
				} else{
					$outstr .= $hashref->{$curval}."\n";
				}
			} else {
				if (ref ($hashref->{$curval}) eq "ARRAY") {
					@arr = @{$hashref->{$curval}};
					foreach (@arr) {
						$outstr .= "$_ $curval $notice\n";
					}
				} else {
					$outstr .= $hashref->{$curval}." $curval $notice\n";
				}
			}
		}
	}
	return $outstr;
}

sub trimspace($)
{
	my ($retl)=@_;
	$retl =~ s/^\s+//;
	$retl =~ s/\s+$//;
	return $retl;
}
