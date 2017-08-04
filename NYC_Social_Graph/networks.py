# build the social networks

import pickle
import codecs
import networkx as nx

def flatten_graph(M):
	"""Takes a multigraph & returns weighted graph"""
	G = nx.Graph()
	for u,v,data in M.edges_iter(data=True):
    		w = data['weight']
    		if G.has_edge(u,v):
        		G[u][v]['weight'] += w
    		else:
        		G.add_edge(u, v, weight=w)
	return G

# Degree: find 100 most popular people
def solve_Degree(M):
	cx_count = [i for i in M.degree_iter()] 
	popular = sorted(cx_count, key=lambda cx: cx[1], reverse=True)
	top = popular[0:100]
	return top 

# PageRank: find top 100 by Page Rank
def solve_PageRank(G):
	rank = nx.pagerank(G)
	ranksort = sorted(rank.items(), key=lambda rank: rank[1], reverse=True)
	highest = ranksort[0:100]
	return highest
 
# BestFriends: find 100 edges with the highest weights
def solve_BestFriends(G):
	friends = sorted(G.edges(data=True), key=lambda \
			 (source,target,data): data['weight'], reverse=True)
	bffs = friends[0:100]
	return bffs, friends

def solve_Degree2(BFFS):
        G = nx.Graph()
        G.add_weighted_edges_from(BFFS)
        degrees = []
        for n,nbrs in G.adjacency_iter():
            degree = 0
            for nbr,eattr in nbrs.items():
                data=eattr['weight']
                degree += data['weight']
            degrees.append((n, degree))
        degrees.sort(key=lambda degrees: degrees[1], reverse=True)
        return degrees[0:100]

def main():
	"""Solve the three problems in graph.py"""
	# Set up MultiGraph
	with open('./connection_tuples.pkl', 'rb') as infile:
		cxs = pickle.load(infile)
	# add a weight of one to every edge
	weighted = [i + (1,) for i in cxs]
	graph = nx.MultiGraph()
	graph.add_weighted_edges_from(weighted)
	# flatten into graph with edges weighted by no. of connections
	G = flatten_graph(graph)
	# answer the questions
	degree = solve_Degree(graph)
	with codecs.open('degree_answer.txt', 'w', 'utf-8') as outfile:
		print >> outfile, degree
	rank = solve_PageRank(G)
	with codecs.open('rank_answer.txt', 'w', 'utf-8') as outfile:
		print >> outfile, rank
	bff, friends = solve_BestFriends(G)
	with codecs.open('bff_answer.txt', 'w', 'utf-8') as outfile:	
		print >> outfile, bff 
        degree2 = solve_Degree2(friends)
        with codecs.open('degree2_answer.txt', 'w', 'utf-8') as outfile:
                print >> outfile, degree2
    
if __name__ == '__main__':
	main()


