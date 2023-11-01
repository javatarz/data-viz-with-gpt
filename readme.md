# Data Visualisation using GPT

Step 1. Add data to the 'data' folder

Step 2. Generate an [OpenAI API key](https://platform.openai.com/account/api-keys) (requires a paid account)

Step 3. Run the command below

```bash
CHATGPT_API_KEY=<api key here> poetry run python data_viz_with_gpt.py --data-query "How many shopping reports do you have per category?" --viz-query "bar chart" --file-to-query shopping_trends
```