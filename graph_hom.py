import numpy as np
import sys

def H(k, V, E, Z):
	C_0 = lc(len(V))
	C_1 = lc(len(E))

	# partial function
	partial_1 = np.zeros((len(V), len(E)))
	for i, (v_1, v_2) in enumerate(E):
		partial_1[V.index(v_1), i] = 1
		partial_1[V.index(v_2), i] = 1

	Z_0 = C_0
	Z_1 = ker(partial_1, C_1, C_0)

	B_0 = img(partial_1, C_1, C_0)
	B_1 = []

	if k == 0:
		equiv = {}
		for i in range(len(Z_0)):
			for j in range(i+1, len(Z_0)):
				b = (Z_0[j] - Z_0[i]) % 2
				if np.any(np.array_equal(b, x) for x in B_0):
					if np.sum(Z_0[i]) == 1 and np.sum(Z_0[j]) == 1:
						if V[np.argmax(Z_0[i])] not in equiv:
							equiv[V[np.argmax(Z_0[i])]] = []
						if V[np.argmax(Z_0[j])] not in equiv:
							equiv[V[np.argmax(Z_0[j])]] = []
						equiv[V[np.argmax(Z_0[i])]].append(V[np.argmax(Z_0[j])])
						equiv[V[np.argmax(Z_0[j])]].append(V[np.argmax(Z_0[i])])

		ZqB = [[0]]
		vis = set()
		for v in V:
			if not (v in vis):
				vis.add(v)
				e = dfs(equiv, [v], vis, v)
				if len(e) != 0:
					ZqB.append(e)
		return ZqB
	if k == 1:
		return Z_1

# f: A->B
def img(f, A, B):
	ans = []
	for a in A:
		fa = np.matmul(f, a) % 2
		if np.any(np.array_equal(fa, x) for x in A):
			ans.append(fa)
	return ans

# f: A->B
def ker(f, A, B):
	row, col = f.shape
	sol = lc(col)
	ans = []

	for v in sol:
		if np.count_nonzero(np.matmul(f, v) % 2) == 0:
			ans.append(v)

	return ans

# all linear combinations in mod 2
def lc(n):
	m = 2**n
	ans = []
	for i in range(m):
		b = bin(i)[2:]
		v = np.zeros(n)
		for j, c in enumerate(b[::-1]):
			if c == '0':
				v[n-j-1] = 0
			else:
				v[n-j-1] = 1
		ans.append(v)
	return ans

def dfs(equiv, e, vis, v):
	if len(equiv[v]) == 0:
		return e
	for w in equiv[v]:
		if w not in vis:
			e.append(w)
			vis.add(w)
			dfs(equiv, e, vis, w)

	return e

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
	elif n == 0.1:
		V = ['a','b','c','d']
		E = [('a', 'b'), ('a','c'), ('b','c'), ('b','d'), ('c','d')]
	else:
		n = int(n)
		V = []
		for i in range(n):
			V.append(str(i))
		E = []
		for i in range(n):
			for j in range(i+1, n):
				E.append((V[i], V[j]))

	print(H(0, V, E, 2))
	print(H(1, V, E, 2))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: python graph_hom.py <exercise/n>')
	else:
		run(float(sys.argv[1]))
