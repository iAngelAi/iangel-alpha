import os
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

async def check_models():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = AsyncAnthropic(api_key=api_key)
    
    models_to_test = [
        "claude-3-5-sonnet-20240620", # Sonnet 3.5 v1
        "claude-3-haiku-20240307"     # Haiku (notre plan B)
    ]
    
    for model in models_to_test:
        print(f"\n🔍 Test du modèle : {model}...")
        try:
            await client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            print(f"✅ ACCÈS CONFIRMÉ pour {model}")
        except Exception as e:
            print(f"❌ ACCÈS REFUSÉ pour {model} : {e}")

if __name__ == "__main__":
    asyncio.run(check_models())

