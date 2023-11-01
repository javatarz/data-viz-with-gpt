from dataclasses import dataclass

import duckdb
import openai
from openai.openai_object import OpenAIObject
from pandas import DataFrame


@dataclass
class Message:
    system: str
    user: str
    column_names: str
    column_attr: str


@dataclass
class Response:
    request_message: Message
    open_ai_response: OpenAIObject
    sql: str


def _create_sql_message(table_name: str, query: str) -> Message:
    tbl_describe = duckdb.sql("DESCRIBE SELECT * FROM " + table_name + ";")
    col_attr = tbl_describe.df()[["column_name", "column_type"]]
    col_attr["column_joint"] = col_attr["column_name"] + " " + col_attr["column_type"]
    col_names = str(col_attr["column_joint"].to_list()) \
        .replace('[', '').replace(']', '') \
        .replace('\'', '')

    system = f"""Given the following SQL table, your job is to write queries given a user’s request.
    
    CREATE TABLE {table_name} ({col_names})
    """
    user = f"Write a SQL query that returns - {query}"

    return Message(system=system, user=user, column_names=col_attr["column_name"], column_attr=col_attr["column_type"])


def _add_quotes_to_query(query, col_names):
    quoted_query = str(query)
    for i in col_names:
        if i in query:
            quoted_query = quoted_query.replace(i, f'"{i}"')
    return query


def lang2sql(api_key: str, table_name: str, query: str, model: str = "gpt-3.5-turbo", temperature: int = 0,
             max_tokens: int = 256, top_p: int = 1, frequency_penalty: int = 0, presence_penalty: int = 0) -> Response:
    openai.api_key = api_key

    m = _create_sql_message(table_name=table_name, query=query)

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
        col_names=m.column_names
    )

    return Response(request_message=m, open_ai_response=openai_response, sql=sql_query)


def run_query(query: str, table_name: str, api_key: str) -> DataFrame:
    response = lang2sql(api_key=api_key, table_name=table_name, query=query)
    print(f'Usage for {run_query.__name__}: {response.open_ai_response["usage"]}')

    return duckdb.sql(response.sql).df()
