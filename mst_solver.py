import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_step(G, mst_edges, current_edge=None, pos=None, title=""):
    """
    Helper function to draw the graph and the MST-in-progress.
    """
    if pos is None:
        pos = nx.spring_layout(G, seed=42) # Fix layout for consistent steps
    
    plt.figure(figsize=(10, 7))
    plt.title(title)
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    
    # Draw all edges in grey
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='grey', alpha=0.5)
    
    # Draw the MST edges in blue
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='blue', width=2)
    
    # Highlight the current edge being considered
    if current_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[current_edge], edge_color='red', width=3, style='dashed')
        
    # Draw labels
    nx.draw_networkx_labels(G, pos)
    
    # Draw edge weights (labels)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.show() # This will pause execution until the plot window is closed
    
def kruskals_mst_step_by_step(G):
    """
    Finds the MST of graph G using Kruskal's algorithm and shows each step.
    """
    print("--- Running Kruskal's Algorithm (Step by Step) ---")
    
    # Get a fixed layout for all drawing steps
    pos = nx.spring_layout(G, seed=42)
    
    # Draw the initial graph 
    draw_graph_step(G, [], pos=pos, title="Initial Connected Graph")
    
    mst = [] # List to store edges of the MST
    mst_weight = 0
    
    # A disjoint set (Union-Find) data structure to detect cycles
    # Initially, each node is its own component
    disjoint_sets = {node: {node} for node in G.nodes()}

    def find_set(node):
        for s in disjoint_sets.values():
            if node in s:
                return s
        return None

    def union_sets(set1, set2):
        new_set = set1.union(set2)
        # Remove old sets and add the new merged set
        keys_to_remove = []
        for key, s in disjoint_sets.items():
            if s == set1 or s == set2:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            disjoint_sets.pop(key, None)
        disjoint_sets[tuple(new_set)] = new_set # Use a hashable key

    # Sort all edges by weight in non-decreasing order
    sorted_edges = sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1))
    
    step_count = 1
    for u, v, data in sorted_edges:
        weight = data.get('weight', 1)
        
        # Check if adding this edge forms a cycle
        set_u = find_set(u)
        set_v = find_set(v)
        
        title = f"Step {step_count}: Consider edge ({u}, {v}) with weight {weight}"
        
        if set_u != set_v:
            # No cycle: Add this edge to the MST
            mst.append((u, v))
            mst_weight += weight
            union_sets(set_u, set_v)
            title += " - Added (No Cycle)"
        else:
            # Cycle: Reject this edge
            title += " - Rejected (Forms Cycle)"
            
        # Show the step
        draw_graph_step(G, mst, current_edge=(u,v), pos=pos, title=title)
        step_count += 1

    # Draw the final MST 
    print(f"--- MST Complete ---")
    print(f"Total Weight: {mst_weight}")
    print(f"Edges: {mst}")
    
    final_mst_graph = nx.Graph()
    final_mst_graph.add_edges_from(mst)
    for u,v in mst:
        final_mst_graph[u][v]['weight'] = G[u][v]['weight']
        
    draw_graph_step(final_mst_graph, final_mst_graph.edges(), pos=pos, title=f"Final MST (Total Weight: {mst_weight})")
    
    return final_mst_graph, mst_weight

def kruskals_mst_final(G, graph_name="Graph"):
    """
    Finds and depicts the final MST for a graph G without step-by-step.
    Used for testing on the 2 new graphs.
    """
    print(f"\n--- Finding MST for {graph_name} ---")
    pos = nx.spring_layout(G, seed=42)
    
    # Draw the original graph
    draw_graph_step(G, [], pos=pos, title=f"Original {graph_name}")

    # Run Kruskal's algorithm
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
    mst_weight = mst.size(weight='weight')
    
    print(f"Total Weight: {mst_weight}")
    print(f"Edges: {list(mst.edges())}")
    
    # Draw the final MST
    draw_graph_step(mst, mst.edges(), pos=pos, title=f"Final MST for {graph_name} (Weight: {mst_weight})")
    return mst

def main():
    # --- Graph 1: Main task ---
    # A connected graph with 7 nodes and 11 edges
    G1 = nx.Graph()
    G1.add_nodes_from(range(7))
    G1.add_edges_from([
        (0, 1, {'weight': 7}), (0, 3, {'weight': 5}),
        (1, 2, {'weight': 8}), (1, 3, {'weight': 9}), (1, 4, {'weight': 7}),
        (2, 4, {'weight': 5}),
        (3, 4, {'weight': 15}), (3, 5, {'weight': 6}),
        (4, 5, {'weight': 8}), (4, 6, {'weight': 9}),
        (5, 6, {'weight': 11})
    ])
    
    # Run the step-by-step function for the first graph
    kruskals_mst_step_by_step(G1)
    
    # --- Graph 2: Test case ---
    # 5 nodes, 8 edges
    G2 = nx.Graph()
    G2.add_edges_from([
        ('A', 'B', {'weight': 1}), ('A', 'C', {'weight': 4}),
        ('B', 'C', {'weight': 3}), ('B', 'D', {'weight': 2}),
        ('B', 'E', {'weight': 7}),
        ('C', 'D', {'weight': 5}),
        ('D', 'E', {'weight': 6}),
        ('E', 'A', {'weight': 8})
    ])
    kruskals_mst_final(G2, "Test Graph 2")

    # --- Graph 3: Test case ---
    # 6 nodes, 9 edges
    G3 = nx.Graph()
    G3.add_edges_from([
        (1, 2, {'weight': 3}), (1, 4, {'weight': 2}), (1, 5, {'weight': 5}),
        (2, 3, {'weight': 1}), (2, 4, {'weight': 6}),
        (3, 4, {'weight': 4}), (3, 6, {'weight': 7}),
        (4, 5, {'weight': 8}),
        (5, 6, {'weight': 9})
    ])
    kruskals_mst_final(G3, "Test Graph 3")

if __name__ == "__main__":
    main()
