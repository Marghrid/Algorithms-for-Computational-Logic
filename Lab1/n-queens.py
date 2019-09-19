# N Queen problem
import sys

N = 8

def cell(r, c): 
    return (r*N + c) + 1

def main():
    dimacs = ''
    # Rows
    for r in range(N):
        for c in range(N):
            dimacs += f"{cell(r, c)} "
        dimacs += "0\n"
    
    for r in range(N):
        for c in range(N):
            for k in range(c+1, N):
                dimacs += f"{-cell(r, c)} {-cell(r, k)} 0\n"

    # Columns
    for c in range(N):
        for r in range(N):
            dimacs += f"{cell(r, c)} "
        dimacs += "0\n"

    for c in range(N):
        for r in range(N):
            for k in range(r+1, N):
                dimacs += f"{-cell(r, c)} {-cell(k, c)} 0\n"
    
    for r in range(N):
        for c in range(N):
            for k in range(1, min(N-r, N-c)):
                dimacs += f"{-cell(r, c)} {-cell(r+k, c+k)} 0\n"

            for k in range(1, min(N-r, c+1)):
                dimacs += f"{-cell(r, c)} {-cell(r+k, c-k)} 0\n"

    n_clauses = dimacs.count('\n')
    header = f"p cnf {N*N} {n_clauses}\n"
    dimacs = header + dimacs
    print(dimacs)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    main()

