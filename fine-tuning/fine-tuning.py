from openai import OpenAI
client = OpenAI()

def file_upload(file_path):
    respond = client.files.create(
        file=open("dataset.jsonl", "rb"),
        purpose="fine-tune"
    )
    print(respond)

def fine_tuning(file_id, model_id):
    respond = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=model_id
    )
    print(respond)

def check_jobs(num_jobs):
    respond = client.fine_tuning.jobs.list(limit=num_jobs)
    print(respond)

def check_job(job_id):
    respond = client.fine_tuning.jobs.retrieve(job_id)
    print(respond)

def chat_with_gpt(prompt, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a coder of yu-gi-oh card game simulator. i will give you the data and effect of a card, you need to write the code to simulate the card, based on ygopro."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7  # Adjust creativity level
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# client.fine_tuning.jobs.create(
#     training_file="file-NKTeu5r1xUAJ3yQGXB15Mp",
#     model="gpt-4o-mini-2024-07-18"
# )
# check_job("ftjob-oDrQLSqXxZXQHYPVNof6h5Gm")

if __name__ == "__main__":
    print("AI Chat Agent (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_with_gpt(user_input, "ft:gpt-4o-mini-2024-07-18:noobility::AlX20DFH")
        print(f"AI: {response}")
