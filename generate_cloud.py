
import os
from wordcloud import WordCloud, STOPWORDS
from get_text import get_text, clean_text

irish_stopwords = ['a', 'ach', 'acu', 'ag', 'agus', 'an', 'ar', 'as', 'atá', "b'", 'ba', 'bhí', 'bhfuil', 'chuig', "d'",
                   'de', 'den', 'do', 'don', 'é', 'faoi', 'faoin', 'go', 'i', 'í', 'in', 'ina', 'is', 'le', 'leis',
                   'mar', 'mé', 'mo', 'muid', 'na', 'ná', 'nach', 'ní', 'nó', 'ó', 'ón', 'raibh', 'roimh',
                   'sa', 'san', 'sé', 'seachas', 'seo', 'sí', 'siad', 'sibh', 'sin', 'sinn', 'sna',
                   'tá', 'thar', 'trí', 'tú', 'um']


def generate_cloud(text_file, stop_words=STOPWORDS, text_cleaning=None):
    """Generates a word-cloud using text from a .docx file"""

    # Go to the word-document directory
    main_dir = os.getcwd()
    os.chdir("word_docs")

    # Get the text from the .docx file and clean it
    text = get_text(text_file)
    if text_cleaning:
        text = clean_text(text, text_cleaning)

    # Generate the word-cloud
    wc = WordCloud(
        mode="RGBA",
        background_color=None,
        stopwords=stop_words,
        collocations=False,
        height=100,
        width=1500
    )
    wc.generate(text)

    # Move to the directory where the word-cloud will be saved
    os.chdir(main_dir)
    os.chdir("word_clouds")
    save_dir = os.getcwd()

    # Save the word-cloud
    wc.to_file(text_file + ".png")

    # Return to the main directory
    os.chdir(main_dir)

    return f"Word-cloud saved to directory:\n    {save_dir}"


if __name__ == "__main__":

    """Identify name of word file and appropriate stopwords"""
    filename = "An Ghaeilge"
    sw = irish_stopwords

    """generate the cloud"""
    print(generate_cloud(filename, sw, "Gaeilge"))

