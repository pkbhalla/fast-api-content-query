from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import PyPDF2
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import T5ForConditionalGeneration, T5Tokenizer



async def scrape_url(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to scrape the URL: {e}")
       




async def extract_pdf_text(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return ' '.join(text.split())


model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def cosine_similarity_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

def get_text_embedding(text: str) -> np.ndarray:
    return model.encode(text)

t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")
t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")


def paraphrase_text(text: str) -> str:
    input_text = "summarize: " + text
    print(f"Input to T5 model for paraphrasing: {input_text}")
    encoding = t5_tokenizer.encode_plus(input_text, return_tensors="pt")
    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    outputs = t5_model.generate(
        input_ids=input_ids, 
        attention_mask=attention_mask, 
        max_length=100, 
        num_beams=5, 
        early_stopping=True
    )
    paraphrased_text = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Paraphrased text: {paraphrased_text}")
    return paraphrased_text

def find_most_relevant(content: str, question: str) -> str:
    sentences = content.split(". ") 
    question_embedding = get_text_embedding(question)

    most_relevant_sentence = None
    highest_similarity = -1


    for sentence in sentences:
        sentence_embedding = get_text_embedding(sentence)
        similarity = cosine_similarity_vectors(sentence_embedding, question_embedding)

        if similarity > highest_similarity:
            highest_similarity = similarity
            most_relevant_sentence = sentence

    if most_relevant_sentence and highest_similarity > 0.5: 
        paraphrased_response = paraphrase_text(most_relevant_sentence)
        return f"Paraphrased answer: {paraphrased_response}\n\n(Similarity: {highest_similarity:.2f})"
    else:
        return "No relevant content found."