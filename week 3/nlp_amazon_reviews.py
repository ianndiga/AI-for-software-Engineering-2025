import spacy
import pandas as pd
import random
from spacy import displacy
from collections import Counter
import matplotlib.pyplot as plt

print("Loading spaCy model...")

nlp = spacy.load("en_core_web_sm")

reviews = [
    "I absolutely love my new iPhone 14 Pro from Apple. The camera quality is amazing and battery life lasts all day!",
    "The Samsung Galaxy S23 is terrible. The screen cracked after one week and customer service was horrible.",
    "Just bought a Sony headphones from Amazon. The sound quality is incredible but the comfort could be better.",
    "My Dell laptop stopped working after 2 months. Worst purchase ever, never buying Dell again.",
    "The new Microsoft Surface Pro is fantastic for work. Great performance and the pen is very responsive.",
    "Bose QuietComfort headphones are worth every penny. Noise cancellation is perfect for flights.",
    "This HP printer is a nightmare. It constantly jams and the ink is too expensive.",
    "Google Pixel 7 has the best camera I've ever used. Android 13 runs smoothly on this device.",
    "Lenovo ThinkPad is built like a tank. Perfect for business use and very reliable.",
    "Apple MacBook Pro with M2 chip is revolutionary. Fast, efficient, and the display is stunning."
]

print(f"Analyzing {len(reviews)} sample reviews...")

results = []

for i, review in enumerate(reviews):
    print(f"\n--- Review {i+1} ---")
    print(f"Text: {review}")
    
    doc = nlp(review)
    
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Entities found: {entities}")
    
    positive_words = ['love', 'amazing', 'incredible', 'fantastic', 'great', 'perfect', 'best', 'revolutionary', 'stunning']
    negative_words = ['terrible', 'horrible', 'worst', 'nightmare', 'jams']
    
    positive_count = sum(1 for word in positive_words if word in review.lower())
    negative_count = sum(1 for word in negative_words if word in review.lower())
    
    if positive_count > negative_count:
        sentiment = "POSITIVE"
    elif negative_count > positive_count:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    
    print(f"Sentiment: {sentiment} (Positive words: {positive_count}, Negative words: {negative_count})")
    
    results.append({
        'review': review,
        'entities': entities,
        'sentiment': sentiment,
        'positive_words': positive_count,
        'negative_words': negative_count
    })

results_df = pd.DataFrame(results)

print("\n=== Overall Analysis ===")
print(f"Total reviews: {len(results_df)}")
print(f"Positive reviews: {len(results_df[results_df['sentiment'] == 'POSITIVE'])}")
print(f"Negative reviews: {len(results_df[results_df['sentiment'] == 'NEGATIVE'])}")
print(f"Neutral reviews: {len(results_df[results_df['sentiment'] == 'NEUTRAL'])}")

all_entities = []
for entities_list in results_df['entities']:
    all_entities.extend(entities_list)

entity_df = pd.DataFrame(all_entities, columns=['Entity', 'Label'])
entity_counts = entity_df['Entity'].value_counts()

print("\nMost common entities:")
print(entity_counts.head(10))

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
entity_label_counts = entity_df['Label'].value_counts()
entity_label_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution of Entity Types')
plt.xlabel('Entity Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.subplot(2, 2, 2)
sentiment_counts = results_df['sentiment'].value_counts()
colors = ['green', 'red', 'gray']
sentiment_counts.plot(kind='bar', color=colors)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.subplot(2, 2, 3)
product_entities = entity_df[entity_df['Label'].isin(['ORG', 'PRODUCT'])]
product_counts = product_entities['Entity'].value_counts().head(8)
product_counts.plot(kind='bar', color='lightcoral')
plt.title('Most Mentioned Products/Brands')
plt.xlabel('Product/Brand')
plt.ylabel('Mentions')
plt.xticks(rotation=45)
plt.subplot(2, 2, 4)
plt.scatter(results_df['positive_words'], results_df['negative_words'], 
           c=['green' if s == 'POSITIVE' else 'red' if s == 'NEGATIVE' else 'gray' 
              for s in results_df['sentiment']], alpha=0.7, s=100)
plt.xlabel('Positive Words Count')
plt.ylabel('Negative Words Count')
plt.title('Sentiment Analysis: Positive vs Negative Words')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('nlp_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== NER Visualization for Sample Review ===")
sample_review = reviews[0]
doc = nlp(sample_review)
displacy.render(doc, style='ent', jupyter=False)

html = displacy.render(doc, style='ent', page=True)
with open('ner_visualization.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"NER visualization saved as 'ner_visualization.html'")

print("\n=== Detailed Entity Analysis ===")
entity_summary = entity_df.groupby('Label').agg({'Entity': ['count', lambda x: ', '.join(list(x)[:5])]})
entity_summary.columns = ['Count', 'Examples']
print(entity_summary)

print("\n=== Brand-Specific Sentiment ===")
brand_sentiment = {}

for idx, row in results_df.iterrows():
    entities = row['entities']
    sentiment = row['sentiment']
    
    for entity, label in entities:
        if label in ['ORG', 'PRODUCT']:
            if entity not in brand_sentiment:
                brand_sentiment[entity] = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
            brand_sentiment[entity][sentiment] += 1

for brand, sentiments in list(brand_sentiment.items())[:10]:
    total = sum(sentiments.values())
    positive_pct = (sentiments['POSITIVE'] / total) * 100 if total > 0 else 0
    print(f"{brand}: {sentiments} (Positive: {positive_pct:.1f}%)")

print("\n=== NLP Analysis Complete ===")