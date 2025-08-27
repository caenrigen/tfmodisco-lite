# cluster.py
# Authors: Jacob Schreiber <jmschreiber91@gmail.com>
# adapted from code written by Avanti Shrikumar 

import leidenalg
import numpy as np
import igraph as ig
from tqdm import tqdm
import logging


def LeidenCluster(affinity_mat, n_seeds=2, n_leiden_iterations=-1, verbose=False):
    n_vertices = affinity_mat.shape[0]
    n_cols = affinity_mat.indptr
    sources = np.concatenate([np.ones(n_cols[i+1] - n_cols[i], dtype='int32') * i for i in range(n_vertices)])

    g = ig.Graph(directed=None) 
    g.add_vertices(n_vertices)
    g.add_edges(zip(sources, affinity_mat.indices))

    best_clustering = None
    best_quality = None

    logger = logging.getLogger("modisco-lite")

    for seed in tqdm(range(1, n_seeds+1), desc="Leiden clustering:"):
        partition = leidenalg.find_partition(
            graph=g,
            partition_type=leidenalg.ModularityVertexPartition,
            weights=affinity_mat.data,
            n_iterations=n_leiden_iterations,
            initial_membership=None,
            seed=seed*100) 

        quality = np.array(partition.quality())
        membership = np.array(partition.membership)
        
        if verbose:
            logger.info(f"Leiden clustering quality for seed {seed}: {quality}")

        if best_quality is None or quality > best_quality:
            best_quality = quality
            best_clustering = membership

    return best_clustering
