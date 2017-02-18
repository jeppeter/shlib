
all:
	@perl -e "my (\$$cmd)=\"\#! /usr/bin/env perl\n\nuse strict;\nmy (\\\$$cmd) = \\\"hello\\\\\\\"'\\\\\\\$$\\\\\\\`\\\\\@_\\\\\#\\\";\nprint \\\$$cmd;\";print \$$cmd;"