from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import base64
import logging
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_agent():
    """
    Initialize and return the LangChain Azure OpenAI agent.
    
    Returns:
        AzureChatOpenAI: Configured Azure OpenAI client
    """
    try:
        logger.info("Initializing Azure OpenAI agent...")
        logger.info(f"Using deployment: {settings.azure_openai_deployment_name}")
        logger.info(f"Using API version: {settings.azure_openai_api_version}")
        
        agent = AzureChatOpenAI(
            azure_deployment=settings.azure_openai_deployment_name,
            openai_api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            temperature=0.5
        )
        logger.info("Azure OpenAI agent initialized successfully")
        return agent
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI agent: {str(e)}")
        raise Exception(f"Failed to initialize Azure OpenAI agent: {str(e)}")


from langchain_community.callbacks.manager import get_openai_callback

def analyze_image(agent, prompt: str, image_data=None):
    """
    Use the agent to analyze an image based on the given prompt.
    
    Args:
        agent: The LangChain Azure OpenAI agent
        prompt: User's prompt for guiding image analysis
        image_data: Optional binary image data
        
    Returns:
        dict: The agent's analysis response and token usage
    """
    logger.info(f"Starting image analysis with prompt: {prompt[:50]}...")
    
    # Start with the system message
    messages = [SystemMessage(content=settings.default_system_prompt)]
    logger.info("Added system message to conversation")
    
    # Prepare the human message content
    if image_data:
        logger.info(f"Processing image data of size: {len(image_data)} bytes")
        # Convert image to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        logger.info("Image converted to base64 format")
        
        # Create a multimodal message with text and image
        human_message_content = [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        logger.info("Created multimodal message with text and image")
        
        human_message = HumanMessage(content=human_message_content)
    else:
        logger.info("No image provided, creating text-only message")
        # Text-only message
        human_message = HumanMessage(content=prompt)
    
    messages.append(human_message)
    
    # Invoke the agent and get the response, tracking costs
    try:
        logger.info("Invoking Azure OpenAI agent for analysis with callback for cost tracking")
        with get_openai_callback() as cb:
            response = agent.invoke(messages)
            logger.info("Successfully received response from Azure OpenAI")
            return {
                "result": response.content,
                "token_usage": {
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost": round(cb.total_cost, 4)
                }
            }
    except Exception as e:
        logger.error(f"Error during image analysis: {str(e)}")
        raise Exception(f"Error during image analysis: {str(e)}")

