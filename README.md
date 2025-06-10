# Healthcare-ChatbotGenAI

## Frontend Code Repository
```
https://github.com/grv-vishal/HealthcareChatbot-frontend
```

## How To Run
### Create a Git Repo like this and colne your https repo link to local code editor i.e. VS Code 

```
Project Repo: https://github.com/grv-vishal/Healthcare-ChatbotGenAI.git
```

### Create a conda environment after opening repository

``` bash
conda create -n healthbot python=3.10 -y
```

``` bash
conda activate healthbot
```

### Install the requirements

``` bash
pip install -r requirements.txt
```

### Create a `.env` file in the root directory and add your Pinecone & Huggingface LLM Model credentials as follows:

```ini
PINECONE_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
HUGGINGFACE_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```


