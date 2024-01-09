from bs4 import BeautifulSoup

from pathlib import Path

def get_extension(filename):
    """
    Parsing filename and returning file extension.
    """
    extension = Path(filename).suffix.replace('.', '')

    return extension

def convert_preview(article_list:list):
    """
    Removes html tags and sets them for preview.
    """
    for index, article in enumerate(article_list):
        article_list[index].content = BeautifulSoup(article.content, 'html.parser').get_text()[:400]+'...'
    
    return article_list

def remove_tags(article:str):
    """
    Removes html tags
    """

    return BeautifulSoup(article, 'html.parser').get_text()
