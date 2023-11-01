# Data Visualisation using GPT

Step 1. Download the data the URL mentioned at `data/source.txt` and extract it into the `data` folder

Step 2. Generate an [OpenAI API key](https://platform.openai.com/account/api-keys) (requires a paid account)

Step 3. Run the command below

```bash
CHATGPT_API_KEY=<api key here> poetry run python data_viz_with_gpt.py --data-query <data-query> --viz-query <viz-query>
```

## Sample queries
### Working
#### Bar charts
* `--data-query "How many unique people affiliations do we have?"`
* `--data-query "How many people do we have data for every affiliation name?"`
* `--data-query "How many unique titles (in relationship table) do you have for every affiliation name (from people table)? Please give me the top 10 results."`
* `--data-query "How many unique affiliations do people have for every relationship title? Please give me the top 10 results."`

#### Pie chart
* `--data-query "How many unique affiliations do people have for every relationship title? Please give me the top 10 results." --viz-query "how much share does each title have?"`

#### Line chart
* `--data-query "How many unique affiliations do people have for every relationship title? Please give me the top 10 results." --viz-query "Can you visualise this as a line chart?"`
* `--data-query "What is the total number of acquisitions per year (by acquisition date)?"`
* `--data-query "What is the total number of acquisitions per year?"`
* `--data-query "What is the total number of acquisitions per year after 2002?"`
* `--data-query "What is the total number of acquisitions per year between 2002 and 2010?"`
* `--data-query "What is the total number of acquisitions per year in the 20th century?"`

It is interesting that a line chart was created for time series data without being explicitly asked for. :smile:

### Not Working
* `--data-query "How many unique affiliations do people have for every title from a relationship?"` - no query is built
* `--data-query "How many unique people affiliations do we have for every relationship title?"` - generates incorrect query
