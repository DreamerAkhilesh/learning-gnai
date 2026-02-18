"""
Advanced Multimodal Examples

This file demonstrates advanced use cases for GPT-4 Vision:
1. Multiple images in one request
2. Visual question answering
3. Image comparison
4. Local image processing (base64)
"""

import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def encode_image_to_base64(image_path: str) -> str:
    """
    Convert a local image file to base64 encoding.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string with data URI prefix
    """
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Determine MIME type based on file extension
    extension = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(extension, 'image/jpeg')
    
    return f"data:{mime_type};base64,{encoded}"


def example_1_visual_qa():
    """
    Example 1: Visual Question Answering
    Ask specific questions about an image.
    """
    print("\n" + "=" * 60)
    print("Example 1: Visual Question Answering")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What colors are prominent in this image? What mood does it convey?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://images.pexels.com/photos/12899196/pexels-photo-12899196.jpeg"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    
    print(response.choices[0].message.content)


def example_2_multiple_images():
    """
    Example 2: Analyzing Multiple Images
    Compare or analyze multiple images in one request.
    """
    print("\n" + "=" * 60)
    print("Example 2: Multiple Image Analysis")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Compare these two images. What are the similarities and differences?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://images.pexels.com/photos/12899196/pexels-photo-12899196.jpeg"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg"
                        }
                    }
                ]
            }
        ],
        max_tokens=400
    )
    
    print(response.choices[0].message.content)


def example_3_detailed_analysis():
    """
    Example 3: Detailed Image Analysis
    Request comprehensive analysis with high detail.
    """
    print("\n" + "=" * 60)
    print("Example 3: Detailed Image Analysis")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Provide a detailed analysis of this image including:
                        1. Main subject and composition
                        2. Lighting and atmosphere
                        3. Colors and their emotional impact
                        4. Potential use cases (marketing, editorial, etc.)
                        5. Technical quality assessment"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://images.pexels.com/photos/12899196/pexels-photo-12899196.jpeg",
                            "detail": "high"  # Request high-resolution analysis
                        }
                    }
                ]
            }
        ],
        max_tokens=600
    )
    
    print(response.choices[0].message.content)


def example_4_local_image():
    """
    Example 4: Processing Local Images
    Analyze images from your local filesystem using base64 encoding.
    
    Note: Requires a local image file. Update the path accordingly.
    """
    print("\n" + "=" * 60)
    print("Example 4: Local Image Processing")
    print("=" * 60)
    
    # Example path - update this to your actual image path
    image_path = "sample_image.jpg"
    
    # Check if file exists
    if not Path(image_path).exists():
        print(f"⚠️  Image not found: {image_path}")
        print("   Please provide a valid image path to test this example.")
        return
    
    try:
        # Encode image to base64
        base64_image = encode_image_to_base64(image_path)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in detail."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")


def example_5_conversation_with_images():
    """
    Example 5: Multi-turn Conversation with Images
    Have a conversation about images with context.
    """
    print("\n" + "=" * 60)
    print("Example 5: Conversation with Images")
    print("=" * 60)
    
    # First message with image
    response1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's the main subject of this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://images.pexels.com/photos/12899196/pexels-photo-12899196.jpeg"
                        }
                    }
                ]
            }
        ],
        max_tokens=200
    )
    
    print("User: What's the main subject of this image?")
    print(f"Assistant: {response1.choices[0].message.content}\n")
    
    # Follow-up question (without re-sending image)
    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's the main subject of this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://images.pexels.com/photos/12899196/pexels-photo-12899196.jpeg"
                        }
                    }
                ]
            },
            {
                "role": "assistant",
                "content": response1.choices[0].message.content
            },
            {
                "role": "user",
                "content": "What emotions does this image evoke?"
            }
        ],
        max_tokens=200
    )
    
    print("User: What emotions does this image evoke?")
    print(f"Assistant: {response2.choices[0].message.content}")


def main():
    """
    Run all examples.
    """
    print("\n🖼️  Advanced Multimodal Examples with GPT-4 Vision")
    print("=" * 60)
    
    try:
        example_1_visual_qa()
        example_2_multiple_images()
        example_3_detailed_analysis()
        example_4_local_image()
        example_5_conversation_with_images()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your OPENAI_API_KEY is set in the .env file")


if __name__ == "__main__":
    main()
