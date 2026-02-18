# Multimodal AI - Image Understanding with GPT-4 Vision

This project demonstrates how to use OpenAI's GPT-4 Vision models to analyze and understand images.

## Overview

GPT-4 Vision models can:
- Generate image captions and descriptions
- Answer questions about images
- Compare multiple images
- Analyze image composition, colors, and mood
- Extract text from images (OCR)
- Identify objects, people, and scenes
- Provide accessibility descriptions

## Files

- `main.py` - Basic image captioning example
- `advanced_examples.py` - Advanced use cases and patterns
- `README.md` - This documentation

## Prerequisites

- Python 3.8+
- OpenAI API key with GPT-4 Vision access
- Internet connection (for URL-based images)

## Setup

### 1. Install Dependencies

```bash
pip install openai python-dotenv
```

### 2. Configure API Key

Create a `.env` file in the project root (or use the existing one):

```env
OPENAI_API_KEY=your_openai_key_here
```

### 3. Run Examples

**Basic Example:**
```bash
python main.py
```

**Advanced Examples:**
```bash
python advanced_examples.py
```

## Available Models

### GPT-4 Vision Models

| Model | Description | Best For |
|-------|-------------|----------|
| `gpt-4o` | Most capable vision model | Complex analysis, high accuracy |
| `gpt-4o-mini` | Faster, more affordable | General use, quick responses |
| `gpt-4-turbo` | Balance of speed and capability | Production applications |

### Model Selection

```python
# High accuracy, slower, more expensive
model="gpt-4o"

# Fast, affordable, good quality
model="gpt-4o-mini"

# Balanced option
model="gpt-4-turbo"
```

## Usage Examples

### 1. Basic Image Captioning

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
```

### 2. Visual Question Answering

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What colors are in this image?"},
                {"type": "image_url", "image_url": {"url": "..."}}
            ]
        }
    ]
)
```

### 3. Multiple Images

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these images"},
                {"type": "image_url", "image_url": {"url": "image1.jpg"}},
                {"type": "image_url", "image_url": {"url": "image2.jpg"}}
            ]
        }
    ]
)
```

### 4. Local Images (Base64)

```python
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image("local_image.jpg")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)
```

### 5. High-Detail Analysis

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this image in detail"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "...",
                        "detail": "high"  # Request high-resolution analysis
                    }
                }
            ]
        }
    ]
)
```

## Image Detail Levels

The `detail` parameter controls image resolution:

| Detail Level | Description | Use Case | Cost |
|--------------|-------------|----------|------|
| `low` | 512x512 resolution | Quick analysis, simple images | Lower |
| `high` | Full resolution | Detailed analysis, text extraction | Higher |
| `auto` (default) | Automatic selection | General use | Variable |

## Use Cases

### 1. Content Moderation
```python
"Is there any inappropriate content in this image?"
```

### 2. Accessibility
```python
"Generate an alt text description for this image for screen readers"
```

### 3. E-commerce
```python
"Describe this product image for an online store listing"
```

### 4. Social Media
```python
"Generate an engaging caption for this photo for Instagram"
```

### 5. Education
```python
"Explain what's happening in this diagram"
```

### 6. Medical (Non-diagnostic)
```python
"Describe the anatomical structures visible in this educational image"
```

### 7. Real Estate
```python
"Describe this property photo highlighting key features"
```

### 8. Art Analysis
```python
"Analyze the composition, colors, and style of this artwork"
```

## Best Practices

### 1. Clear Prompts
```python
# Good
"List all the objects you can see in this image"

# Better
"List all the objects in this image, categorized by type (furniture, electronics, etc.)"
```

### 2. Specify Output Format
```python
"Describe this image in exactly 50 words"
"Provide a JSON response with keys: subject, colors, mood"
```

### 3. Use System Messages
```python
messages=[
    {
        "role": "system",
        "content": "You are an expert art critic. Analyze images with technical precision."
    },
    {
        "role": "user",
        "content": [...]
    }
]
```

### 4. Handle Errors
```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"Error: {e}")
```

### 5. Optimize Costs
- Use `gpt-4o-mini` for most tasks
- Use `low` detail for simple images
- Batch similar requests
- Cache results when possible

## Limitations

### What GPT-4 Vision CAN'T Do
- ❌ Identify specific individuals (privacy protection)
- ❌ Make medical diagnoses
- ❌ Verify authenticity of documents
- ❌ Generate images (use DALL-E for that)
- ❌ Process video (only static images)

### What GPT-4 Vision CAN Do
- ✅ Describe scenes and objects
- ✅ Read and extract text (OCR)
- ✅ Analyze composition and style
- ✅ Answer questions about images
- ✅ Compare multiple images
- ✅ Identify general categories (e.g., "a person", not "John Doe")

## Error Handling

### Common Errors

**1. Invalid Image URL**
```python
# Error: Image URL not accessible
# Solution: Verify URL is public and accessible
```

**2. Image Too Large**
```python
# Error: Image exceeds size limit
# Solution: Resize image or use lower detail level
```

**3. Unsupported Format**
```python
# Supported: JPEG, PNG, GIF, WebP
# Unsupported: BMP, TIFF, SVG
```

**4. Rate Limits**
```python
# Error: Rate limit exceeded
# Solution: Implement retry logic with exponential backoff
```

## Pricing Considerations

### Cost Factors
1. **Model choice**: `gpt-4o-mini` is cheaper than `gpt-4o`
2. **Image detail**: `high` costs more than `low`
3. **Image size**: Larger images cost more
4. **Token usage**: Response length affects cost

### Cost Optimization
```python
# Use mini model for most tasks
model="gpt-4o-mini"

# Use low detail when appropriate
"detail": "low"

# Limit response length
max_tokens=300

# Batch similar requests
# Process multiple images in one request when comparing
```

## Advanced Patterns

### 1. Image + Context
```python
messages=[
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "This is a product photo for our e-commerce site."},
            {"type": "text", "text": "Generate a compelling product description."},
            {"type": "image_url", "image_url": {"url": "..."}}
        ]
    }
]
```

### 2. Multi-turn Conversation
```python
# First turn
messages = [
    {"role": "user", "content": [{"type": "text", "text": "What's in this image?"}, ...]}
]
response1 = client.chat.completions.create(...)

# Second turn (follow-up)
messages.append({"role": "assistant", "content": response1.choices[0].message.content})
messages.append({"role": "user", "content": "Tell me more about the colors"})
response2 = client.chat.completions.create(...)
```

### 3. Structured Output
```python
prompt = """
Analyze this image and respond in JSON format:
{
  "subject": "main subject",
  "colors": ["color1", "color2"],
  "mood": "emotional tone",
  "objects": ["object1", "object2"]
}
"""
```

## Security & Privacy

### Best Practices
1. **Don't send sensitive images** to external APIs
2. **Respect copyright** - only analyze images you have rights to
3. **User consent** - get permission before analyzing user photos
4. **Data retention** - OpenAI doesn't use API data for training (as of 2024)
5. **Compliance** - ensure GDPR/privacy law compliance

### Privacy Protections
- GPT-4 Vision won't identify specific individuals
- Designed to protect personal privacy
- Refuses to analyze certain sensitive content

## Troubleshooting

### Image Not Loading
```python
# Check URL is accessible
import requests
response = requests.get(image_url)
print(response.status_code)  # Should be 200
```

### Poor Quality Results
```python
# Try high detail mode
"detail": "high"

# Use more specific prompts
"Describe the architectural features of this building in detail"

# Use gpt-4o instead of mini
model="gpt-4o"
```

### Rate Limit Errors
```python
import time
from openai import RateLimitError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    time.sleep(60)  # Wait and retry
    response = client.chat.completions.create(...)
```

## Examples in This Project

### main.py
- Basic image captioning
- Simple URL-based image analysis
- Clean, minimal example

### advanced_examples.py
- Visual question answering
- Multiple image comparison
- Detailed analysis with high resolution
- Local image processing (base64)
- Multi-turn conversations

## Next Steps

1. **Experiment** with different prompts
2. **Try different models** to compare quality/cost
3. **Build applications**:
   - Image search engine
   - Content moderation tool
   - Accessibility alt-text generator
   - Product catalog automation
4. **Combine with other APIs**:
   - DALL-E for image generation
   - Whisper for audio transcription
   - GPT-4 for text analysis

## Resources

- [OpenAI Vision API Docs](https://platform.openai.com/docs/guides/vision)
- [OpenAI Pricing](https://openai.com/pricing)
- [Best Practices Guide](https://platform.openai.com/docs/guides/vision/best-practices)
- [API Reference](https://platform.openai.com/docs/api-reference/chat)

## Common Questions

**Q: Can I use this for medical diagnosis?**
A: No, GPT-4 Vision is not approved for medical diagnosis.

**Q: Can it identify people?**
A: No, it's designed to protect privacy and won't identify specific individuals.

**Q: What image formats are supported?**
A: JPEG, PNG, GIF, and WebP.

**Q: Is there a size limit?**
A: Yes, images should be under 20MB. Larger images may need resizing.

**Q: Can I process video?**
A: Not directly. You can extract frames and analyze them individually.

**Q: How accurate is it?**
A: Very accurate for general tasks, but always verify critical information.

---

**Ready to start?** Run `python main.py` for a basic example or `python advanced_examples.py` for more advanced patterns!
