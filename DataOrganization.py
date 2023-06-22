#%% Import
import pandas as pd
import re
import openai
import os
from openai.embeddings_utils import get_embedding
import json

#%% Read the CSV into the code
df = pd.read_csv("M28C_Scrap_Token_Reduction.csv")

# %% Functions to clean the CSV
# Function for unicode (standardize accented characters)
def standardize_accented_chars(text):
    fixed_text = text.replace("’", "'")
    return fixed_text

# Function to standardize heading numbers (removes extra period)
def standardize_heading(heading):
    # Match a double number followed by a period and an extra period
    pattern = r"(\d+\.\d+)\."
    # Replace the second period with an empty string
    cleaned_heading = re.sub(pattern, r"\1", heading)
    return cleaned_heading

# Function to format the headings with the same spacing (all headings should be X.XX  Chapter Name)
def format_heading(heading):
    # Match a double number followed by one or more spaces and a word
    pattern = r"(\d+\.\d+)\s{2}(\w+|\d+)"
    # Check if the heading matches the expected format
    match = re.match(pattern, heading)
    if match:
        # Heading is already in the correct format
        return heading
    else:
        # Extract the first two numbers and the remaining text
        match = re.match(r"(\d+\.\d+)\s*(.*)", heading)
        if match:
            # Check if there's only one space after the number
            if len(match.group(2)) > 0 and match.group(2)[0] != " ":
                # Add an additional space after the number
                formatted_heading = f"{match.group(1)}  {match.group(2)}"
            else:
                # Heading is already in the correct format
                formatted_heading = heading
            return formatted_heading
        else:
            # Heading doesn't match any expected format, return it as is
            return heading

#%% 
# Editing the CSV for OpenAI finetuning API
# Step 1: Fix unicode
df['Chapter Title'] = df['Chapter Title'].apply(standardize_accented_chars)
df['Heading'] = df['Heading'].apply(standardize_accented_chars)
df['Content'] = df['Content'].apply(standardize_accented_chars)

# Step 2: Standardize Headings (Extra period(s) removed)
df['Heading'] = df['Heading'].apply(standardize_heading)

# Step 3: Format Headings (spacing fixed)
df['Heading'] = df['Heading'].apply(format_heading)

#%%
# Create a context by concatenating the title, heading, and the content of each section
df = df.rename(columns={'Chapter Title': 'Title'})
df['Context'] = df.Title + "\n" + df.Heading + "\n\n" + df.Content

#########################################################################################################################################################################

#%% 
# Load your API key
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

#########################################################################################################################################################################
#%% 
# Embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

#%%
# Create combined column that combines the Heading and the Content
df["combined"] = ("Title: " + df.Heading.str.strip() + "; Content: " + df.Content.str.strip())
df.head(2)

#%% 
# Embed Document Chunks
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
print(df)
#%% 
# df.to_csv('output/embedded_1k_reviews.csv', index=False)

#########################################################################################################################################################################

#%% Create questions based on the context
# Can experiment more with temperature, max_tokens, top_p, frequency_penalty, and presence_penalty
def get_questions(Context):
    try:
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"Write questions based on the text below\n\nText: {Context}\n\nQuestions:\n1.",
            temperature=0,
            max_tokens= 300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        return response['choices'][0]['text']
    except:
        return ""


df['Questions']= df.Context.apply(get_questions)
df['Questions'] = "1." + df.Questions
print(df[['Questions']].values[0][0])

# %%
# Check if questions populated correctly
df.to_csv('M28C_Scrap_Q.csv', index=False)

#%% Create answers based on the context and question
#  Nearly 2 hour runtime (Increase tokens to 300 when have time)
def get_answers(row):
    try:
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=f"Write answer based on the text below\n\nText: {row.Context}\n\nQuestions:\n{row.Questions}\n\nAnswers:\n1.",
            temperature=0,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['text']
    except Exception as e:
        print (e)
        return ""


df['Answers']= df.apply(get_answers, axis=1)
df['Answers'] = "1." + df.Answers
df = df.dropna().reset_index().drop('index',axis=1)
print(df[['Answers']].values[0][0])

# %%
# Check if questions and answers populated correctly
df.to_csv('M28C_Scrap_QA.csv', index=False)

################################################################################################################################################

# %%
# df = pd.read_csv("M28C_Scrap_QA.csv")

# %%
# Create a new dataframe with prompt and completion columns
formatted_df = pd.DataFrame(columns=["prompt", "completion"])

#%% Iterate over each row in the original dataframe
for index, row in df.iterrows():
    # Create a dictionary for each row containing the prompt and completion
    data = {
        "prompt": row["Context"],  # Use the concatenated context as the prompt
        "completion": row["Content"],  # Use the content as the completion
        "question": row["Questions"],  # Include the generated question
        "answer": row["Answers"]  # Include the generated answer
    }

    # Append the dictionary as a new row in the formatted dataframe
    formatted_df = formatted_df.append(data, ignore_index=True)

#%% 
# Save the formatted dataframe to a JSONL file
formatted_df.to_json("M28C_formatted_data.jsonl", orient="records", lines=True)

#%% 
# Verify the content of the JSONL file
with open("M28C_formatted_data.jsonl", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(json.loads(line))
# %%
