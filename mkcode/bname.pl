#! /usr/bin/env perl

use File::Basename;

foreach (@ARGV) {
	print basename($_)."\n";
}