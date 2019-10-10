import sys

def write_obj_function(opb, n_v):
	opb += "min: "
	for i in range(1, n_v+1):
		opb += f"1 x{i} "
	opb += ";\n"
	return opb

file = open(sys.argv[1])

opb = ""

for line in file:
	if line[0] == "c":    # ignore comments
		continue
	elif line[0] == "h":  # read header. v = num vertices, e = num edges
		n_v, n_e = map(int, line.split()[1:])
		opb = write_obj_function(opb, n_v)
	elif line.strip():
		e, f = [int(i) for i in line.split()] # (e, f) is an edge in the graph
		# add clause for pairs of vertices that are connected by an edge
		opb += f"1 x{e+1} +1 x{f+1} >= 1;\n"

# number of clauses
n_c = opb.count("\n") - 1

print(f"* #variable= {n_v} #constraint= {n_c}")
print(opb)