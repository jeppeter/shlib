#! /usr/bin/env perl

use strict;
use Cwd "abs_path";

foreach(@ARGV) {
	print abs_path($_).''."\n";
}