import os
import time
from PIL import Image

from google.adk import Agent
from google.adk.tools import ToolContext, load_artifacts
from google.genai import Client, types

from . import prompt


async def generate_image(img_prompt: str):
    client = Client()
    
    response = client.models.generate_images(
        model="imagen-4.0-fast-generate-001",
        prompt=img_prompt,
        config=types.GenerateImagesConfig(
            aspect_ratio="9:16",
            number_of_images=1,
        ),
    )
    
    if not response.generated_images:
        return {"status": "failed", "detail": "Image generation failed."}
        
    # get the image bytes
    image_data = response.generated_images[0].image.image_bytes
    
    # ensure outputs directory exists in the root
    output_dir = os.path.join(os.getcwd(), "travel_assistant_agent/outputs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # save to local outputs
    ts = int(round(time.time(), 0))
    filename = f"image_{ts}.png"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "wb") as f:
        f.write(image_data)

    return {
        "status": "success",
        "detail": f"Generated trip infographic: {filename}",
        "filepath": filepath,
    }


image_generator_agent = Agent(
    model="gemini-2.5-flash",
    name="image_generator_agent",
    instruction=prompt.IMAGE_GENERATOR_PROMPT,
    tools=[generate_image, load_artifacts],
)
