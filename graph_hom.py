import numpy as np

def H(k, V, E, Z):
	# map of vertex to index
	G = {}
	vnum = {}
	for i, v in enumerate(V):
		vnum[v] = i
		G[v] = []

	for (v_1, v_2) in E:
		G[v_1].append(v_2)
		G[v_2].append(v_1)

	# partial function
	partial_1 = np.zeros((len(V), len(E)))

	for i, (v_1, v_2) in enumerate(E):
		partial_1[vnum[v_1], i] = 1
		partial_1[vnum[v_2], i] = 1

	ans = solve(partial_1)

	if k == 0:
		# equivalence classes
		equiv = []
		equiv.append(set('0'))

		# find vertices that are equivalent to 0
		for a in ans:
			if np.count_nonzero(a) == 1:
				equiv[0].add(V[np.argmax(a > 0)])

		# do the rest
		visited = []
		for v in V:
			visited.append(False)

		for v in V:
			if v not in equiv[0] and not visited[vnum[v]]:
				s = set(v)
				dfs(G, vnum, v, visited, s)
				equiv.append(s)

		return equiv

	if k == 1:
		return ans

def solve(arr):
	row, col = arr.shape
	ans = []

	n = 2**col
	for i in range(n):
		sol = np.zeros((col, 1))
		b = bin(i)[2:]
		for j, c in enumerate(b[::-1]):
			if c == '0':
				sol[col-j-1, 0] = 0
			else:
				sol[col-j-1, 0] = 1
		if np.count_nonzero(np.matmul(arr, sol) % 2) == 0:
			ans.append(sol)
	return ans

def dfs(G, vnum, v, visited, s):
	if len(G[v]) == 0:
		return
	for child in G[v]:
		if not visited[vnum[child]]:
			visited[vnum[child]] = True
			s.add(child)
			dfs(G, vnum, child, visited, s)
	return

def run(n):
	if n == 1.6:
		V = ['a','b','c','d','e']
		E = [('a','b'), ('b','c'), ('c','d'), ('d','e')]
	elif n == 1.7:
		V = ['a','b','c','d']
		E = [('a','b'), ('b','c'), ('d','c'), ('a','d')]
	elif n == 1.8:
		V = ['1', '2']
		E = [('1', '2')]
	elif n == 1.9:
		V = ['a','b','c','d']
		E = [('a','b'), ('b','c'), ('b','d')]
	else:
		V = []
		for i in range(n):
			V.append(str(i))
		E = []
		for i in range(n):
			for j in range(i+1, n):
				E.append((V[i], V[j]))
		print(V)
		print(E)

	print(H(0, V, E, 2))
	print(H(1, V, E, 2))

if __name__ == '__main__':
	run(5)
