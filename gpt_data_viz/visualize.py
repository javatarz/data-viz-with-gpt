import os
from dataclasses import dataclass

import openai
from openai.openai_object import OpenAIObject
from pandas import DataFrame

from gpt_data_viz.timers import timer


@dataclass
class Response:
    request_prompt: str
    open_ai_response: OpenAIObject
    code: str


def _create_viz_message(df: DataFrame, query: str, csv_path: str) -> str:
    prompt = f"""You are given the following pandas dataframe dtypes that can be read from a CSV file at {csv_path}:
    
    {df.dtypes}
    
    You have pandas, numpy, plotly available to you.
    
    Write python code that visualizes the dataframe in a way that answers the following question: {query}
    
    Return only python code, no need to print anything.
    """
    return prompt


@timer
def code_to_visualize(df: DataFrame, query: str, api_key: str, model: str = "gpt-3.5-turbo-instruct",
                      temperature: int = 0, max_tokens: int = 256, top_p: int = 1, frequency_penalty: int = 0,
                      presence_penalty: int = 0) -> Response:
    openai.api_key = api_key
    csv_path = "tmp/data.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path)

    prompt = _create_viz_message(df=df, query=query, csv_path=csv_path)
    openai_response: OpenAIObject = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty)

    return Response(prompt, openai_response, openai_response["choices"][0]["text"])


@timer
def visualize(df: DataFrame, query: str, api_key: str) -> None:
    response = code_to_visualize(df=df, query=query, api_key=api_key)
    print(f'Usage for {visualize.__name__}: {response.open_ai_response["usage"]}')

    print('---------------')
    print(f'{response.code=}')
    print('---------------')
    exec(response.code)
