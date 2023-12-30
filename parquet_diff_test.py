#!/usr/bin/env python
import json
import os
from subprocess import check_output

import pandas as pd
from pyarrow.parquet import ParquetFile

df = pd.DataFrame([{ 'a': 111 }])
empty_df = df.iloc[:0]
path = 'test.parquet'
empty_df.to_parquet(path)

sha256sum = check_output(['sha256sum', 'test.parquet']).decode('utf-8').split()[0]

parquet_file = ParquetFile(path)
metadata = parquet_file.metadata
metadata_dict = metadata.to_dict()

size = os.stat(path).st_size

output = {
    'metadata': metadata_dict,
    'sha256sum': sha256sum,
    'size': size,
}
print(json.dumps(output, indent=2))
