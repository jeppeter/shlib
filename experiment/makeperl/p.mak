
all:
	@perl -e "my (\$$cmd)=\"\#! /usr/bin/env perl\n\nuse strict;\nmy (\\\$$cmd) = \\\"hello\\\\\\\"'\\\\\\\$$\\\\\\\`\\\\\#\\\";\nprint \\\$$cmd;\";print \$$cmd;"