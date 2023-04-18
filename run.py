from data_generator import generate_nested_dict
from processor import process_dataframes_single
from analysers import extract_identifiers, process_offset_dataframe, remove_blank_dfs
from graph import construct_graph_from_data
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
from flask import Flask, jsonify

app = Flask(__name__)

dfs_multi = generate_nested_dict(10)
dfs_multi = process_dataframes_single(dfs_multi, remove_blank_dfs)
dfs_multi = process_dataframes_single(dfs_multi, process_offset_dataframe)
dfs_multi = process_dataframes_single(dfs_multi, extract_identifiers, identifier_type='email')

graph1 = construct_graph_from_data(dfs_multi)

@app.route('/graph')
def get_graph():
    nodes = [{'id': n, 'type': graph1.nodes[n]['node_type'], **graph1.nodes[n]} for n in graph1.nodes()]
    edges = [{'source': u, 'target': v, **graph1[u][v]} for u, v in graph1.edges()]
    return jsonify({'nodes': nodes, 'links': edges})

if __name__ == '__main__':
    app.run(host='localhost', port=5555)