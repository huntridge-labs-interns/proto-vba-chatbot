# Training a LLM using Custom Data
## Description
Test and evaluate the viability of using OpenAI's fine-tuning API for Government use cases using real-world Government documents. The goal of this project is not to create the most accurate custom chat interface, but rather to prove the concept of training a LLM using custom data. The data pertains to the M28C Glossary of Terms, PART I Overview, PART II Office Administration, PART III Program Administration, PART IV Application, Evaluation, and Planning, PART V Case Management, PART VI Employment Services, PART VII Other Benefits Case Management, and PART VIII Program Oversight in the Veteran Readiness and Employment (VR&E) program. Found here: https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000143195/M28C-Table-of-Contents%3FarticleViewContext=article_view_related_article

## Directory Structure
| Path  | Description |
| ------------- | ------------- |
| Embeddings  | Contains CSVs that are used in Embedding.py and Interface.py. The folder and the contents within the folder are generated in Embedding.py file. The CSVs located here will be called Embedding1.csv, Embedding2.csv, Embedding#.csv. They're chunks of a dataframe due to size issues. Each file will contain a Title, Heading, Content, Tokens, Combined, and embedding columns.  |
| ExtraCSVs  | Contains CSVs that are not used in the current model. Includes M28C_Scrap_Q.csv (Generated in DataCleaning.py. Contains Title, Heading, Content, Tokens, Context, Questions), M28C_Scrap_QA.csv (Generated in DataCleaning.py. Contains Title, Heading, Content, Tokens, Context, Questions, Answers), M28C_Scrap_Token_Reduction.csv (Generated in Scrap.py and used in DataCleaning.py. Scraped dataframe of M28C Manual that limits tokens for each row. Contains Chapter Title, Heading, Content, Tokens)  |
| assets  | Images used in the interface design  |
| chromedriver_win32  | Chromedriver used to scrap the required web pages. Constantly being updated and depending on system being used will need to download specific version. Information can be found here: [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/home)  |
| DataCleaning.py  | **Input**: M28C_Scrap.csv, GlossaryTerms.csv, ExtraData.csv <br />Cleans/formats CSVs for embedding. Outputs the ForEmbedding.csv. Can also create questions and answers about the data from context using OpenAI. <br />**Output**: ForEmbedding.csv, M28C_Q.csv, M28C_QA.csv    |
| Embedding.py  | **Input**: ForEmbedding.csv <br />Embeds the dataframe, chunks the dataframe into manageable sections, and answers a query using GPT and a dataframe of relevant texts and embeddings. <br />**Output**: Embeddings folder with subsequent CSVs  |
| Interface.py  | **Input**: Embeddings folder <br />Creates an interface to query chatGPT and ask it user questions.  |
| Scrap.py  | Scraps the VR&E Manual. Includes options for scraping one chapter, scraping all chapters with no restrictions, scraping all chapters with token reduction, scraping all chapters with token reduction (splitting on paragraphs) and scraping the Glossary of Terms. <br />**Output**: M28C_Scrap.csv, GlossaryTerms.csv, M28C_Scrap_Token_Reduction.csv, M28C_Scrap_Token_Reduction_By_Paragraph.csv  |
| ExtraData.csv  | Created manually to answer questions the model was struggling with. Can add additional questions/answers to this file as needed. Contains Chapter Title, Heading, Question, Content, Tokens  |
| ForEmbedding.csv  | Generated in DataCleaning.py and used in Embedding.py. Contains Title, Heading, Content, Tokens, Context   |
| GlossaryTerms.csv  | Generated in Scrap.py and used in DataCleaning.py. Scraped dataframe of the Glossary of Terms that contains Chapter Title, Heading, Content, and Tokens.  |
| M28C_Scrap.csv  | Generated in Scrap.py and used in DataCleaning.py. Scraped dataframe of M28C Manual that has no token limit. Contains Chapter Title, Heading, Content, Tokens  |

## Steps to Replicate Project
Progression of project goes Scrap.py > DataCleaning.py > Embedding.py > Interface.py. Can either run each program or can use the provided CSVs 
1. Download repository
2. To install all required Python packages use: pip install -r requirements.txt  
3. Run Scrap.py to generate M28C_Scrap.csv and GlossaryTerms.csv
   - Chromedriver will most likely need to be updated/downloaded for specific version of chrome and/or machine being used. Information can be found here: [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/home)
   - Recommend running the code in the sections labeled DATA SCRAPING ALL CHAPTERS and DATA SCRAP GLOSSARY OF TERMS
   - If issues with the URL(s), this [M28C.I.A.1 Veteran Readiness and Employment Manual](https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000146267/M28CIA1-Veteran-Readiness-and-Employment-Manual%3FarticleViewContext=article_view_related_article) should be used for DATA SCRAPING ALL CHAPTERS and this [M28C Glossary of Terms](https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000144454/M28C-Glossary-of-Terms%3FarticleViewContext=article_view_related_article) for DATA SCRAP GLOSSARY OF TERMS    
5. Run DataCleaning.py
   - Enter your OpenAI API KEY
   - Option to run code to generate questions and answers based on context
6. Run Embedding.py
   - Enter your OpenAI API KEY
   - Can add words/definitions to synonym list
   - At end of the code, can change the question in ask() to ask the model a question
7. Run Interface.py
   - Enter your OpenAI API Key
   - Can add words/definitions to synonym list
   - Run all cells and an interface will open
   - Type relevant question/phrase to get a response
   
## Screenshot of Interface
<kbd>![DemoScreenshot](https://github.com/huntridge-labs-interns/vre-poc/assets/135631259/4a388d48-d51f-4fb8-95fa-0d6079e83cf7)<kbd>

## Running Interface in Web Browser
1. Have all the necessary libraries installed. You can install them using the following command in the terminal:
   - pip install dash dash-bootstrap-components
2. Save the Interface.py file with your openAI API Key
3. Open the integrated terminal/terminal and navigate to the directoy where your 'Interface.py' file is located using the 'cd' command.
   - For example: cd path/to/your/project
4. Run the Interface by executing the following command in the terminal: python Interface.py
5. After running the command, you should see output in the terminal indicating that the server is running. It will mention the URL where your app is hosted, which is usually 'http://127.0.0.1:8050/'
6. Open a web browser and enter the URL mentioned in the terminal ('http://127.0.0.1:8050/' by default). This will open the Dash app interface in your web browser.
This should allow interaction with the interface in your web browser. Any changes made to the code will automatically be reflected when you refresh the web page.
Please note that while the development server is running, you'll see the terminal output and logs there. If you want to stop the server, you can do so by pressing Ctrl+C in the terminal.
