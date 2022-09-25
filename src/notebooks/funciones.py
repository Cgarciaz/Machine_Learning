def to_1D(series):
 return pd.Series([x for _list in series for x in _list])