# FastAPI Content Query

## Description

`fastapi-content-query` is a backend service built with FastAPI that provides APIs for processing web URLs and PDF documents. It also offers a chat interface for querying processed content using embeddings for accurate response generation.

## Features

- **Process Web URL**: Scrapes content from a given URL and stores it.
- **Process PDF Document**: Extracts and stores text from uploaded PDF documents.
- **Chat Interface**: Allows users to query stored content with responses generated using embeddings and cosine similarity.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker (for deployment)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/fastapi-content-query.git
   cd fastapi-content-query

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

### Running the service

1. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload

2. **Test the API endpoints:**

    - Process Web URL:
   ```bash
    curl -X POST "http://127.0.0.1:8000/process_url" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
    ```
    - Process PDF Document:
      ```bash
      curl -X POST "http://127.0.0.1:8000/process_pdf" -F "file=@/path/to/file.pdf"
      ```
    - Chat API:
      ```bash
      curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"chat_id":"your_chat_id", "question":"What is the document about?"}'
      ```


This was done as an assignment.
