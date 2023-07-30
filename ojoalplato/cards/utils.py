import openai
import environ


def paraphrase_text(text):
    env = environ.Env()
    openai.api_key = env('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Parafrasea el siguiente texto: {text}"}],
    )
    return response.choices[0].message.content
