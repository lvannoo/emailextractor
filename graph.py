import networkx as nx
import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
import mpld3
from flask import Flask


def construct_graph_from_data(nested_dict):
    G = nx.Graph()
    for collection_id, collection in nested_dict.items():
        for document_id, df in collection.items():
            for i, row in df.iterrows():
                # Add a node for the person
                person_node = f"{row['first_name']}_{row['last_name']}"
                G.add_node(person_node, node_type='person', 
                           first_name=row['first_name'], 
                           last_name=row['last_name'],
                           color='red')
                
                # Add nodes for the email addresses
                if row['my_emails'] == '' or pd.isna(row['my_emails']):
                    continue
                else:
                    emails = row['my_emails'].split(',')
                    for email in emails:
                        email_node = f"{email.strip()}"
                        G.add_node(email_node, 
                                   node_type='email', 
                                   email=email.strip(),
                                   color='blue')
                        G.add_edge(person_node, email_node, color='blue')
                
                # Add node for the phone number (if it exists)
                if 'phone_number' in df.columns and not pd.isna(row['phone_number']):
                    phone_node = f"{row['phone_number']}"
                    G.add_node(phone_node,
                              node_type='phone',
                              phone=row['phone_number'],
                              color='green')
                    G.add_edge(person_node, phone_node, color='green')
                
    return G


def render_graph(G):
    pos = nx.spring_layout(G, seed=42)
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    node_sizes = [250 if G.nodes[node]['node_type'] == 'person' else 100 for node in G.nodes()]
    edge_colors = [G.nodes[node]['color'] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(G, pos, font_size=6, font_family="Arial")
    plt.axis("off")
    plt.show()

def render_graph_size(G, figsize=(10, 8)):
    pos = nx.spring_layout(G, seed=42)
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    node_sizes = [250 if G.nodes[node]['node_type'] == 'person' else 100 for node in G.nodes()]
    edge_colors = [G.nodes[node]['color'] for node in G.nodes()]
    fig, ax = plt.subplots(figsize=figsize)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(G, pos, font_size=6, font_family="Arial")
    ax.set_axis_off()
    plt.show()

