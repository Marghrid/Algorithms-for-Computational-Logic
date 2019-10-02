import sys

file = open(sys.argv[1])

dimacs = ''

for line in file:
	if line[0] == 'c':    # ignore comments
		continue
	elif line[0] == 'h':  # read header. v = num vertices, e = num edges
		_, v, e = line.split()
	elif line.strip():
		e, f = [int(i) for i in line.split()]
		# add clause for pairs of vertices that are connected by an edge
		dimacs += "100 {} {} 0\n".format(e+1, f+1)

# add clause for all vertices
for i in range(int(v)):
	dimacs += "1 {} 0\n".format(-(i+1))

# number of clauses
n_c = dimacs.count('\n')

print("p wcnf {} {} 100".format(v, n_c))
print(dimacs)