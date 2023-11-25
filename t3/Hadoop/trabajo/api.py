import os
import json
import wikipediaapi

paginas = [
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
    'Samurai Champloo',  # 15
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
    'Slam Dunk'  # 30
]


def get_api_documents(folder, page_title, number):
    wiki = wikipediaapi.Wikipedia(user_agent='tareatres', language='es', extract_format=wikipediaapi.ExtractFormat.WIKI)
    page = wiki.page(page_title)
    if page.exists():
        text = '{} {}<splittername>{}'.format(number, page.fullurl, json.dumps(page.text))
        filepath = f"./{folder}/documento_{number}.txt"

        if os.path.isfile(filepath):
            os.remove(filepath)

        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(filepath, "wb") as file:
            file.write(text.encode('utf-8'))


i = 1
for pagina in paginas:
    if i <= 15:
        get_api_documents('docs_1', pagina, i)
    else:
        get_api_documents('docs_2', pagina, i)
    i += 1
