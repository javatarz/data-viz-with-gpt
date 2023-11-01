from dataclasses import dataclass
from itertools import chain
from typing import List

import duckdb
import openai
from openai.openai_object import OpenAIObject
from pandas import DataFrame

from gpt_data_viz.timers import timer


@dataclass
class Message:
    system: str
    user: str
    all_column_names: List[str]


@dataclass
class Response:
    request_message: Message
    open_ai_response: OpenAIObject
    sql: str


def _create_sql_message(query: str) -> Message:
    table_names = duckdb.sql("SHOW TABLES;").df()["name"].to_list()
    all_column_names = list(chain(
        *[_column_attributes_for_table(table_name)["column_name"].to_list() for table_name in table_names]
    ))
    create_table_commands = [
        _create_table_command(table_name, _column_names(_column_attributes_for_table(table_name)))
        for table_name in table_names
    ]
    all_create_table_commands = "\n".join(create_table_commands)

    system = f"""Given the following SQL tables, your job is to write queries given a user’s request.
    
    {all_create_table_commands}
    """
    user = f"Write a SQL query that returns - {query}"

    return Message(system=system, user=user, all_column_names=all_column_names)


def _column_attributes_for_table(table_name) -> DataFrame:
    return duckdb.sql(f"DESCRIBE SELECT * FROM {table_name};") \
        .df()[["column_name", "column_type"]]


def _column_names(col_attr: DataFrame) -> str:
    col_attr = col_attr.copy()
    col_attr["column_joint"] = col_attr["column_name"] + " " + col_attr["column_type"]

    return str(col_attr["column_joint"].to_list()) \
        .replace('[', '').replace(']', '') \
        .replace('\'', '')


def _create_table_command(table_name: str, col_names: str) -> str:
    return f"CREATE TABLE {table_name} ({col_names})"


def _add_quotes_to_query(query: str, col_names: List[str]) -> str:
    quoted_query = str(query)
    for i in col_names:
        if i in query:
            quoted_query = quoted_query.replace(i, f'"{i}"')
    return query


@timer
def lang2sql(api_key: str, query: str, model: str = "gpt-3.5-turbo", temperature: int = 0,
             max_tokens: int = 256, top_p: int = 1, frequency_penalty: int = 0, presence_penalty: int = 0) -> Response:
    openai.api_key = api_key

    m = _create_sql_message(query=query)

    message = [
        {
            "role": "system",
            "content": m.system
        },
        {
            "role": "user",
            "content": m.user
        }
    ]

    openai_response: OpenAIObject = openai.ChatCompletion.create(
        model=model,
        messages=message,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty)

    sql_query = _add_quotes_to_query(
        query=openai_response["choices"][0]["message"]["content"],
        col_names=m.all_column_names
    )

    return Response(request_message=m, open_ai_response=openai_response, sql=sql_query)


@timer
def run_query(query: str, api_key: str) -> DataFrame:
    response = lang2sql(api_key=api_key, query=query)
    print(f'Usage for {run_query.__name__}: {response.open_ai_response["usage"]}')

    print('---------------')
    print(f'{response.sql=}')
    print('---------------')

    return duckdb.sql(response.sql).df()
