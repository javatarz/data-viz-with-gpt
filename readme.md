# Data Visualisation using GPT

Step 1. Add data to the 'data' folder

Step 2. Generate an [OpenAI API key](https://platform.openai.com/account/api-keys) (requires a paid account)

Step 3. Run the command below

```bash
CHATGPT_API_KEY=<api key here> poetry run python data_viz_with_gpt.py --data-query "How many people do we have data for every affiliation name?" --viz-query "bar chart"
```

## Sample queries
### Working
* "How many unique people affiliations do we have?"
* "How many people do we have data for every affiliation name?"
* "How many unique titles (in relationship table) do you have for every affiliation name (from people table)?"
* "How many unique affiliation names (from people table) do you have for every title (from relationship table)?"
* "How many unique affiliations (from people table) do you have for every title (from relationship table)?"
* "How many unique affiliations do people have for every relationship title?"

### Not Working
* "How many unique affiliations do people have for every title from a relationship?" - no query is built
* "How many unique people affiliations do we have for every relationship title?" - generates incorrect query

## Sample visualisations
* bar chart
* pie chart
* line chart