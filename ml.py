import os
import openai
from newspaper import Article
from urlextract import URLExtract
from pathlib import Path
from dotenv import load_dotenv
# Load your API key from an environment variable or secret management service
load_dotenv()
openai.api_key = os.environ["OPEN_AI"]

#generateTLDR generates a summary of the article
def makeGPTRequest(prompt):
  response = openai.Completion.create(
  engine="davinci",
  prompt=prompt,
  temperature=0.3,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0)
  return response.choices[0].text

#urlToText converts a URL to a string of text
def urlToText(url = "https://www.google.com"):
  article = Article(url)
  article.download()
  article.parse()
  return article.text

#getURLS takes a message and returns a list of URLs in a string
def getURLS(message): 
  extractor = URLExtract()
  urls = extractor.find_urls(message)
  return urls

#MLHandler takes a message and returns a summary of the article
def MLHandler(message):
  urls = getURLS(message)
  temp = ""
  if not urls:
      return makeGPTRequest(message)
  else:
      for i, siteStr in enumerate([urlToText(URL) for URL in urls]):
          temp = temp + 'Summarizing ' + urls[i] + ': \n' + makeGPTRequest(siteStr + "\ntl;dr") + '\n'
      return temp