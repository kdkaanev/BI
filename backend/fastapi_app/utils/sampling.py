def sample_even(df, n=50):
    """Sample up to n rows evenly from the DataFrame."""
    if len(df) <= n:
        return df.to_dict(orient="records")
    
    idxs = [
        int(i * (len(df) - n) / (n - 1))
        for i in range(n)
    ]
    return df.iloc[idxs].to_dict(orient="records")


