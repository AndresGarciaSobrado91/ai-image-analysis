# AI Image Analysis Service

A Python service that runs an AI agent backed by Azure OpenAI LLM using LangChain. The service provides an API endpoint that allows users to send a prompt and an optional image for analysis.

## Features

- FastAPI-based RESTful API
- Integration with Azure OpenAI via LangChain
- Image analysis capabilities
- Customizable system instructions

## Requirements

- Python 3.8+
- Azure OpenAI API access

## Setup

1. Clone this repository:

```bash
git clone <repository-url>
cd ai-ads-filtering
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

5. Update the `.env` file with your Azure OpenAI credentials:

```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=your_azure_openai_api_version
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

## Running the Service

You can run the service using UV (a high-performance Python ASGI server):

```bash
python -m uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### POST /infer

Analyze an image using the AI agent.

**Parameters:**

- `prompt` (required, form): Text prompt describing what to analyze or look for in the image
- `image` (optional, file): Image file to be analyzed

**Example using curl:**

```bash
# With image
curl -X POST "http://localhost:8000/infer" \
  -H "accept: application/json" \
  -F "prompt=Analyze this image and describe what you see" \
  -F "image=@/path/to/image.jpg"

# Without image
curl -X POST "http://localhost:8000/infer" \
  -H "accept: application/json" \
  -F "prompt=What can you tell me about image analysis?"
```

### Example response

```json
{
  "analysis": "This is an image of ...",
  "token_usage": {
    "total_tokens": 123,
    "prompt_tokens": 45,
    "completion_tokens": 78,
    "total_cost": 0.0123
  }
}
```

## Usage

### Using the Web UI

The service also provides a modern web interface for easy image analysis.

1. Start the server as above.
2. Open your browser and go to [http://localhost:8000/](http://localhost:8000/).
3. Enter your prompt, upload an image (optional), and click **Analyze**.
4. The result and token usage will be displayed below.
5. Use the **Try Again** button to reset and analyze another image or prompt.

> The web UI features a modern, user-friendly design with multiline prompt support, image preview, and clear state management.

## Customizing the Agent

The default system instructions for the agent can be modified in `app/core/config.py`.