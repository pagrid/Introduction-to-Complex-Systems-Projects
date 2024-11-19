# -*- coding: utf-8 -*-
"""Real Networks.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kAH0ksRQ5b9tUg-HzzVhYYK4DlGwliUZ

**Import necessary libraries**
"""

# Import necessary libraries
!pip install powerlaw
!pip install requests
!pip install dask[dataframe]
!pip install pandas
!pip install --upgrade networkx
!pip install scipy

import pandas as pd
import numpy as np
import os
import gzip
import networkx as nx
import powerlaw
import matplotlib.pyplot as plt
import requests
from scipy import sparse
from scipy.stats import poisson, chisquare

""" **Download Data**  """

def download_data(url, local_path):
    """
    Download data from a URL and save it to a local file.
    """
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    with open(local_path, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded: {local_path}")
    return local_path

"""**Data Loading**"""

import dask.dataframe as dd # Import dask.dataframe as dd

def load_data(file_path, sep=',', from_col='from', to_col='to'):
    """Loads data from a file into a pandas DataFrame."""
    try:
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rt') as f:
                df = pd.read_csv(f, sep=sep)  # Use pd here
        else:
            df = pd.read_csv(file_path, sep=sep)  # Use pd here

        # ... (rest of the function to find and select columns) ...

    except pd.errors.EmptyDataError:  # Use pd here
        print(f"Warning: File '{file_path}' is empty or has an invalid format.")
        return pd.DataFrame(columns=[from_col, to_col])  # Return an empty DataFrame with the expected columns

def load_data_as_edgelist(file_path, sep='\t', from_col='FromNodeId', to_col='ToNodeId', comments='#'):
    """Loads data from a file into an edge list."""
    with gzip.open(file_path, 'rt') as f:  # Open in text mode for gzip files
        edge_list = []
        for line in f:
            if line.startswith(comments):
                continue  # Skip comment lines
            parts = line.strip().split(sep)
            try:  # Use column indices if names not found
                from_node = int(parts[0]) # Assume first column is 'from' node
                to_node = int(parts[1])  # Assume second column is 'to' node
                edge_list.append((from_node, to_node))
            except (IndexError, ValueError):
                pass  # Skip invalid lines

    return edge_list

"""**Adjacency Matrix Computation**"""

def compute_adjacency_matrix(graph):
    """Computes the adjacency matrix of the graph."""
    # Use nx.to_scipy_sparse_array if nx.to_scipy_sparse_matrix is not available
    # This function was renamed in NetworkX 2.6
    try:
        # Try using the newer function name first for compatibility with newer NetworkX versions
        adj_matrix = nx.to_scipy_sparse_array(graph, format='csr')
    except AttributeError:
        # If the newer function is not available, try the older function name for backwards compatibility
        adj_matrix = nx.to_scipy_sparse_matrix(graph, format='csr')
    except TypeError:  # Fallback to dense matrix if sparse conversion fails
        adj_matrix = nx.to_numpy_array(graph)

    return adj_matrix

"""**Plotting Degree Distribution**"""

def plot_degree_distribution(graph, log_scale=False, save_path=None):
    """Plots the degree distribution of a graph."""
    degrees = [deg for _, deg in graph.degree()]
    # Calculate degree frequencies
    degreesfreq = nx.degree_histogram(graph)
    # Create a DataFrame for plotting
    degreesfreqdf = pd.DataFrame({'degrees': range(len(degreesfreq)), 'frequency': degreesfreq})
    # Calculate total degree frequency
    totaldegreesfreq = sum(degreesfreq)

    ## probability mass distribution graph
    probability = degreesfreqdf['frequency'] / totaldegreesfreq
    plt.figure(figsize=(12, 8))
    plt.plot(degreesfreqdf['degrees'], probability, 'bx', color='blue')

    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Probability")

    # Save and show the normal scale plot
    if save_path and not log_scale:
        plt.savefig(save_path.replace('.png', '_normal.png'))
    plt.show()

    # If log_scale is True, generate the log-log plot
    if log_scale:
        plt.figure(figsize=(12, 8))
        plt.plot(degreesfreqdf['degrees'], probability, 'bx', color='red')
        plt.xscale('log')
        plt.yscale('log')
        plt.title("Degree Distribution (Log-Log Scale)")
        plt.xlabel("Degree")
        plt.ylabel("Probability")

        if save_path:
            plt.savefig(save_path)
        plt.show()

"""**Clustering Coefficients**"""

def compute_clustering_coefficients(graph):
    clustering_coefficients = {}
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        num_neighbors = len(neighbors)
        if num_neighbors < 2:  # Handle nodes with less than 2 neighbors
            clustering_coefficients[node] = 0  # or any other appropriate value like float('nan')
            continue

        num_triangles = 0
        for i in range(num_neighbors):
            for j in range(i + 1, num_neighbors):
                if graph.has_edge(neighbors[i], neighbors[j]):
                    num_triangles += 1

        # Calculate clustering coefficient, avoiding division by zero
        clustering_coefficient = (2 * num_triangles) / (num_neighbors * (num_neighbors - 1)) if num_neighbors > 1 else 0
        clustering_coefficients[node] = clustering_coefficient

    # Calculate average clustering coefficient, handle empty dictionary
    if clustering_coefficients:  # Check if the dictionary is not empty
        avg_clustering_coefficient = sum(clustering_coefficients.values()) / len(clustering_coefficients)
        print(f"Average clustering coefficient: {avg_clustering_coefficient}")
    else:
        print("Average clustering coefficient cannot be calculated: No nodes with sufficient neighbors.")

"""**Poisson goodness-of-fit test**"""

def goodness_of_fit_poisson(graph):
    """Fit the degree distribution to a Poisson distribution and perform goodness-of-fit."""
    degrees = [deg for _, deg in graph.degree()]

    # Calculate observed frequencies
    unique_degrees, observed_freq = np.unique(degrees, return_counts=True)

    # Calculate lambda for Poisson distribution (average degree)
    avg_degree = np.mean(degrees)

    # Calculate expected frequencies based on Poisson distribution
    # Use the observed degree range to generate expected frequencies
    expected_dist = poisson.pmf(unique_degrees, avg_degree) * len(degrees)

    # Ensure expected_dist sums to the same as observed_freq (within tolerance)
    expected_dist = expected_dist * np.sum(observed_freq) / np.sum(expected_dist)

    # Perform Chi-square test
    # Add a small constant (e.g., 1e-6) to frequencies to avoid division by zero
    observed_freq = observed_freq + 1e-6
    expected_dist = expected_dist + 1e-6

    chi2_stat, p_value = chisquare(observed_freq, expected_dist)

    print(f"Chi-square statistic: {chi2_stat}, p-value: {p_value}")
    return chi2_stat, p_value

"""**Power-law fit**"""

def goodness_of_fit_powerlaw(graph):
    """Fit the degree distribution to a power-law distribution and perform goodness-of-fit."""
    degrees = [deg for _, deg in graph.degree()]
    fit = powerlaw.Fit(degrees, discrete=True)
    ks_stat = fit.power_law.KS()
    print(f"Kolmogorov-Smirnov distance for power-law: {ks_stat}")

    # The plot_pdf method is used to plot the probability density function
    fig, ax = plt.subplots(figsize=(8, 6))  # Create a figure and an axes object with a specified size

    # Plot PDF for data and power-law fit
    fit.plot_pdf(color='r', linewidth=2, ax=ax)
    fit.power_law.plot_pdf(color='g', linestyle='--', ax=ax)

    # Customize the x-axis ticks (start from 10)
    start = 10
    end = int(np.log10(max(degrees))) + 1  # Compute the range of ticks
    ax.set_xticks([10**i for i in range(int(np.log10(start)), end)])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # Add labels
    plt.xlabel('Degree')
    plt.ylabel('Probability Density')

    # Display the plot
    plt.show()

    return ks_stat

"""**Main function**"""

# Main function
def main():
    # Define source URLs | Make sure the URLs are up to date
    amazon_url = "https://snap.stanford.edu/data/amazon0302.txt.gz"

    # Local file paths
    local_dir = "datasets"
    os.makedirs(local_dir, exist_ok=True)
    amazon_path = os.path.join(local_dir, "amazon.txt.gz")

    # Download dataset
    download_data(amazon_url, amazon_path)

    # Load data into Dask DataFrames
    amazon_df = load_data(amazon_path, from_col='FromNodeId', to_col='ToNodeId')

    # Create NetworkX graphs directly from edge lists
    amazon_graph = nx.DiGraph(load_data_as_edgelist(amazon_path, sep = '\t'))  # Changed to load_data_as_edgelist

    # Adjacency matrix
    amazon_adj = compute_adjacency_matrix(amazon_graph)
    avg_clustering = nx.average_clustering(amazon_graph)  # Example
    print(f"Average clustering coefficient (using nx.average_clustering): {avg_clustering}")

    # Degree distribution
    plot_degree_distribution(amazon_graph, log_scale=True, save_path='amazon_degree_log.png') # Fixed indentation

    # Goodness-of-fit tests
    goodness_of_fit_poisson(amazon_graph)
    goodness_of_fit_powerlaw(amazon_graph)

"""**Run**"""

# Entry point
if __name__ == "__main__":
    main()

