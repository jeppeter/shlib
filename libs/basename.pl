#! /usr/bin/env perl

use strict;

use File::Basename;

foreach (@ARGV)  {
	print basename($_)."\n";
}