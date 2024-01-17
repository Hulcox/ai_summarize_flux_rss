import feedparser
import ssl
from datetime import datetime
import os
import textwrap
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

ssl._create_default_https_context = ssl._create_unverified_context

model = "openchat"
max_limit= 4

def summarize_by_ai(url):
  loader = WebBaseLoader(url)

  prompt_template = """Write a summary in a perfect french of this following article:
  "{document}"
  SUMMARY IN FRENCH:"""
  prompt = PromptTemplate.from_template(prompt_template)

  llm = Ollama(
      model=model,
      callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
  )
  llm_chain = LLMChain(llm=llm, prompt=prompt)
  stuff_chain = StuffDocumentsChain(llm_chain=llm_chain)

  docs = loader.load()

  return stuff_chain.invoke(docs)

def flux_rss(url):
    
    feed = feedparser.parse(url)

    if 'bozo_exception' in feed and feed.bozo_exception:
        print("Error lors de la récupération du flux RSS:", feed.bozo_exception)
        return None
    
    print("Titre du flux:", feed.feed.title)
    print("Description du flux:", feed.feed.description)

    today = datetime.now().date()

    for entry in feed.entries[:max_limit]:
        
        try:
          publication_date = datetime.strptime(entry.published , "%a, %d %b %Y %H:%M:%S %z").date()
        except (AttributeError, ValueError):
          print("Erreur pour cette artcile dans ce flux RSS")
          return
         
        if publication_date == today:
          print("\nTitre de l'article:", entry.title)
          print("Date de publication:", entry.published)
          print("Lien de l'article:", entry.link)
          print("Résumé de l'article (Flux RSS):", entry.summary)

          print("Résumé de l'article (AI):\n")
          ai_summarize = summarize_by_ai(entry.link)

          print("\n")
          
          save_in_folder(feed.feed, entry, textwrap.fill(ai_summarize['output_text'], width=120))
          
          print("-" * 40)

def save_in_folder(feed, entry, ai_summarize):
    folder_path = "summary/"+feed.title+"/"+datetime.now().date().strftime('%d-%m-%Y')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(folder_path+"/"+entry.title+"_resume.txt", "w+") as fichier:
        fichier.write("Titre de l'article: " + entry.title + "\n")
        fichier.write("Date de publication: " + entry.published + "\n")        
        fichier.write("Lien de l'article: " + entry.link + "\n")
        fichier.write("Résumé de l'article (Flux RSS): " + entry.summary + "\n")
        fichier.write("Résumé de l'article (AI):\n")
        fichier.write(ai_summarize)
    
    print("Résumé sauvegarder dans : " + folder_path+"/"+entry.title+"_resume.txt")

def urls_list(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]
    
urls_flux_rss = urls_list("url_flux_rss.txt")
    
for url in urls_flux_rss:
    print("\n=== Récupération du flux RSS depuis", url, "===")
    flux_rss(url)