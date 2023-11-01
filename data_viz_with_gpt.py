import os
from argparse import Namespace, ArgumentParser

from gpt_data_viz.load_to_db import load_files_as_tables
from gpt_data_viz.query import run_query
from gpt_data_viz.timers import timer
from gpt_data_viz.visualize import visualize


def parse_args() -> Namespace:
    parser = ArgumentParser(description='Visualise the data from the database using ChatGPT')

    parser.add_argument('--data-query', help='Question for the system to answer', required=True)
    parser.add_argument('--viz-query', help='Prompt on how to visualize the data', default="")
    parser.add_argument('--data-dir', help='Directory to load CSVs from', default='data')
    parser.add_argument('--api-key', help='ChatGPT API key', default=os.environ.get('CHATGPT_API_KEY'))

    return parser.parse_args()


@timer
def run() -> None:
    args = parse_args()
    load_files_as_tables(args.data_dir)
    df = run_query(args.data_query, args.api_key)
    print(df)
    visualize(df, args.viz_query, args.api_key)


if __name__ == '__main__':
    run()
