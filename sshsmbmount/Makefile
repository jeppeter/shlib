
all:sshsmbmount

sshsmbmount:sshsmbmount.tmpl check_split_awk
	${QUIET}bash ${TOPDIR}/changefile -i split.awk -P sshsmbmount.tmpl -o sshsmbmount -p '%SPLITAWK_STR%'

check_split_awk:split.awk
	${QUIET}bash ${TOPDIR}/changefile -i split.awk -P ${TOPDIR}/echocode.tmpl -o split_awk.tmp -p '%REPLACE_PATTERN%'
	${QUIET}bash split_awk.tmp > split_awk_res.tmp
	${QUIET}diff -q -B -Z split_awk_res.tmp split.awk || (echo "not change right for split.awk" && exit 3)

clean:
	${QUIET}rm -f sshsmbmount *.tmp
