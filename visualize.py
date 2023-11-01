from dataclasses import dataclass

import openai
from openai.openai_object import OpenAIObject
from pandas import DataFrame


@dataclass
class Response:
    request_prompt: str
    open_ai_response: OpenAIObject
    code: str


def _create_viz_message(df: DataFrame, query: str) -> str:
    prompt = f"""You are given the following pandas dataframe dtypes
    
    {df.dtypes}
    
    You have pandas, numpy, plotly available to you.
    
    Write python code that visualizes the dataframe as a {query}
    """
    return prompt


def code_to_visualize(df: DataFrame, query: str, api_key: str, model: str = "gpt-3.5-turbo-instruct",
                      temperature: int = 0, max_tokens: int = 256, top_p: int = 1, frequency_penalty: int = 0,
                      presence_penalty: int = 0) -> Response:
    openai.api_key = api_key

    prompt = _create_viz_message(df=df, query=query)
    openai_response: OpenAIObject = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty)

    return Response(prompt, openai_response, openai_response["choices"][0]["text"])


def visualize(df: DataFrame, query: str, api_key: str) -> None:
    response = code_to_visualize(df=df, query=query, api_key=api_key)
    print(f'Usage for {visualize.__name__}: {response.open_ai_response["usage"]}')

    exec(response.code)
