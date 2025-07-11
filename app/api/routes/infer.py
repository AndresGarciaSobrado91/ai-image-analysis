from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import Optional
import io
from PIL import Image
import logging
from app.core.agent import get_agent, analyze_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/infer",
    tags=["inference"]
)

@router.post("/")
async def infer(
    prompt: str = Form(..., description="The prompt to guide image analysis"),
    image: Optional[UploadFile] = File(None, description="Image file to be analyzed")
):
    """
    Analyze an image based on the provided prompt using an AI agent.
    
    - **prompt**: Text prompt describing what to analyze or look for in the image
    - **image**: Optional image file to analyze (JPG, PNG, etc.)
    
    Returns analysis results from the AI agent.
    """
    try:
        # Process the image if provided
        image_data = None
        if image:
            contents = await image.read()
            try:
                # Open and validate the image
                img = Image.open(io.BytesIO(contents))
                # Convert to RGB if image has alpha channel
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')
                # Get image as bytes for processing
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                image_data = img_byte_arr.getvalue()
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
        
        # Get agent and analyze the image
        agent = get_agent()
        CYAN = "\033[96m"
        RED = "\033[91m"
        RESET = "\033[0m"
        logger.info(f"{CYAN}User prompt: {prompt}{RESET}")
        analysis = analyze_image(agent, prompt, image_data)
        logger.info(f"{CYAN}Final analysis result: {analysis['result']}{RESET}")
        logger.info(f"{CYAN}Token usage: {analysis['token_usage']}{RESET}")
        return {
            "analysis": analysis["result"],
            "token_usage": analysis["token_usage"]
        }
    
    except Exception as e:
        RED = "\033[91m"
        RESET = "\033[0m"
        logger.error(f"{RED}Error during analysis: {str(e)}{RESET}")
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")
