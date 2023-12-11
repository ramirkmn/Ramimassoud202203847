import json
import requests


{
" name ": " Jane Smith " ,
" age ": 28 ,
" city ": " Los Angeles " ,
" occupation ": " Graphic Designer " ,
" interests ": [" Art " , " Travel " , " Photography "] ,
" education ": " Bachelor ’ s in Fine Arts " ,
" projects ": [
{
" name ": " Logo Design for Company WinterField " ,
" client ": " Company WinterField " ,
" year ": 2022
} ,
{
" name ": " Illustrations for a book " ,
" client ": " Marie Katterburg " ,
" year ": 2021
}
] ,
" pets ": [{" name ":" thomas " , " type ":" cat "} ,{" name ":" gulpy " , " type ":" frog "}]
}

# Step 1: Read JSON file
with open('./data.json', 'r') as file:
    data = json.load(file)

    # Extracting required data
name = data[" name "]
first_interest = data[" interests "][0]
second_project_client = data[" projects "][1][" client "]
second_pet_name = data[" pets "][1][" name "]

    # Printing extracted data
print(name)
print(first_interest)
print(second_project_client)
print(second_pet_name)

    # Step 2: Using ChatGPT API
api_key = "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"  # Remember to replace "YOUR_API_KEY" with the actual key.
url = "https://api.openai.com/v1/chat/completions"
prompt = f"Based on the data about {name}, a {data[' occupation ']} from {data[' city ']}, who likes {', '.join(data[' interests '])}, create a short story."

payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7
    }

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    response_data = response.json()
    story = response_data["choices"][0]["message"]["content"]

    # Step 3: Writing the story to a new file
    with open('generated_story.txt', 'a') as out_file:

        out_file.write(story)

else:
    print(f"API call failed with status code: {response.status_code}")
    print(response.text)