# Digico Solutions Chatbot

## Part 1: Scraping Data and Cleaning

###Overview
This project provides a complete solution for scraping data from websites, cleaning text, and using the processed content to build a chatbot for Digico Solutions. The pipeline handles URL extraction, text extraction, cleaning, and storage of the data, which is then used in a Retrieval-Augmented Generation (RAG) workflow. The chatbot leverages LangChain, ChromaDB, and Amazon Bedrock to provide intelligent, context-aware responses based on the scraped content.

### Features
- **URL Extraction:** Fetches all URLs from sitemaps.  
- **Text Extraction:** Extracts raw text from web pages using helper functions.  
- **Data Cleaning Pipeline:** Removes headers, footers, repetitive words, special characters, and whitespace.  
- **Flexible Metadata Handling:** Supports storing metadata for each document (e.g., source URL, section, date).  
- **RAG-Ready:** Produces clean text suitable for embedding into vector databases like Chroma.
- **Semantic:** Chunking: Splits cleaned text into meaningful chunks using a semantic chunking method.
- **Embeddings:** with Amazon Titan: Generates embeddings for each chunk using the Titan model from Amazon Bedrock.
- **Vector Database Storage:** Saves chunk embeddings and metadata to ChromaDB hosted on AWS EC2.
- **RAG System for Q&A:** Creates a retrieval-augmented generation (RAG) system that answers user questions based on company information.
- **Session Management:** Uses DynamoDB to store and manage session data for user interactions.

### Project Structure
```
project/
│
├── scrape_website.py           # Helper functions to fetch URLs and extract raw text
├── extract_data.py             # Methods for extracting text and saving it
├── clean_data.py               # Pipeline for cleaning text (headers, footers, special characters)
├── variables.py                # Variables and configurations used across the project
├── scraped_data/               # Raw scraped files
├── scraped_data_clean/         # Cleaned output files
├── README.md
│
├── chatbot/                    # Chatbot system and RAG pipeline
│   ├── Chatbot_system.py       # Run this to start the chatbot
│   ├── Claude_config.py        # Claude model configuration
│   ├── Connectdb.py            # Connect to ChromaDB (update IP after EC2 restart)
│   ├── Create_chunksv1.py      # Script to create chunks from documents
│   ├── Delete_collection.py    # Delete collection from ChromaDB (for testing)
│   ├── Dynamodb_creation.py    # Create table in DynamoDB
│   ├── Embed_model.py          # Embedding model used to embed chunks
│   ├── Prompt_creation.py      # Create prompts for the Claude model
│   ├── Read_and_store.py       # Read chunks and store them in ChromaDB
│   └── Chunks/                 # Generated chunks from documents
│
└── requirements.txt            # Freeze project dependencies

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

## Installing and Running ChromaDB on EC2

### EC2 Configuration
- **Instance type:** t3.large  
- **OS:** Ubuntu 22  
- **User:** ubuntu  
- **EBS Volume:** 8 GB  

### 1. Install Docker

Follow the official [Docker Engine installation guide for Ubuntu](https://docs.docker.com/engine/install/ubuntu/). Then run:

```
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
docker --version
2. Pull and Run ChromaDB Docker Image
1.	Pull the ChromaDB image:
docker pull chromadb/chroma:0.6.4.dev283
2.	Run ChromaDB as a container with persistent storage:
sudo docker run -d -p 8000:8000 \
  --name jovial_cartwrigt \
  --restart unless-stopped \
  -v /home/ubuntu/chroma_data:/root/.chromadb/chroma.db \
  chromadb/chroma:0.6.4.dev283
Note: Initially, I ran the container without specifying a volume path, which caused data not to be saved persistently. Adding -v /home/ubuntu/chroma_data:/root/.chromadb/chroma.db ensures that ChromaDB data is stored on the EC2 host.
3.	Verify the container is running:
sudo docker ps
sudo docker logs -f jovial_cartwrigt
sudo lsof -i -P -n | grep LISTEN | grep 8000
curl http://localhost:8000/api/v2/heartbeat
# should return {"status":"ok"}
sudo docker ps
sudo docker logs -f jovial_cartwrigt
sudo lsof -i -P -n | grep LISTEN | grep 8000
curl http://localhost:8000/api/v2/heartbeat
# should return {"status":"ok"}
3. Managing the Container
During debugging or maintenance, you can use:
sudo docker stop jovial_cartwrigt   # Stop container
sudo docker rm jovial_cartwrigt     # Remove container
sudo docker start jovial_cartwrigt  # Restart existing container
Note: When turning off the EC2 instance and running it again, only SSH and ChromaDB will start. Update the IP address in the connectdb file after restarting the instance.

```

## Create chunks
```
python Create_chunksv1.py 
```
## update IP in connectdb

## Store embeddings in chromadb
```
Read_and_store.py
```
## Run Chatbot
```
Chatbot_system.py
```



