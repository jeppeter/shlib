#! /usr/bin/env awk -f

{
	curidx=1;
	curitem="";
	printout=0;
	curcon=$0;
	n=split($0,a);	
	for(i=1;i<=NF;i++) {
		spaces="";
		
		idx=index(curcon,a[i]);
		if(idx>1) {
			spaces=substr(curcon,1,idx-1);
			curcon=substr(curcon,length(spaces)+1);
		}
		curcon=substr(curcon,length(a[i])+1);
		if(length(a[i])==0) {
			if(length(curitem)>0){
			curitem=sprintf("%s%s",curitem,spaces);
		}
		continue;
	}
		if(a[i]==splitchar) {
			if(curidx==searchidx) {
				printf("%s\n",curitem);
				printout=1;break;
			}
			curitem="";
			curidx+=1;
			continue;
		}
		if(length(curitem)>0) {
			curitem=sprintf("%s%s%s",curitem,spaces,a[i]);
		} else {
			curitem=$i;
		}
	}
	if(printout==0&&curidx==searchidx){
		printf("%s\n",curitem);
		printout=1;
	}
}