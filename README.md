# DS_chatbot
# Digico Solutions Chatbot

## Part 1: Scraping Data and Cleaning

### Overview
This project provides a complete solution for scraping data from websites and cleaning text for use in Retrieval-Augmented Generation (RAG) workflows. The pipeline handles URL extraction, text extraction, cleaning, and storage of processed content in a structured format.

### Features
- **URL Extraction:** Fetches all URLs from sitemaps.  
- **Text Extraction:** Extracts raw text from web pages using helper functions.  
- **Data Cleaning Pipeline:** Removes headers, footers, repetitive words, special characters, and whitespace.  
- **Flexible Metadata Handling:** Supports storing metadata for each document (e.g., source URL, section, date).  
- **RAG-Ready:** Produces clean text suitable for embedding into vector databases like Chroma.  

### Project Structure
```
project/
│
├── scrape_website.py # Helper functions to fetch URLs and extract raw text
├── extract_data.py # Methods for extracting text and saving it
├── clean_data.py # Pipeline for cleaning text (headers, footers, special characters)
├── variables.py # Variables and configurations used across the project
├── scraped_data/ # Raw scraped files
├── scraped_data_clean/ # Cleaned output files
└── README.md
```
### Setup

1. **Create a virtual environment**  
   ```
   # Windows
   python -m venv venv
   ```
2. **Activate the virtual environment**
   ```
   .\venv\Scripts\activate.bat
   ```
3. **Install dependencies (Python 3.10+ recommended)**
   ```
   pip install -r requirements.txt
    ```
   

### Installation
1. **Clone the repository**
  ```
  git clone https://github.com/yourusername/project.git](https://github.com/Jinanrachid/DS_chatbot.git
  cd DS_chatbot
  ```
### Usage
1. **Scrape data**
  ```
  python scrape_website.py
  ```
2. **Clean data**
  ```
  python clean_data.py
  ```

