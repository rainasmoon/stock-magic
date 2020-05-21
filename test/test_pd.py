import pandas as pd
import numpy as np

def test_feather():
    afile = 'test_a_file'
    sz =1000000
    df = pd.DataFrame({'A': np.random.randn(sz), 'B': [1] * sz})
    df.to_hdf(afile, 'test')
    df = pd.read_hdf(afile, 'test')
    print(df)
    store = pd.HDFStore(afile)
    store['test1'] = df
    store.close()
    df = pd.read_hdf(afile, 'test1')
    print(df)
    store = pd.HDFStore(afile)
    print('test' in store)
    print('test2' in store)

test_feather()
