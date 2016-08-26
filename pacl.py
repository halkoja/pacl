#!/usr/bin/python
import sys

def printChangelog( pkg, n=-1, v=False ):
	from lxml import html
	from urllib2 import urlopen,HTTPError

	url = 'https://git.archlinux.org/svntogit/packages.git/log/trunk?h=packages/' + pkg
	
	desc = []
	hop=2
	
	if v:
		url = url + "&showmsg=1"
		hop=3
	
	try:
		ref = urlopen(url)
		page = ref.read()
		cod = ref.code
		ref.close()
	except HTTPError:
		print 'Error: Package "' + pkg + '" not found.'
		sys.exit(1)
	except Exception as e:
		print e
		sys.exit(1)
		
	tree = html.fromstring(page)

	data = tree.xpath('//table[@class="list nowrap"]/*[(self::tr and (@class="nohover" or @class="logheader"))]/td/*[not(@class="decoration")]//text() | //table[@class="list nowrap"]/tr/td[@class="logmsg"]//text()')

	dates = data[0::hop]
	# Ignore unicode characters since xpath doesn't parse them correctly.
	changes = [d.encode('ascii','ignore') for d in data[1::hop]]
	if v:
		desc = data[2::hop]
		desc = [x.split('\n') for x in desc]
		desc = [[x for x in y if x != ''] for y in desc]
		desc = [x[0:-1] for x in desc]
		desc = ['\n'.join(x) for x in desc]
		desc = [' ' + (d.encode('ascii','ignore')).replace('\n','\n ') for d in desc]

	if n > 0:
		dates = dates[0:n]
		changes = changes[0:n]
		desc = desc[0:n]

	dates = ['\033[1m' + d + '\033[0m' for d in dates]

	pad = max(len(s) for s in dates)+3
	fstr = "{:<" + str(pad) + "}{}"

	print '\033[34m' + pkg + '\033[0m:'
	if not(v):
		for d,c in zip(dates,changes):
			print(fstr.format(d,c))
	else:
		fstr = "{:<" + str(pad) + "}{}\n{}"
		fstre = "{:<" + str(pad) + "}{}"
		for d,c,dsc in zip(dates,changes,desc):
			if dsc != ' ':
				print(fstr.format(d,c,dsc))
			else:
				print(fstre.format(d,c))

def main(argv):
	n=-1
	pkg=None
	v=False
	
	stdi = False
	pkg = []
	if not sys.stdin.isatty():
		ars = sys.stdin.readlines()
		ars = [a.replace('\n','') for a in ars]
		pkg = reduce(lambda x,y: x+y, [a.split(' ') for a in ars])
		stdi=True
	
	
	estr = 'Usage: pacl [-v] [<number of entries>] <pkgname>'
	if len(argv) < 1 and not(stdi):
		print estr
		sys.exit()
	for s in argv:
		try:
			n=int(s)
		except ValueError:
			if s == '-h':
				print estr
				sys.exit()
			elif s == '-v':
				v=True
			elif s[0] != '-':
				pkg.append(s)
			elif not(stdi):
				print estr
				sys.exit(1) 				
	if pkg is None:
		print 'Package name required'
		sys.exit(2)
	[printChangelog(p,n,v) for p in pkg]

if __name__ == "__main__":
	main(sys.argv[1:])
