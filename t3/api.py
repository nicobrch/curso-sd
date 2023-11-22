import os
import wikipediaapi
import unidecode


def get_wikipedia_documents():

    wiki_wiki = wikipediaapi.Wikipedia('TareaSD (tareasd@example.com)', 'es')

    documents = []

    article_titles = [
        'One Piece',
        'Monkey D. Luffy',
        'Jujutsu Kaisen',
        'Chainsaw Man',
        'Steins;Gate',
        'Code Geass',
        'The Tatami Galaxy',
        'Hunter × Hunter',
        'Bakuman',
        'Devilman Crybaby',
        'Shingeki no Kyojin',
        'Cowboy Bebop',
        'Neon Genesis Evangelion',
        'El viaje de Chihiro',
        'Samurai Champloo',     # 15
        'FLCL',
        'Naruto',
        'Fullmetal Alchemist',
        'Angel Beats!',
        'Puella Magi Madoka Magica',
        'Psycho-Pass',
        'Plastic Memories',
        'Mob Psycho 100',
        'Kimi no Na wa.',
        'No Game No Life',
        'Dragon Ball',
        'Dragon Ball Z',
        'One Outs',
        'Hajime no Ippo',
        'Slam Dunk'             # 30
    ]

    for title in article_titles:
        page_py = wiki_wiki.page(title)
        if page_py.exists():
            documents.append({
                'title': page_py.title,
                'text': page_py.text,
            })

    return documents


def save_documents_to_folder(documents, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i, doc in enumerate(documents):
        file_path = os.path.join(folder_name, f"document_{i + 1}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {doc['title']}\n\n")
            file.write(doc['text'])


def clean_text(text):
    cleaned_text = unidecode.unidecode(text)
    cleaned_text = ''.join(char for char in cleaned_text if char.isalpha() or char.isspace())
    return cleaned_text


def clean_documents_in_folder(folder_name):
    for filename in os.listdir(folder_name):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_name, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            cleaned_content = clean_text(content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)


if __name__ == "__main__":
    wikipedia_documents = get_wikipedia_documents()

    # Dividir los documentos en dos grupos
    docs_1 = wikipedia_documents[:15]
    docs_2 = wikipedia_documents[15:]

    # Guardar los primeros 15 documentos en "docs_1"
    save_documents_to_folder(docs_1, "docs_1")

    # Guardar los siguientes 15 documentos en "docs_2"
    save_documents_to_folder(docs_2, "docs_2")

    # Limpiar caracteres no pertenecientes al alfabeto español en "docs_1"
    clean_documents_in_folder("docs_1")

    # Limpiar caracteres no pertenecientes al alfabeto español en "docs_2"
    clean_documents_in_folder("docs_2")
