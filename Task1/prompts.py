def system_instruction():
    """Defines the strict JSON output format required."""
    return """
    You are an expert sentiment analyzer for Yelp reviews.
    You MUST output valid JSON only. No markdown, no pre-amble.
    Format:
    {
        "predicted_stars": <int between 1 and 5>,
        "explanation": "<brief reasoning>"
    }
    """

def prompt1(review_text):
    return f"""
    Analyze this review and predict the star rating (1-5).
    Review: "{review_text}"
    """

def prompt2(review_text):
    return f"""
    Analyze this review and predict the star rating (1-5).
    
    Examples:
    Review: "Terrible service, food was cold." -> {{"predicted_stars": 1, "explanation": "Negative sentiment regarding service and food quality."}}
    Review: "Decent place, but a bit overpriced." -> {{"predicted_stars": 3, "explanation": "Mixed sentiment: good place but negative value."}}
    Review: "Absolutely loved it! Best pizza ever." -> {{"predicted_stars": 5, "explanation": "Strong positive sentiment."}}
    
    Now analyze this one:
    Review: "{review_text}"
    """

def prompt3(review_text):
    return f"""
    Analyze this review step-by-step.
    1. Identify positive and negative phrases.
    2. Determine the overall tone (angry, happy, neutral).
    3. Assign a star rating (1-5) based on the evidence.
    
    Review: "{review_text}"
    """