import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq()                             # reads GROQ_API_KEY from .env
def call_llm_json(system: str, user: str, model_cls, retries: int = 2):
    """
    Calls the LLM and returns an instance of model_cls, built from its
    reply. Retries once if the reply doesn't match the schema.
    """
    schema = model_cls.model_json_schema()
    last_err = None
    for _ in range(retries + 1):
        resp = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "llama-3.3-70b-versatile"),
            temperature=0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": model_cls.__name__,
                    "schema": schema,
                    "strict": True,
                },
            },
        )
        raw = resp.choices[0].message.content
        try:
            return model_cls.model_validate(json.loads(raw))
        except Exception as e:
            last_err = e
    raise last_err
