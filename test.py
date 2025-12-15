# from utils.LLM_helper import generate_user_response

# print(generate_user_response("Delivery was late but support was helpful.", 3))

from google import genai
import os
client = genai.Client(api_key="AIzaSyDAMc5mBirHEPxHgdLTvtWj90Yg2es53vs")
try:
    for m in client.models.list():
        if "generateContent" in m.supported_actions:
            print(f"✅ Available: {m.name}")

except Exception as e:
    print(f"#####Error#### : {e}")