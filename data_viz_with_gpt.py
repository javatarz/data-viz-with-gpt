import os
from argparse import Namespace, ArgumentParser

from load_to_db import load_files_as_tables
from query import run_query
from visualize import visualize


def parse_args() -> Namespace:
    parser = ArgumentParser(description='Visualise the data from the database using ChatGPT')

    parser.add_argument('--data-query', help='Question for the system to answer', required=True)
    parser.add_argument('--viz-query', help='Prompt on how to visualize the data', required=True)
    parser.add_argument('--data-dir', help='Directory to load CSVs from', default='data')
    parser.add_argument('--file-to-query', help='File to query', required=True)
    parser.add_argument('--api-key', help='ChatGPT API key', default=os.environ.get('CHATGPT_API_KEY'))

    return parser.parse_args()


def run() -> None:
    args = parse_args()
    load_files_as_tables(args.data_dir)
    df = run_query(args.data_query, args.file_to_query, args.api_key)
    visualize(df, args.viz_query, args.api_key)


if __name__ == '__main__':
    run()
