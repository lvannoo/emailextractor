import multiprocessing as mp
import pandas as pd
import re
from tqdm import tqdm
from typing import Dict, Any, List, Tuple, Callable
from utils import timer

@timer
def process_dataframes_multi(df_dict: Dict[str, Dict[str, pd.DataFrame]],
                       process_func: Callable[[pd.DataFrame, Dict[str, Any]], Any],
                       batch_size: int = 100,
                       **kwargs: Any) -> Dict[str, Dict[str, Any]]:
    # get a list of all the dataframes in the dictionary
    all_dfs = [df for coll in df_dict.values() for df in coll.values()]

    # calculate the number of batches based on the batch size
    n_batches = len(all_dfs) // batch_size + (1 if len(all_dfs) % batch_size > 0 else 0)

    # create a list of batch indices
    batch_indices = [range(i * batch_size, min((i + 1) * batch_size, len(all_dfs))) for i in range(n_batches)]

    # create a pool of worker processes
    pool = mp.Pool(mp.cpu_count() - 1)

    # iterate over the batches and apply the function to each batch
    results = []
    values = tuple(kwargs.values())
    with tqdm(total=len(all_dfs)) as pbar:
        for i, indices in enumerate(batch_indices):
            batch = [all_dfs[j] for j in indices]
            res = pool.starmap(process_func, [(df,) + values for df in batch])
            results.extend(res)

            pbar.update(len(batch))

    # close the worker pool
    pool.close()
    pool.join()

    new_dict = {}
    for coll_id, coll in df_dict.items():
        new_dict[coll_id] = {}
        for doc_id, df in coll.items():
            processed_df = results.pop(0)
            if processed_df.empty:
                continue  # skip this document if the processed DataFrame is empty
            new_dict[coll_id][doc_id] = processed_df

        # remove the collection if it has no remaining documents
        if not new_dict[coll_id]:
            del new_dict[coll_id]

    return new_dict

@timer
def process_dataframes_single(nested_dict, process_func, **kwargs):
    """
    Applies a function to every Pandas DataFrame in a nested dictionary in-place.

    Parameters:
    nested_dict (dict): A nested dictionary with the following structure:
                        {collection_id: {document_id: pd.DataFrame}}
    process_func (callable): A function to be applied to every DataFrame in the nested dictionary.
    **kwargs: Additional keyword arguments to be passed to the process_func.

    Returns:
    None
    """

    pd.options.mode.chained_assignment = None  # default='warn'
    
    new_dict = {}
    for coll_id, collection_dict in tqdm(nested_dict.items()):
        new_dict[coll_id] = {}
        for doc_id, df in list(collection_dict.items()):
            if isinstance(df, pd.DataFrame):
                if df.empty:
                    continue
                else:
                    new_dict[coll_id][doc_id] = process_func(df, **kwargs)
            else:
                new_dict[coll_id][doc_id] = df
        if new_dict[coll_id] == {}:
            del new_dict[coll_id]
    
    return new_dict