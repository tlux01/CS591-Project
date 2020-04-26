from DynamicCon import DynamicCon
import AVLDyCon as avl
import networkx as nx
from random import sample, seed
import random
from time import time
import copy
import numpy as np
import matplotlib.pyplot as plt

def mySample(s):
    return sample(s,1)[0]

def areConnected(G,node1,node2):
    """test if node1 and node2 are connected in G using bfs. Takes linear time in the number of nodes
    in the connected component of node1"""
    return node2 in nx.node_connected_component(G,node1)

def getRandomConnectedNodes(G):
    """return two random connected nodes"""
    node1 = mySample(G.nodes())
    node2 = mySample(nx.node_connected_component(G,node1))
    return node1, node2

def getRandomNotConnectedNodes(G):
    """return two random connected nodes"""
    node1 = mySample(G.nodes())
    nodes = set(G.nodes())
    CC = nx.node_connected_component(G,node1)
    possible_nodes = nodes - CC
    if len(possible_nodes) == 0:
        print("Error: G is connected!")
        return None
    node2 = mySample(list(nodes - CC))
    return node1, node2

def test1(n,p):
    """tests DC and BFS-based connectivity alg on a G(n,p)"""
    #seed(69)

    G = nx.gnp_random_graph(n,p)
    print("G has {} connected components".format(nx.number_connected_components(G)))
    DC = DynamicCon(G)
    N = 100
    allTrues1 = [False]*N
    allTrues2 = [False]*N
    for i in range(N):
        node1,node2 = getRandomConnectedNodes(G)
        allTrues1[i] = areConnected(G,node1,node2)
        allTrues2[i] = DC.connected(node1,node2)
    print("The BFS-based alg works correctly = " + str(False not in allTrues1))
    print("The DC-based alg works correctly = " + str(False not in allTrues2))

    allFalses1 = [True]*N
    allFalses2 = [True] * N
    for i in range(N):
        node1,node2 = getRandomNotConnectedNodes(G)
        allFalses1[i] = areConnected(G,node1,node2)
        allFalses2[i] = DC.connected(node1,node2)
        if allFalses2[i]:
            print("DC reports that {} and {} are connected!".format(node1, node2))
            print("Node1: {}, node2: {}. CC of node1: {}".format(node1, node2, nx.node_connected_component(G,node1)))

    print("The BFS-based alg works correctly = " + str(True not in allFalses1))
    print("The DC-based alg works correctly = " + str(True not in allFalses2))

def test2():
    """tests DC with adding edges on n nodes"""
    G = nx.Graph()
    for i in range(5):
        G.add_node(i)
    DC = DynamicCon(G)
    DC.ins(0,1)
    DC.ins(0,1)
    DC.ins(1,2)
    DC.ins(0,4)
    print("edge are: {}".format(G.edges))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0,1)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0, 2)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(1, 4)))
    print("DC works correctly wrt insertion = {}".format(not DC.connected(1, 3)))

    print("Deleting edge (0,1)...")
    DC.del_edge((0,1))
    DC.del_edge((0, 1))
    print("edge are: {}".format(G.edges))
    print("DC works correctly wrt deletion = {}".format(DC.connected(1,2)))
    print("DC works correctly wrt deletion = {}".format(DC.connected(0,4)))
    print("DC works correctly wrt deletion = {}".format(not DC.connected(0,1)))
    print("DC works correctly wrt deletion = {}".format(not DC.connected(1,4)))


    print("Inserting edge (0,1)...")
    DC.ins(0, 1)
    DC.ins(0, 1)
    print("edge are: {}".format(G.edges))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0, 1)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(1,2)))
    print("DC works correctly wrt insertion = {}".format(DC.connected(0, 2)))
    print("DC works correctly wrt insertion = {}".format(not DC.connected(1, 3)))

def test3():
    G = nx.Graph()
    for i in range(3):
        G.add_node(i)
    DC = DynamicCon(G)
    DC.ins(0, 1)
    DC.ins(0, 1)
    DC.ins(1, 2)
    DC.del_edge((0,1))
    DC.del_edge((0, 1))
    DC.ins(0, 1)
    DC.ins(0, 1)
    print("edges: {}".format(G.edges))
    u = 1
    v = 2
    g_nodes = DC.G.nodes
    print("In-order of the tree containing {}: {}".format(u, g_nodes[u]["data"].active_occ[DC.max_level].find_root().in_order()))
    print("In-order of the tree containing {}: {}".format(v, g_nodes[v]["data"].active_occ[DC.max_level].find_root().in_order()))

def test4():
    seed(400)
    n = 100
    p = 2/n
    num_tests = 10000
    G = nx.gnp_random_graph(n, p)
    DC = DynamicCon(G)
    DC_correct = [False]*num_tests
    for i in range(num_tests):
        r = random.random()
        if r < 0.5:
            # add random edge
            node1 = mySample(G.nodes)
            node2 = mySample(G.nodes - {node1})
            print("{} | Want to insert: {}".format(i,(node1,node2)))
            DC.ins(node1,node2)
        else:
            # remove random edge
            node1, node2 = mySample(G.edges)
            print("{} | Want to delete: {}".format(i,(node1,node2)))
            DC.del_edge((node1,node2))
        node1,node2 = getRandomConnectedNodes(G)
        node3, node4 = getRandomNotConnectedNodes(G)

        DC_correct[i] = DC.connected(node1,node2) and not DC.connected(node3,node4)
        if not DC_correct[i]:
            print("{} and {} connected: {}".format(node1, node2, DC.connected(node1,node2)))
            print("{} and {} not connected: {}".format(node3, node4, DC.connected(node3,node4)))
    print("DC works correctly = {}".format(False not in DC_correct))

def test5():
    seed(10)
    n = 10
    p = .06
    num_tests = 100
    G = nx.gnp_random_graph(n, p)
    DC = DynamicCon(G)
    DC_correct = [False]*num_tests
    for i in range(num_tests):
        r = random.random()
        if r < 0.5:
            # add random edge
            node1 = mySample(G.nodes)
            node2 = mySample(G.nodes - {node1})
            print("{} | Want to insert: {}".format(i,(node1,node2)))
            DC.ins(node1,node2)
        else:
            # remove random edge


            node1, node2 = mySample(G.edges)
            print("{} | Want to delete: {}".format(i,(node1,node2)))
            DC.del_edge((node1,node2))
        node1,node2 = getRandomConnectedNodes(G)
        node3, node4 = getRandomNotConnectedNodes(G)

        DC_correct[i] = DC.connected(node1,node2) and not DC.connected(node3,node4)
        if not DC_correct[i]:
            print("{} and {} connected: {}".format(node1, node2, DC.connected(node1,node2)))
            print("{} and {} not connected: {}".format(node3, node4, DC.connected(node3,node4)))
    print("DC works correctly = {}".format(False not in DC_correct))

def test6():
    G = nx.Graph()
    for i in range(4):
        G.add_node(i)
    G.add_edge(0,1)
    G.add_edge(1,2)




    DC = DynamicCon(G)

    DC.ins(0,2)

    DC.ins(0,3)

def benchmark1():
    n = 10000
    p = 2 / n
    num_iterations = 100
    query_frequency = 10
    print("Running benchmark 1")
    print("number of nodes: {}\n"
          "number of edge additions and deletions: {}\n"
          "query frequency: {}\n".format(n, num_iterations, query_frequency))
    total_time_DC = 0
    total_time_BFS = 0
    G = nx.gnp_random_graph(n, p)
    H = copy.deepcopy(G) # keep H to be the same as G
    precompute_start = time()
    DC = DynamicCon(G)
    precompute_end = time()
    precompute_time = precompute_end - precompute_start
    for i in range(num_iterations):

        node1, node2 = sample(G.nodes,2)
        node3, node4 = mySample(G.edges)
        node5, node6 = sample(G.nodes, 2)
        # only query once in query_frequency
        if (i % query_frequency == 0):
            start = time()
            DC.ins(node1, node2)
            DC.del_edge((node3, node4))
            c1 = DC.connected(node5, node6)
            end = time()
            total_time_DC += end - start

            start = time()
            H.add_edge(node1, node2)
            H.remove_edge(node3, node4)
            c2 = areConnected(H, node5, node6)
            end = time()
            total_time_BFS += end - start
        else:
            start = time()
            DC.ins(node1, node2)
            DC.del_edge((node3, node4))
            end = time()
            total_time_DC += end - start

            start = time()
            H.add_edge(node1, node2)
            H.remove_edge(node3, node4)
            end = time()
            total_time_BFS += end - start

        if (c1 != c2):
            print("ERROR! THE TWO METHODS DO NOT AGREE!")
    return precompute_time, total_time_DC, total_time_BFS

def benchmark2(doPrinting = False):
    n = 10000
    p = 2 / n
    num_iterations = 100
    query_frequency = 5
    if doPrinting:
        print("Running benchmark 2")
        print("number of nodes: {}\n"
              "number of edge additions and deletions: {}\n"
              "query frequency: {}\n".format(n, num_iterations, query_frequency))
    total_time_DC = 0
    total_time_BFS = 0
    G = nx.gnp_random_graph(n, p)
    H = copy.deepcopy(G) # keep H to be the same as G
    precompute_start = time()
    DC = DynamicCon(G)
    precompute_end = time()
    precompute_time = precompute_end - precompute_start

    for i in range(num_iterations):
        node1, node2 = sample(G.nodes, 2)
        node3, node4 = mySample(G.edges)

        # DC:
        start = time()
        DC.ins(node1, node2)
        DC.del_edge((node3, node4))
        for j in range(query_frequency):
            node5, node6 = sample(G.nodes, 2)
            c1 = DC.connected(node5, node6)
        end = time()
        total_time_DC += end - start

        # BFS:
        start = time()
        H.add_edge(node1, node2)
        H.remove_edge(node3, node4)
        for j in range(query_frequency):
            node5, node6 = sample(G.nodes, 2)
            c2 = areConnected(H, node5, node6)
        end = time()
        total_time_BFS += end - start

    return precompute_time, total_time_DC, total_time_BFS

def benchmark3(use_custom_max_level = True, n = 10**3, query_frequency = 5, max_level = 0, doPrinting = True, withBFS = False):
    # n = number of nodes
    # query_frequency = number of queries per edge addition, deletion
    # max_level = max_level for the DC data structure
    p = 2 / n
    num_iterations = 100
    if doPrinting:
        print("Running benchmark 3")
        print("number of nodes: {}\n"
              "query frequency: {}\n".format(n, query_frequency))
    total_time_DC = 0
    total_time_BFS = 0
    G = nx.gnp_random_graph(n, p)
    print("G has {} CC's".format(nx.number_connected_components(G)))
    precompute_start = time()
    DC = DynamicCon(G, use_custom_max_level, max_level)
    precompute_end = time()
    precompute_time = precompute_end - precompute_start

    for i in range(num_iterations):
        node1, node2 = sample(G.nodes, 2)
        node3, node4 = mySample(G.edges)

        # DC:
        start = time()
        DC.ins(node1, node2)
        DC.del_edge((node3, node4))
        for j in range(query_frequency):
            node5, node6 = sample(G.nodes, 2)
            DC.connected(node5, node6)
        end = time()
        total_time_DC += end - start

        #BFS
        if withBFS:
            start = time()
            for j in range(query_frequency):
                node5, node6 = sample(G.nodes, 2)
                areConnected(G, node5, node6)
            end = time()
            total_time_BFS += end - start
    return precompute_time, total_time_DC, total_time_BFS

def benchmark_and_save_old():
    # tDC = O(log(n) + query_freq + ?(max_level))
    # tBFS = O(n + query freq)
    low_deg = 5
    high_deg = 15
    use_custom_max_level = True
    withBFS = False
    print("Running test until {} nodes".format(2**(high_deg-1)))
    ns = [2 ** k for k in range(low_deg, high_deg)]
    tDC_times = []
    precompute_times = []
    tBFS_times = []
    for i in range(len(ns)):
        print("Benchmarking with {} nodes".format(ns[i]))
        precompute, tDC, tBFS = benchmark3(use_custom_max_level= use_custom_max_level, n=ns[i], max_level=0, withBFS=withBFS, doPrinting=False)
        tDC_times.append(tDC)
        precompute_times.append(precompute)
        tBFS_times.append(tBFS)

        if (ns[i] >= 2**12):
            marker = "D"
            plt.figure(1) # for ordinary axis
            ns_so_far = ns[:i+1]
            #plt.plot(ns_so_far, precompute_times, label = "precompute", marker = marker)
            plt.plot(ns_so_far, tDC_times, label="DC time", marker = marker)
            if withBFS:
                plt.plot(ns_so_far, tBFS_times, label="BFS time", marker = marker)
            plt.legend()
            plt.xlabel("number of nodes (n)")
            plt.ylabel("time in seconds")
            plt.title("G(n,2/n), 100 edge insertions/deletions, 500 queries, n from {} to {}".format(ns[0], ns_so_far[-1]))
            plt.savefig("data/plots/tDC_times_nodes_from_{}_to_{}_max_level_{}.png".format(ns[0],ns_so_far[-1], 0))
            plt.clf()

            plt.figure(2)  # for log axis
            #plt.plot(ns_so_far, precompute_times, label="precompute", marker=marker)
            plt.plot(ns_so_far, tDC_times, label="DC time", marker=marker)
            if withBFS:
                plt.plot(ns_so_far, tBFS_times, label="BFS time", marker=marker)
            plt.xscale("log")
            #plt.yscale("log")
            plt.legend()
            plt.xlabel("number of nodes (n)")
            plt.ylabel("time in seconds")
            plt.title("Log scale. G(n,2/n), 100 ins/del, 500 queries, n from {} to {}".format(ns[0], ns_so_far[-1]))
            plt.savefig("data/plots/log_scale_tDC_times_nodes_from_{}_to_{}_max_level_{}.png".format(ns[0], ns_so_far[-1], 0))
            plt.clf()

            np.save('data/benchmark_data/precompute_times_from_{}_to_{}_nodes_5_query_freq'.format(ns[0], ns_so_far[-1]),
                    np.array(precompute_times))
            np.save('data/benchmark_data/tDC_from_{}_to_{}_nodes_5_query_freq'.format(ns[0], ns_so_far[-1]),
                    np.array(tDC_times))
            np.save('data/benchmark_data/tBFS_from_{}_to_{}_nodes_5_query_freq'.format(ns[0], ns_so_far[-1]),
                    np.array(tBFS_times))


def benchmark_DC_connected_method_k_times(k, DC):
    start = time()
    for i in range(k):
        node1, node2 = sample(DC.G.nodes, 2)
        DC.connected(node1, node2)
    end = time()
    return end - start

def benchmark_DC_ins_method_k_times(k,DC):
    res = 0
    for i in range(k):
        node1, node2 = sample(DC.G.nodes, 2)
        start = time()
        DC.ins(node1, node2)
        end = time()
        res += end - start
    return res

def benchmark_DC_del_method_k_times(k,DC):
    res = 0
    for i in range(k):
        node3, node4 = mySample(DC.G.edges)
        start = time()
        DC.del_edge((node3, node4))
        end = time()
        res += end - start
    return res

def benchmark_BFS_connected_method_k_times(k, G):
    start = time()
    for i in range(k):
        node1, node2 = sample(G.nodes, 2)
        areConnected(G,node1, node2)
    end = time()
    return end - start

def delete_random_edge(DC):
    node3, node4 = mySample(DC.G.edges)
    DC.del_edge((node3, node4))

def benchmark_on_dataset(deletion_freq = 100, query_freq = 5):
    f = open("data/dataset.txt","r")
    lines = f.readlines()
    f.close()

    nodes = []
    edges = []
    for line in lines:
        sp = line.split(" ")
        sp[-1] = sp[-1][:-1]
        ev = [eval(k) for k in sp]
        node1, node2, t = ev
        edges.append((node1, node2))
        nodes.append(node1)
        nodes.append(node2)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    print("There are {} nodes".format(len(G.nodes)))
    DC = DynamicCon(G, True, 0)

    ins_time_DC = 0
    del_time_DC = 0
    query_time_DC = 0
    query_time_BFS = 0
    num_iterations = 10**5
    for i in range(num_iterations):
        if i%10**4 == 0:
            print("i = {}".format(i))
        start = time()
        DC.ins(edges[i][0],edges[i][1])
        ins_time_DC += time() - start
        if i%deletion_freq == 0:
            start = time()
            delete_random_edge(DC)
            del_time_DC += time() - start
        start = time()
        benchmark_DC_connected_method_k_times(query_freq, DC)
        query_time_DC += time() - start

        query_time_BFS += benchmark_BFS_connected_method_k_times(query_freq, G)

    return ins_time_DC/(num_iterations), del_time_DC/(num_iterations/deletion_freq), query_time_DC/(num_iterations*query_freq), query_time_BFS/(num_iterations*query_freq)


def benchmark_and_save_on_dataset_old():
    use_custom_max_level = True
    withBFS = True
    tDC_times = []
    tBFS_times = []
    query_freqs = range(1,10)
    for i in range(len(query_freqs)):
        print("Benchmarking with {} query frequency".format(query_freqs[i]))
        tDC, tBFS = benchmark_on_dataset(query_freq = query_freqs[i])
        tDC_times.append(tDC)
        tBFS_times.append(tBFS)

        marker = "D"
        plt.figure(1)  # for ordinary axis
        query_freqs_so_far = query_freqs[:i+1]
        plt.plot(query_freqs_so_far, tDC_times, label="DC time", marker=marker)
        if withBFS:
            plt.plot(query_freqs_so_far, tBFS_times, label="BFS time", marker=marker)
        plt.legend()
        plt.xlabel("query frequency")
        plt.ylabel("time in seconds")
        plt.title("Dataset, 986 nodes, 100,000 edge ins, query freq from {} to {}".format(query_freqs_so_far[0], query_freqs_so_far[-1]))
        plt.savefig("data/plots/times_email_dataset_query_freq_from_{}_to_{}.png".format(query_freqs_so_far[0], query_freqs_so_far[-1]))
        plt.clf()


def benchmark_on_graph(G, use_custom_max_level, max_level, withBFS, use_AVL):
    # benchmark on graph G
    # return average time for insertion, deletion, query, BFS query, and precompute time
    num_iterations = 50
    ins_time_DC = 0
    del_time_DC = 0
    query_time_DC = 0
    query_time_BFS = 0
    precompute_time = 0
    # print("G has {} CC's".format(nx.number_connected_components(G)))
    precompute_start = time()
    DC = DynamicCon(nx.empty_graph()) # for scope
    if use_AVL:
        DC = avl.DynamicCon(G, use_custom_max_level, max_level)
    else:
        DC = DynamicCon(G, use_custom_max_level, max_level)
    precompute_end = time()
    precompute_time += precompute_end - precompute_start
    num_ins = 10
    num_q = 10
    for i in range(num_iterations):
        # DC:
        ins_time_DC += benchmark_DC_ins_method_k_times(num_ins,DC)
        del_time_DC += benchmark_DC_del_method_k_times(1, DC)
        query_time_DC += benchmark_DC_connected_method_k_times(num_q,DC)

        # BFS
        if withBFS:
            query_time_BFS += benchmark_BFS_connected_method_k_times(1,G)
    return ins_time_DC/(num_iterations*num_ins), del_time_DC/num_iterations, query_time_DC/(num_iterations*num_q), query_time_BFS/num_iterations, precompute_time

def benchmark4(use_custom_max_level, n, max_level, withBFS, use_AVL):
    # graph creation:
    #G = nx.disjoint_union(nx.complete_graph(int(n/2)), nx.complete_graph(int(n/2)))
    G = nx.gnp_random_graph(n,2/n)
    return benchmark_on_graph(G, use_custom_max_level, max_level, withBFS, use_AVL)

def benchmark_and_save():
    # tDC = O(log(n) + query_freq + ?(max_level))
    # tBFS = O(n + query freq)
    low_deg = 6
    high_deg = 15
    use_custom_max_level = True
    max_level = 0
    withBFS = True
    #name_of_graph = "Kn_Kn_disjoint"
    name_of_graph = "G_np"

    print("Running test until {} nodes".format(2**(high_deg-1)))
    ns = [2 ** k for k in range(low_deg, high_deg)]
    rnb_times = [[] for k in range(4)]
    avl_times = [[] for k in range(4)]
    for i in range(len(ns)):
        print("Benchmarking with {} nodes".format(ns[i]))
        rnb_temp = benchmark4(use_custom_max_level, ns[i], max_level, withBFS,False)
        avl_temp = benchmark4(use_custom_max_level, ns[i], max_level, withBFS, True)
        for k in range(4):
            rnb_times[k].append(rnb_temp[k])
            avl_times[k].append(avl_temp[k])

        # for plotting
        if use_custom_max_level:
            ml = str(max_level)
        else:
            ml = "6logn"
        labels = ["insertion", "deletion", "query DC", "query BFS"]
        if (ns[i] >= 2**13):
            ns_so_far = ns[:i + 1]
            for j in range(2):
                marker = "D"
                plt.figure(j) # for ordinary axis
                for k in range(4):
                    plt.plot(ns_so_far, rnb_times[k], label="rnb "+labels[k], marker=marker)
                    if k != 3:
                        plt.plot(ns_so_far, avl_times[k], label="avl " + labels[k], marker=marker)
                if j == 1:
                    plt.xscale("log")
                plt.legend()
                plt.xlabel("number of nodes (n)")
                plt.ylabel("average time in seconds")
                if j == 0:
                    plt.title("{}, time, n from {} to {}".format(name_of_graph,ns[0], ns_so_far[-1]))
                    plt.savefig("data/plots/{}_tDC_average_times_nodes_from_{}_to_{}_max_level_{}.png".format(name_of_graph,ns[0],ns_so_far[-1], ml))
                else:
                    plt.title("Log scale, {}, average time, n from {} to {}".format(name_of_graph,ns[0], ns_so_far[-1]))
                    plt.savefig(
                        "data/plots/{}_log_scale_tDC_average_times_nodes_from_{}_to_{}_max_level_{}.png".format(name_of_graph,ns[0], ns_so_far[-1], ml))
                plt.clf()

            for k in range(4):
                np.save('data/benchmark_data/rnb_{}_average_{}_time_from_{}_to_{}_nodes_max_level_{}'.format(
                    name_of_graph,labels[k],ns[0], ns_so_far[-1], ml), np.array(rnb_times[k]))
                np.save('data/benchmark_data/avl_{}_average_{}_time_from_{}_to_{}_nodes_max_level_{}'.format(
                    name_of_graph, labels[k], ns[0], ns_so_far[-1], ml), np.array(avl_times[k]))



if __name__ == "__main__":
    real_dataset = False

    start = time()
    if real_dataset:
        ins_time_DC, del_time_DC, query_time_DC, query_time_BFS = benchmark_on_dataset()
    else:
        benchmark_and_save()
    end = time()
    print("The test took {} seconds".format(end - start))
    print("Done")
