import spacy

# Load the standard English model
nlp = spacy.load("en_core_web_sm")

def extract_general_features(text, limit=5):
    doc = nlp(text)
    
    # 1. Define Generic "Fluff" Adjectives to remove
    # These apply to ALL categories (Fashion, Tech, Housing, etc.)
    # We remove these so "Luxurious room" becomes just "Room" or "Large Kitchen" becomes "Kitchen"
    ignore_adjectives = {
        'large', 'small', 'free', 'luxurious', 'spacious', 'beautiful', 
        'good', 'best', 'new', 'furnished', 'three', 'two', 'one'
    }

    # 2. Identify Entities to EXCLUDE (Locations, Dates, People)
    # This prevents "Jalandhar City" or "Vinay Nagar" from appearing as features.
    excluded_spans = []
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'DATE', 'TIME', 'cardinal', 'FAC']:
            # GPE = Cities/Countries, FAC = Buildings/Airports
            excluded_spans.append(ent.text.lower())

    candidates = []

    # 3. Iterate over Noun Chunks (The core "things" in the sentence)
    for chunk in doc.noun_chunks:
        # Get the clean text (lowercase)
        text_clean = chunk.text.lower().strip()
        
        # SKIP if the chunk is inside a Location/Date (e.g. skip "Jalandhar City")
        if any(ex in text_clean for ex in excluded_spans):
            continue
            
        # SKIP if it's just a pronoun (e.g. "it", "they")
        if chunk.root.pos_ == 'PRON':
            continue

        # 4. Clean the chunk: Remove the "Fluff" adjectives from the start
        # e.g., "Free car parking" -> "Car parking"
        words = text_clean.split()
        if words[0] in ignore_adjectives and len(words) > 1:
            clean_feature = " ".join(words[1:])
        else:
            clean_feature = text_clean
            
        # Capitalize for display
        final_feature = clean_feature.title()
        
        # Avoid single generic words if possible (optional heuristic)
        # e.g., we prefer "Crompton Gyser" over just "Room"
        candidates.append(final_feature)

    # 5. Deduplicate while preserving order
    unique_features = []
    seen = set()
    
    for item in candidates:
        if item not in seen:
            unique_features.append(item)
            seen.add(item)

    return unique_features[:limit]

# # --- TEST ON YOUR TEXT ---
# text_housing = "Crompton Gyser Sofas table AC large balcony large room large kitchen with chimney washroom with Tub dressing table with wooden almirahs Three Free car parking 112 Vinay Nagar LP Jalandhar City Furnished Luxurious room with Led TV double bed fans lights luxurious room with large wooden almirah and dressing table. Table chair. Free maintenance car parking."

# print(f"Housing Features: {extract_general_features(text_housing)}")

# # --- TEST ON OTHER DOMAINS ---
# text_fashion = "Brand new Nike Air Jordan red sneakers with white laces comfortable sole generic box included."
# print(f"Fashion Features: {extract_general_features(text_fashion)}")

# text_grocery = "Fresh organic apples 1kg bag bananas dairy milk chocolate bar and cold drink."
# print(f"Grocery Features: {extract_general_features(text_grocery)}")