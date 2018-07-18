#! /usr/bin/env python

import extargsparse
import sys
import logging
import os

class CheckFiles(object):
	def __init__(self,crignore=True):
		self.only = []
		self.diffs = []
		self.crignore = crignore
		return

	def check_file_same(self,leftfile,rightfile):
		llines = []
		logging.info('leftfile [%s] rightfile [%s]'%(leftfile,rightfile))
		with open(leftfile,'rb') as f:
			for l in f:
				llines.append(l)
		rlines = []
		with open(rightfile,'rb') as f:
			for l in f:
				rlines.append(l)

		if len(llines) != len(rlines):
			logging.warn('[%s] (%d) != [%s] (%d)'%(leftfile,len(llines),rightfile,len(rlines)))
			return False

		i = 0
		while i < len(llines):
			ll = llines[i]
			rl = rlines[i]
			if rl != ll:
				if not self.crignore:
					diffcnt = 0
					while diffcnt < len(ll) or diffcnt < len(rl):
						if ll[diffcnt] != rl[diffcnt]:
							break
						diffcnt = diffcnt + 1
					s = '[%d]([%s]<>[%s]) at offset[%d] (0x%02x) <> (0x%02x)\n'%(i,leftfile,rightfile,diffcnt,ord(ll[diffcnt]),ord(rl[diffcnt]))
					s += 'from >>>>>>>>>>>>>>>>\n'
					s += '%s'%(ll)
					s += 'to <<<<<<<<<<<<<<<<<<<\n'
					s += '%s'%(rl)
					if self.crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
				ll = ll.replace('\r','')
				rl = rl.replace('\r','')
				if ll != rl:
					diffcnt = 0
					while diffcnt < len(ll) or diffcnt < len(rl):
						if ll[diffcnt] != rl[diffcnt]:
							break
						diffcnt = diffcnt + 1
					s = '[%d]([%s]<>[%s]) at offset[%d] (0x%02x) <> (0x%02x)\n'%(i,leftfile,rightfile,diffcnt,ord(ll[diffcnt]),ord(rl[diffcnt]))
					s += 'from >>>>>>>>>>>>>>>>\n'
					s += '%s'%(ll)
					s += 'to <<<<<<<<<<<<<<<<<<<\n'
					s += '%s'%(rl)
					if self.crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
			i = i + 1
		return True


	def __format(self):
		s = ''
		s += 'only %s diffs %s'%(self.only, self.diffs)
		return s

	def __str__(self):
		return self.__format()

	def __repr__(self):
		return self.__format()


class CompoundCheckFiles(CheckFiles):
	def __init__(self,crignore=True):
		super(CompoundCheckFiles,self).__init__(crignore)
		self.left_diffs = []
		self.right_diffs = []
		self.left_only = []
		self.right_only = []
		return

	def __format(self):
		s = ''
		s += 'right_only %s left_only %s left_diffs %s right_diffs %s crignore %s'%(self.right_only, self.left_only, self.left_diffs,self.right_diffs,self.crignore)
		return s

	def __str__(self):
		return self.__format()

	def __repr__(self):
		return self.__format()

class DiffDir(object):
	def __init__(self):
		return

	def __compare_dir(self,fromdir,todir,crignore=True):
		cfs = CheckFiles(crignore)
		for root, dirs,files in os.walk(fromdir):
			if root == fromdir  or root == os.path.join(fromdir,os.pathsep):
				npart = ''
			else:
				npart = os.path.relpath(root,fromdir)
			logging.info('npart %s root %s'%(npart, root))
			for d in dirs:
				nd = os.path.join(npart,d)
				nfdir = os.path.join(root,d)
				ntdir = os.path.join(todir,npart,d)
				if not os.path.exists(ntdir):					
					if nd not in cfs.only:
						cfs.only.append(nd)
					continue
			for f in files:
				nf = os.path.join(npart,f)
				nffile = os.path.join(root,f)
				ntfile = os.path.join(todir,npart,f)
				if not os.path.exists(ntfile):
					if nf not in cfs.only:
						cfs.only.append(nf)
					continue
				# now we should check whether
				if (os.path.islink(ntfile) and not (os.path.islink(nffile))) or (not os.path.islink(ntfile) and (os.path.islink(nffile))):
					if nf not in cfs.diffs:
						cfs.diffs.append(nf)
					continue

				retval = cfs.check_file_same(nffile,ntfile)	
				if not retval:
					if nf not in cfs.diffs:
						cfs.diffs.append(nf)
		return cfs

	def dircompare(self,fromdir,todir,crignore=True):
		compound = CompoundCheckFiles(crignore)
		cfs = self.__compare_dir(fromdir, todir,crignore)
		for d in cfs.diffs:
			nd = os.path.join(fromdir,d)
			if nd not in compound.left_diffs:
				compound.left_diffs.append(nd)
		for d in cfs.only:
			nd = os.path.join(fromdir,d)
			if nd not in compound.left_only:
				compound.left_only.append(nd)

		cfs = self.__compare_dir(todir,fromdir,crignore)
		for d in cfs.diffs:
			nd = os.path.join(todir,d)
			if nd not in compound.right_diffs:
				compound.right_diffs.append(nd)
		for d in cfs.only:
			nd = os.path.join(todir,d)
			if nd not in compound.right_only:
				compound.right_only.append(nd)
		return compound

def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    if logging.root and logging.root.handlers :
    	logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return


def main():
	commandline='''
	{
		"verbose|v" : "+"
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	set_log_level(args)
	i = 0
	argc = len(args.args)
	d = DiffDir()
	while i < (argc -1):
		cfs = d.dircompare(args.args[i], args.args[i+1])
		logging.info('cfs %s'%(repr(cfs)))
		i += 2
	return

main()