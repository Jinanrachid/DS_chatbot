import os
import re

import variables
from scrape_website import create_folder


def replace_text(text,word):
    ''' remove words from text'''
    return text.replace(word, "")

#before removeing \n
def remove_repetetive_words(text):
    '''' remove repetetion from text'''
    text =  re.sub(r'\b(\w+)\s+\1 \1\b', '\1', text)
    text =  re.sub(r'(\b\w+\b\n) \1 \1', '\1', text)
    return text

def remove_special_char(text):
    ''' remove special characters from text'''
    return re.sub(r'=+|~+|\*+\w*|<|/>|--+|->', '', text)

def remove_after_prev(text):
    ''' remove everything in text after prev previous'''
    return re.split(r'\bPrev\b\n \bPrevious\b', text, flags=re.IGNORECASE)[0]
"""
def remove_more_blogs(text):
    #text = re.sub(r'\bBlog\n.+\n.+\n.+\n Blog\n.+\n.+\n.+\n Blog\n.+\n.+\n.+\n\sMore\sBlogs\b', '', text)
    #text = re.split(r'Blog\n.+\n.+\n.+\n Blog\n.+\n.+\n.+\n Blog\n.+\n.+\n.+\n\sMore\sBlogs', text, flags=re.IGNORECASE)[0]
    #text = re.split(r'Blog\n.+\n Blog\n.+\n Blog\n.+\n\sMore\sBlogs', text, flags=re.IGNORECASE)[0]
    return replace_text(text,word)
"""
def remove_other_events(text):
    ''' remove everything after Other Events'''
    #re.split(r'Other\sEvents(\n.+)+More\sBlogs', text, flags=re.IGNORECASE)[0]
    return re.split(r'\bOther\sEvents\b', text, flags=re.IGNORECASE)[0]

def remove_empty_lines(text):
    ''' remove empty lines'''
    return re.sub(r'\n\s*\n+', '\n', text)
"""
def remove_start_end_space(text):
    ''' remove whitespace from the beginning and the end'''
    return re.sub(r'^\s\s*|\s\s*$', '', text)
"""
def strip_lines_from_text(text):
    """
    Removes leading and trailing spaces from each line in the input text
    and returns the cleaned text.
    """
    stripped_lines = [line.strip() for line in text.splitlines()]
    return "\n".join(stripped_lines)

"""
def remove_extra_space(text):
    return re.sub(r'\s{2,}', ' ', text)
"""
def remove_x(text):
    ''' remove char ×'''
    return re.sub(r'(^×\s*\W)|(\s*×\s*)', "", text)

def remove_star(text):
    ''' remove * '''
    return re.sub(r'\s*\*\s', "", text)

def clean_text(text, matches_list):
    ''' clean text pipline'''
    # Remove exact phrases
    for phrase in matches_list:
        text = text.replace(phrase, "")
        #Remove whitespace so that the headers are consistent.
        if phrase == variables.language:
            text = remove_empty_lines(text)


    text = remove_x(text)

    text = remove_star(text)

    text = remove_repetetive_words(text)

    text = remove_special_char(text)

    text = remove_after_prev(text)

    #text = remove_more_blogs(text)
    text = remove_other_events(text)

    text = strip_lines_from_text(text)

    #text = remove_extra_space(text)
    text  = text.replace("  ", " ")

    text = remove_empty_lines(text)
    text = text.replace("\n", " ").strip()  # Replace line breaks with space and remove extra spaces

    return text

def remove_newline(text,filename,foldername,include_list, exclude_list):
    ''' remove new line from specific files'''
    if (filename in include_list) or ((foldername == "page-sitemap") and filename not in exclude_list):
        text = text.replace("\n", "")
        text.replace("  ", " ")
    return text

def clean_folder_files(root_path, clean_root = "scraped_data_clean"):
    """
    Processes all files in folders under root_path:
    - Creates corresponding folder in clean_root
    - Reads each file
    - Cleans text by removing phrases and newlines
    - Saves cleaned content to clean_root
    """
    for folder_name in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder_name)

        # Check if it is a folder and create the corresponding folder in clean_root
        if os.path.isdir(folder_path) and create_folder(folder_name, root=clean_root):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                if os.path.isfile(file_path):
                    # Read file content
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Remove header/footer if needed

                    # Clean the text
                    content = clean_text(content, variables.remove_phrases)
                    content = remove_newline(
                        content,
                        file_name,
                        folder_name,
                        variables.files_with_newline,
                        variables.files_to_skip
                    )

                    # Skip certain files/folders
                    if file_name not in variables.remove_files and folder_name != "job-category-sitemap":
                        cleaned_path = os.path.join(clean_root, folder_name, file_name)
                        with open(cleaned_path, "w", encoding="utf-8") as file:
                            file.write(content)


if __name__ == "__main__":

    root_path = "scraped_data"
    clean_folder_files(root_path)
