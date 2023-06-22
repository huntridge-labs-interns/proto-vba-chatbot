#%% 
# Imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search

# Models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# %%
# Load your API key from an environment variable or secret management service
openai.api_key = "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"
#%%
# Test the API connection
response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Test prompt",
    max_tokens=5
)

# Check the response
print(response)

#%%
encoding = tiktoken.get_encoding(embedding_encoding)
df = pd.read_csv("M28C_Scrap_QA.csv")

#%%
df["combined"] = ("Title: " + df.Heading.str.strip() + "; Content: " + df.Content.str.strip())
df.head(2)

#%%
df["embedding"] = df.combined.apply(lambda x: get_embedding(x, model=EMBEDDING_MODEL))

#%%
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
#%%
df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
df.to_csv('output/embedded_1k_reviews.csv', index=False)