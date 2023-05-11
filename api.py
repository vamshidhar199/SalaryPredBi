import subprocess
import json
from transformers import T5ForConditionalGeneration, T5Tokenizer

def call_openai_api(question):
    # Define the curl command with required parameters
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": ""}, {"role": "user", "content": question}],
        "temperature": 0.2,
        "max_tokens": 100
    }

    curl_cmd = [
        "curl",
        "https://api.openai.com/v1/chat/completions",
        "-H",
        "Content-Type: application/json",
        "-H",
        f"Authorization: Bearer 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",
        "-d",
        json.dumps(data)
    ]

    # Run the curl command as a subprocess
    process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error messages from the subprocess
    output, errors = process.communicate()

    # Print the output and error messages to the console
    response_dict = json.loads(output.decode("utf-8"))

    # Get the messages from the response
    messages = response_dict['choices'][0]['message']['content']
    print("Original Response:")
    print(messages)

    # Perform text summarization
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")

    inputs = tokenizer.encode(messages, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=50, num_beams=4, early_stopping=True)
    summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print("Summarized Response:")
    print(summarized_text)

    print(errors.decode("utf-8"))
    return summarized_text

def main():
    question = "salary of a person with 3 years of experience in Spring Boot in California"
    call_openai_api(question)

if __name__ == '__main__':
    main()
