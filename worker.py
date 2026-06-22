from openai import OpenAI
import requests

openai_client = OpenAI()


def speech_to_text(audio_binary):
    # Set up Watson Speech-to-Text HTTP Api url
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + "/speech-to-text/api/v1/recognize"

    params = {
        "model": "en-US_Multimedia",
    }

    # Send the post request and capture the JSON response
    response = requests.post(
        api_url,
        params=params,
        data=audio_binary
    ).json()

    print("speech to text response:", response)

    # Parse the response to get our transcribed text
    text = None

    while bool(response.get("results")):
        text = (
            response.get("results")
            .pop()
            .get("alternatives")
            .pop()
            .get("transcript")
        )
        print("recognised text:", text)
        return text


def text_to_speech(text, voice=""):
    # Set up Watson Text-to-Speech HTTP Api url
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = (
        base_url
        + "/text-to-speech/api/v1/synthesize?output=output_text.wav"
    )

    # Adding voice parameter if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Set the headers for our HTTP request
    header = {
        "Accept": "audio/wav",
        "Content-Type": "application/json",
    }

    # Set the body of our HTTP request
    json_data = {
        "text": text,
    }

    # Send an HTTP POST request to Watson Text-to-Speech Service
    response = requests.post(
        api_url,
        headers=header,
        json=json_data
    )

    print("text-to-speech", response)
    return response.content


def openai_process_message(user_message):
    # Set the prompt for OpenAI API
    prompt = (
        "Act like a personal assistant. You can respond to questions, "
        "translate sentences, summarize news, and give recommendations. "
        "Keep responses concise - 2 to 3 sentences maximum."
    )

    # Call the OpenAI API to process our prompt
    openai_response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
        max_completion_tokens=1000,
    )

    print("openai response:", openai_response)

    # Parse the response to get the response message
    response_text = openai_response.choices[0].message.content
    return response_text