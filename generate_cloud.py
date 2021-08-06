
import os
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from get_text import get_text, clean_text

irish_stopwords = ['a', 'ach', 'acu', 'ag', 'agus', 'an', 'ar', 'as', 'atá', "b'", 'ba', 'bhí', 'bhfuil', 'chuig', "d'",
                   'de', 'den', 'do', 'don', 'é', 'faoi', 'faoin', 'go', 'i', 'í', 'in', 'ina', 'is', 'le', 'leis',
                   'mar', 'mé', 'mo', 'muid', 'na', 'ná', 'nach', 'ní', 'nó', 'ó', 'ón', 'raibh', 'roimh',
                   'sa', 'san', 'sé', 'seachas', 'seo', 'sí', 'siad', 'sibh', 'sin', 'sinn', 'sna',
                   'tá', 'thar', 'trí', 'tú', 'um']


def generate_cloud(text_file, text_cleaning=None, stop_words=STOPWORDS,
                   background=None, mask=None, maskcolour=False, dimensions=None):
    """Generates a word-cloud using text from a .docx file"""

    # Go to the word-document directory
    # If directory doesn't exist, create it and raise error warning to place word-documents in this directory
    # If the document doesn't exist in the directory, raise error warning to check file name
    main_dir = os.getcwd()
    try:
        os.chdir("word_docs")
    except FileNotFoundError:
        os.mkdir("word_docs")
        raise RuntimeError('Could not find "word_docs" folder\n    Created folder, "word_docs"\n    '
                           'Place .docx word file in "word_docs" folder')
    if text_file not in [x.strip('.docx') for x in os.listdir()]:
        raise RuntimeError(f'Could not find file, "{text_file}", in "word_docs" folder, check file extension is .docx')

    # Get the text from the .docx file and clean it
    text = get_text(text_file)
    if text_cleaning:
        text = clean_text(text, text_cleaning)

    # Generate the word-cloud
    if dimensions and not mask:
        height = dimensions[0]
        width = dimensions[1]
        wc = WordCloud(
            mode="RGBA",
            background_color=background,
            stopwords=stop_words,
            collocations=False,
            height=height,
            width=width
        )
        wc.generate(text)
    elif len(mask) > 0:
        wc = WordCloud(
            mode="RGBA",
            background_color=background,
            stopwords=stop_words,
            collocations=False,
            mask=mask
        )
        wc.generate(text)
        if maskcolour:
            image_colors = ImageColorGenerator(mask)
            wc.recolor(color_func=image_colors)
    else:
        raise RuntimeError("No shape selected for word cloud")

    # Move to the directory where the word-cloud will be saved
    # If directory does not exist, create it
    os.chdir(main_dir)
    try:
        os.chdir("word_clouds")
    except FileNotFoundError:
        os.mkdir("word_clouds")
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
    msk = np.array(Image.open("word_cloud_templates\\eire2.jpg"))

    """generate the cloud"""
    print(generate_cloud(filename, "Gaeilge", sw, background="White", dimensions=[100, 1500]))
    # print(generate_cloud(filename, "Gaeilge", sw, background="White", mask=msk))

