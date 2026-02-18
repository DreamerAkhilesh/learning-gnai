"""
Multimodal AI - Image Understanding with GPT-4 Vision

This script demonstrates how to use OpenAI's GPT-4 Vision model to:
1. Analyze images from URLs
2. Generate captions and descriptions
3. Answer questions about images

The model can understand and describe images, making it useful for:
- Image captioning
- Visual question answering
- Content moderation
- Accessibility (alt text generation)
"""

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Make a request to GPT-4 Vision model
# Note: GPT-4 Vision can process both text and images in the same request
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Fixed: was "gpt-4.1-mini" which doesn't exist
    # Available vision models: "gpt-4o", "gpt-4o-mini", "gpt-4-turbo"
    messages=[
        {
            "role": "user",
            "content": [
                # Text prompt - what we want the model to do
                {
                    "type": "text",
                    "text": "Generate a caption for this image in about 50 words"
                },
                # Image input - can be URL or base64 encoded image
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/12899196/pexels-photo-12899196.jpeg",
                        # Optional: "detail" parameter controls image resolution
                        # "detail": "high"  # Options: "low", "high", "auto" (default)
                    }
                }
            ]
        }
    ],
    max_tokens=300  # Limit response length
)

# Print the generated caption
print("🖼️  Image Caption:")
print("=" * 60)
print(response.choices[0].message.content)
print("=" * 60)
