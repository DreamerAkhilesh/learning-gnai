from dotenv import load_dotenv
load_dotenv()


from openai import OpenAI

client = OpenAI() 

client.chat.completions.create(
  model="gpt-4.1-mini",
  messages=[
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "Generate a caption for this image in about 50 words" },
        { "type": "image_url", "image_url": { "url": "" } }
      ]
    }
  ]
)