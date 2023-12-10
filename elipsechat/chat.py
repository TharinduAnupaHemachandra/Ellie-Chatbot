import openai
from typing import List, Optional, Union

import os

from elipsechat.price_calculator import price_calculator

import threading

#openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = "open-ai-key"

# Initialize the conversation with the system message.
messages = [
    {"role": "system",
     "content": "You are an insurance agent who chats based on the given context. Be strict with the context given."}
]

generated_text = ["Curently not available!"]

price = 0

def chat_generate_text(
        firebase_db,
        session_id,
        prompt: str,
        openai_api_key: str = None,
        model: str = "gpt-3.5-turbo-16k",
        system_prompt: str = "You are a helpful assistant.",
        temperature: float = 0.5,
        max_tokens: int = 512,
        n: int = 1,
        stop: Optional[Union[str, list]] = None,
        presence_penalty: float = 0,
        frequency_penalty: float = 0.1,
) -> List[str]:
    global messages  # Declare messages as a global variable
    global price

    # Append the user's message to the conversation.
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
        )

        generated_texts = [
            choice.message["content"].strip() for choice in response["choices"]
        ]

        # Initialize an empty string to store the combined content
        combined_content = ""

        # Iterate through the list of dictionaries and append content to the combined string with a space
        for index, item in enumerate(messages):
            combined_content += item["content"]

            # Add a space if it's not the last item
            # if index < len(list_of_dicts) - 1:
            #     combined_content += " "

        t1 = threading.Thread(target=price_calculator, args=(combined_content, generated_texts[0], 0.003, 0.004, 5, firebase_db, session_id))

        t1.start()

        # Append the assistant's reply to the conversation.
        messages.append({"role": "system", "content": generated_texts[0]})

        print(generated_texts[0])

        # t1 = threading.Thread(target=price_calculator, args=(combined_content, generated_texts[0], 0.0015, 0.002, 5, db, session_id))
        #
        # t1.start()

        return generated_texts[0]
    except openai.error.OpenAIError as e:
        if "maximum context length" in str(e) and "reduce the length of the messages" in str(e):
            print(e)
            # Handle "max tokens" error by keeping only the previous response.
            # Use global to reference the global variable
            messages = messages[-2:]  # Keep only the previous user and assistant messages

            combined_content = ""

            # Iterate through the list of dictionaries and append content to the combined string with a space
            for index, item in enumerate(messages):
                combined_content += item["content"]

                # Add a space if it's not the last item
                # if index < len(list_of_dicts) - 1:
                #     combined_content += " "

            return chat_generate_text(
                firebase_db,
                session_id,
                prompt,
                openai_api_key,
                model,
                system_prompt,
                temperature,
                max_tokens,
                n,
                stop,
                presence_penalty,
                frequency_penalty,
            )

        else:
            print(e)
            return [str(e)]