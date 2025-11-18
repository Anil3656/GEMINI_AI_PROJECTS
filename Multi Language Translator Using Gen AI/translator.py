# translator.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config import GOOGLE_GENAI_API_KEY, GENIE_MODEL

# Export API key for libraries that read from environment
os.environ["GOOGLE_GENAI_API_KEY"] = GOOGLE_GENAI_API_KEY


def translate_text_with_gemini(text: str, source_lang: str = "English", target_lang: str = "Telugu") -> str:
    """
    Uses Gemini via langchain-google-genai to translate text.
    """

    # --- FIX 1: Remove broken hard-coded API pattern check ---
    if not GOOGLE_GENAI_API_KEY:
        raise ValueError("GOOGLE_GENAI_API_KEY not set in config.py")

    # --- Initialize Model ---
    model = ChatGoogleGenerativeAI(
        model=GENIE_MODEL,
        google_api_key=GOOGLE_GENAI_API_KEY
    )

    # --- Prompt Template ---
    system_template = (
        "You are a translation engine. Translate text accurately and naturally. "
        "Return ONLY the translated text."
    )

    user_template = (
        "Translate the following text from {source_lang} to {target_lang}:\n\n"
        "{text}\n\n"
        "Return only the translation."
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", user_template)
    ])

    prompt = prompt_template.invoke({
        "source_lang": source_lang,
        "target_lang": target_lang,
        "text": text
    })

    # --- Call Model ---
    response = model.invoke(prompt)

    # --- Extract Output Safely ---
    try:
        return response.content.strip()
    except:
        return str(response).strip()


# ------------------ TEST RUNNER ------------------
# Run:  python translator.py  to check if working
if __name__ == "__main__":
    print("Testing translator...\n")
    result = translate_text_with_gemini("I am Fine?", "English", "Telugu")
    print("Translation:", result)
