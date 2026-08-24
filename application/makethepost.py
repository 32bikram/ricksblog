from fastapi import HTTPException, status
from . import schemas, config
from google import genai
from google.genai import types
def call_llm(message : str):
    prompt = ''' you will convert the message I sent you like it is said by Rick Sanchez from Rick and Morty.
    you are not gonna say anything new or out of context of my message. you will
    say the same thing but in Rick's characteristic way.
    Rules:
    - Preserve the original meaning, claims, opinions, and information.
    - Do not add new facts, arguments, opinions, or ideas.
    - Do not remove important information.
    - Only change the wording, tone, humor, and phrasing to fit the character.
    - Keep the response roughly the same length as the original unless necessary for the transformation.
    
    Absolute Must follow rules:
    - Return ONLY valid JSON. proper formating of json is must. opening and closing bracket and colons.
    - schema:{
        "message" : ""
    }
    '''
    client = genai.Client(api_key=config.settings.llm_api)
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[prompt, message],
            config=types.GenerateContentConfig(
                max_output_tokens=1200,   #minimum 800 works
                temperature=0.3
            ),
        )
        if response.text is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail ="Please post appropriate text"
            )
        return response.text
    except HTTPException:
        raise
    except:
        raise HTTPException(
            status_code = status.HTTP_402_PAYMENT_REQUIRED,
            detail = "Not enough api token"
        )