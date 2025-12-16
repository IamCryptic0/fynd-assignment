from google import genai
import pandas as pd
import json
import time
import os
from google.genai import types
from sklearn.metrics import accuracy_score, classification_report
from prompts import (
    system_instruction, 
    prompt1,
    prompt2, 
    prompt3
)


from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
df = pd.read_csv('yelp.csv')
sampled_df = df[['text', 'stars']].dropna().sample(n=100, random_state=47).reset_index(drop=True)

print(f"Dataset ready. Rows: {len(sampled_df)}")


def classify_reviews(dataframe, prompt_func, approach_name):
    
    results = []
    
    print(f"--- Starting {approach_name} ---")

    generation_config = types.GenerateContentConfig(
        system_instruction=system_instruction(),
        response_mime_type="application/json",
        temperature=0.1
    )
    
    for index, row in dataframe.iterrows():
        review = row['text']
        actual_stars = row['stars']
        
        try:
            prompt = prompt_func(review)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=generation_config
            )
            
            data = json.loads(response.text)
            pred = data.get("predicted_stars")
            explanation = data.get("explanation")
            
            
            results.append({
                "original_text": review,
                "actual_stars": actual_stars,
                "predicted_stars": int(pred),
                "explanation": explanation,
                "approach": approach_name,
                "json_valid": True
            })
            
        except Exception as e:
            print(f"Error on row {index}: {e}")
            results.append({
                "original_text": review,
                "actual_stars": actual_stars,
                "predicted_stars": 0, #0 is failure to review by LLM
                "explanation": str(e),
                "approach": approach_name,
                "json_valid": False
            })
            
        time.sleep(1) 
        
        
        print(f"Processed {index} rows...")

    return pd.DataFrame(results)

df_simp = classify_reviews(sampled_df, prompt1, "Simple")
df_few = classify_reviews(sampled_df, prompt2, "Few-Shot")
df_reas = classify_reviews(sampled_df, prompt3, "Reasoning")

def evaluate_performance(df_results):
    valid_df = df_results[df_results['json_valid'] == True]
    
    acc = accuracy_score(valid_df['actual_stars'], valid_df['predicted_stars'])
    validity_rate = df_results['json_valid'].mean() * 100
    
    return acc, validity_rate

acc_z, val_z = evaluate_performance(df_simp)
acc_f, val_f = evaluate_performance(df_few)
acc_c, val_c = evaluate_performance(df_reas)

comparison_table = pd.DataFrame({
    "Approach": ["Simple", "Few-Shot", "Reasoning"],
    "Accuracy": [acc_z, acc_f, acc_c],
    "JSON Validity (%)": [val_z, val_f, val_c]
})

df_simp.to_csv("simple.csv", index=False)
df_few.to_csv("few-shot.csv", index=False)
df_reas.to_csv("reasoning.csv", index=False)
comparison_table.to_csv("comparision.csv", index=False)