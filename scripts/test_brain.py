import os
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

async def test_connection():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    # On teste avec Haiku (plus rapide, moins cher) pour valider la connexion
    model = "claude-3-haiku-20240307" 
    
    print(f"🔍 Tentative de connexion avec le modèle: {model}")
    print(f"🔑 Clé trouvée: {'Oui (commence par ' + api_key[:10] + '...)' if api_key else 'Non'}")
    
    client = AsyncAnthropic(api_key=api_key)
    
    try:
        message = await client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Dis bonjour."}]
        )
        print(f"✅ SUCCÈS ! Claude a répondu: {message.content[0].text}")
    except Exception as e:
        print(f"❌ ÉCHEC : {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
