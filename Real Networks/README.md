# Real Networks Analysis

This project explores network analysis concepts using Python. It specifically focuses on analyzing real-world networks such as Amazon co-purchasing graphs. 

Key functionalities include:

* Downloading real-world datasets from the web.
* Constructing and visualizing graph structures.
* Computing clustering coefficients and degree distributions.
* Performing statistical fits (Poisson and power-law) for graph properties.

## Key Features

* Data Handling:
  * Automatic downloading of datasets from online sources.
  * Supports compressed .gz file formats for efficient storage and handling.
  * Flexible data loaders for edge lists and adjacency matrices.
  
* Network Analysis:
    * Constructs directed and undirected graphs using NetworkX.
    * Computes adjacency matrices and clustering coefficients.
      
* Statistical Analysis:
  * Goodness-of-fit tests for degree distributions using:
  * Poisson distribution.
  * Power-law distribution.
  * Visualization of probability density functions.

* Visualization:
  * Degree distributions plotted on normal and log-log scales.
  * Comparison of observed and theoretical distributions.

## Example Outputs
* Degree Distribution:

  * A normal-scale and log-log scale plot of node degrees.
  * Saved to outputs/amazon_degree_log.png.
     
* Statistical Fits:
  * Chi-square and Kolmogorov-Smirnov statistics printed for evaluation.

## Acknowledgements

This project was originally developed as part of the course Introduction to Complex Systems at Utrecht University.
