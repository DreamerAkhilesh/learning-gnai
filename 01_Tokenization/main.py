import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hi, I am Akhilesh"

token = enc.encode(text)
print("Tokens :", token)
# Tokens : [12194, 11, 357, 939, 13232, 71, 2892, 71]

detokenized = enc.decode([12194, 11, 357, 939, 13232, 71, 2892, 71])
print("Detokenized Text :", detokenized)
# Detokenized Text : Hi, I am Akhilesh