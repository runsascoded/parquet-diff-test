#!/usr/bin/env python
import click
import json
import os
from os import path
from subprocess import check_output, PIPE, Popen

import pandas as pd
from pyarrow.parquet import ParquetFile


COMPRESSORS = ['snappy', 'gzip', 'brotli', 'lz4', 'zstd']
ENGINES = ['pyarrow', 'fastparquet']


def run(df, compression, engine):
    out_dir = f'out/{engine}/{compression}'
    os.makedirs(out_dir, exist_ok=True)
    parquet_path = path.join(out_dir, 'empty.parquet')
    json_path = path.join(out_dir, 'metadata.json')
    xxd_path = path.join(out_dir, 'xxd.txt')

    df.to_parquet(parquet_path, compression=compression, engine=engine)

    # Compute sha256sum
    sha256sum = check_output(['sha256sum', parquet_path]).decode('utf-8').split()[0]

    # Load metadata via pyarrow
    parquet_file = ParquetFile(parquet_path)
    metadata = parquet_file.metadata
    metadata_dict = metadata.to_dict()

    # Get Parquet file disk size
    size = os.stat(parquet_path).st_size

    output = {
        'metadata': metadata_dict,
        'sha256sum': sha256sum,
        'size': size,
    }
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)

    proc = Popen(['xxd', parquet_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()
    with open(xxd_path, 'w') as f:
        f.write(stdout.decode('utf-8'))


@click.command('parquet-diff-test')
def main():
    df = pd.DataFrame([{ 'a': 111 }])
    empty_df = df.iloc[:0]
    for compression in COMPRESSORS:
        for engine in ENGINES:
            run(empty_df, compression, engine)


if __name__ == '__main__':
    main()
