from openai import OpenAI
import json

def get_bot_response(question):
    try:
        client = OpenAI(api_key="YOUR_API_KEY")
        with open('info.json','r',encoding='utf-8') as f:
            bank_data=json.load(f)
        bank_data_str=json.dumps(bank_data)
        system_prompt = f"""
        You are a professional Armenian Bank Assistant.
        Your knowledge is strictly limited to the following data: {bank_data_str}

        SCOPE OF WORK:
        1. You MUST only answer questions related to:
        - Credits (Վարկեր)
        - Deposits (Ավանդներ)
        - Branch Locations (Մասնաճյուղերի գտնվելու վայրեր)
        2. You must answer in Armenian.
        3. Use only the provided data to give answers.

        STRICT CONSTRAINTS:
        - If a user asks a question OUTSIDE of the three topics above (e.g., general knowledge, weather, other banking services), you MUST strictly respond with: "Ես չեմ կարող պատասխանել այդ հարցին"
        - If the information is not present in the provided data, also respond with: "Ես չեմ կարող պատասխանել այդ հարցին"
        - Do not provide any financial advice or information outside of the given context.
        """
        response=client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                    ]
        )
        return print("Bot:", response.choices[0].message.content)
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""