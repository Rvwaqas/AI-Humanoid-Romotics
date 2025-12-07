import os
import glob
import json
import urllib.request
import argparse

# The backend is expected to be running on this URL.
# This is the default for FastAPI apps run with uvicorn.
DEFAULT_BACKEND_URL = "http://localhost:8000"

def get_all_markdown_files(root_dir):
    """
    Finds all markdown files recursively in the specified directory.
    """
    return glob.glob(os.path.join(root_dir, '**', '*.md'), recursive=True)

def read_file_content(filepath):
    """
    Reads and returns the content of a file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def ingest_data(backend_url, content_list):
    """
    Sends the list of content strings to the backend's /ingest endpoint.
    """
    url = f"{backend_url}/ingest"
    data = {"content": content_list}
    
    # Encode the data into a JSON byte string
    json_data = json.dumps(data).encode('utf-8')
    
    # Create the request object
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
    
    print(f"Sending {len(content_list)} documents to {url}...")
    
    try:
        with urllib.request.urlopen(req) as response:
            # Check the response
            if response.status == 200:
                response_body = response.read().decode('utf-8')
                result = json.loads(response_body)
                print("✅ Ingestion successful!")
                print(f"   - Documents ingested: {result.get('count', 'N/A')}")
            else:
                print(f"❌ Ingestion failed. Status code: {response.status}")
                print(f"   - Response: {response.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"❌ An error occurred while trying to connect to the backend.")
        print(f"   - Is the backend running at {backend_url}?")
        print(f"   - Error details: {e.reason}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    """
    Main function to orchestrate the data ingestion process.
    """
    parser = argparse.ArgumentParser(description="Ingest markdown content into the RAG chatbot backend.")
    parser.add_argument(
        "--docs-path",
        default="web/docs",
        help="The relative path to the directory containing the markdown documentation."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_BACKEND_URL,
        help=f"The URL of the backend server. Defaults to {DEFAULT_BACKEND_URL}."
    )
    args = parser.parse_args()

    # Get the absolute path for the docs directory
    docs_dir = os.path.abspath(args.docs_path)

    if not os.path.isdir(docs_dir):
        print(f"❌ Error: The specified docs path '{docs_dir}' does not exist or is not a directory.")
        return

    print(f"🔍 Searching for markdown files in: {docs_dir}")
    markdown_files = get_all_markdown_files(docs_dir)
    
    if not markdown_files:
        print("🟡 No markdown files found. Nothing to ingest.")
        return
        
    print(f"   - Found {len(markdown_files)} files.")

    # Read the content of all found files
    content_to_ingest = [read_file_content(f) for f in markdown_files]
    
    # Send the data to the backend
    ingest_data(args.url, content_to_ingest)


if __name__ == "__main__":
    main()
