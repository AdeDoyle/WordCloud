
import docx
import re


def get_text(filename):
    """Opens a word document and returns the full text"""
    file = docx.Document(filename + ".docx")
    paragraphs = []
    for para in file.paragraphs:
        if para.text:
            paragraphs.append(para.text)
    return '\n\n'.join(paragraphs)


def clean_text(text_file, cleaning_style):
    if cleaning_style == "Gaeilge":

        # Separate conjoined tokens
        conjlist = []
        conjpat = re.compile(r"(^| )[bBdD]'[\w-]*[ \n.,\"'\)]")
        conjpatiter = conjpat.finditer(text_file)
        for conj in conjpatiter:
            clean_conj = conj.group()
            conjlist.append(clean_conj)
        for conj_found in sorted(list(set(conjlist))):
            conj_cleaned = "' ".join(conj_found.split("'"))
            text_file = conj_cleaned.join(text_file.split(conj_found))

        # Remove Eclipsis and h-mutation
        eclipsis_exceptions = ["bhfuil"]
        ecllist = []
        eclpat = re.compile(r' ((h|[nt]-)[aeiouáéíóúAEIOUÁÉÍÓÚ]|[tn][AEIOUÁÉÍÓÚ]'
                            r'|m[bB]|g[cC]|n[dDgG]|bh[fF]|b[pP]|t[sS]|d[tT])[\w-]*[ \n.,"\'\)]')
        eclpatiter = eclpat.finditer(text_file)
        for ecl in eclpatiter:
            clean_ecl = ecl.group()
            if len(clean_ecl) > 4 and clean_ecl[1:-1] not in eclipsis_exceptions:
                ecllist.append(clean_ecl)
        for ecl_found in sorted(list(set(ecllist))):
            if ecl_found[2] == "-":
                ecl_removed = ecl_found[0] + ecl_found[3:]
            elif ecl_found[1:3] == "bh":
                ecl_removed = ecl_found[0] + ecl_found[3:]
            else:
                ecl_removed = ecl_found[0] + ecl_found[2:]
            text_file = ecl_removed.join(text_file.split(ecl_found))

        # Combine hyphenated words into single words (wordcloud library does not allow hyphenated words)
        hyphen_exceptions = ['Laidine-Gearmáinise']
        prefixes = ['an-', 'An-', 'mí-', 'Mí-', 'neamh-', 'Neamh-', 'réamh-', 'Réamh-', 'ró-', 'Ró-']
        suffixes = ['-san']
        hyphlist = []
        hyph_pat = re.compile(r'(^| )[a-zA-ZáéíóúÁÉÍÓÚ]+-[a-zA-ZáéíóúÁÉÍÓÚ]+[ \n.,"\'\)]')
        hyphpatiter = hyph_pat.finditer(text_file)
        for hyph in hyphpatiter:
            clean_hyph = hyph.group()
            if len(clean_hyph) > 4 and clean_hyph[1:-1] not in hyphen_exceptions:
                hyphlist.append(clean_hyph)
        for hyph_found in sorted(list(set(hyphlist))):
            hyph_cleaned = None
            for prefix in prefixes:
                if hyph_found[1:len(prefix) + 1] == prefix:
                    hyph_cleaned = " ".join(hyph_found.split("-"))
                    break
            for suffix in suffixes:
                if hyph_found[-len(suffix) - 1:-1] == suffix:
                    hyph_cleaned = "".join(hyph_found.split("-"))
                    break
            if not hyph_cleaned:
                hyph_cleaned = "".join(hyph_found.split("-"))
            text_file = hyph_cleaned.join(text_file.split(hyph_found))

        # Remove Lenition
        lenition_exceptions = ['bhfuil', 'bhí', 'Bhí', 'chaith', 'Chaith', 'chéad', 'Chéad', 'chéanna', 'Chéanna',
                               'chomh', 'Chomh', 'chuala', 'Chuala', 'chun', 'Chun', 'chur', 'Chur', 'dhá', 'Dhá',
                               'shílfeá', 'Shílfeá', 'tháinig', 'Tháinig', 'thar', 'Thar', 'thíos', 'Thíos',
                               'thosaigh', 'Thosaigh', 'thug', 'Thug']
        lenlist = []
        len_pat = re.compile(r' [bcdfgmpstBCDFGMPST]h[\w-]*[ \n.,"\'\)]')
        lenpatiter = len_pat.finditer(text_file)
        for lenit in lenpatiter:
            clean_len = lenit.group()
            if len(clean_len) > 4 and clean_len[1:-1] not in lenition_exceptions:
                lenlist.append(clean_len)
        for len_found in sorted(list(set(lenlist))):
            len_removed = len_found[:2] + len_found[3:]
            text_file = len_removed.join(text_file.split(len_found))

    return text_file

