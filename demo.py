"""
Simple demonstration of the Text Summarization Tool
Shows clear before/after examples with all methods
"""

from text_summarizer import TextSummarizer


def demo():
    """Run a simple, clear demonstration."""
    
    summarizer = TextSummarizer()
    
    # Sample article about technology
    article = """
    Artificial intelligence has revolutionized the way we interact with technology in the modern world. 
    Machine learning algorithms have become increasingly sophisticated, enabling computers to learn from 
    data and make predictions without being explicitly programmed. Deep learning, a subset of machine 
    learning, uses neural networks with multiple layers to process complex patterns in large datasets. 
    These technologies have found applications in various fields including healthcare, finance, 
    transportation, and entertainment. In healthcare, AI systems can analyze medical images to detect 
    diseases with remarkable accuracy, sometimes surpassing human experts. Financial institutions use 
    machine learning algorithms to detect fraudulent transactions and assess credit risk. Self-driving 
    cars rely on deep learning models to interpret sensor data and navigate safely through traffic. 
    Natural language processing, another branch of AI, has enabled virtual assistants like Siri and 
    Alexa to understand and respond to human speech. Despite these advances, AI still faces significant 
    challenges including bias in training data, lack of transparency in decision-making processes, and 
    concerns about privacy and security. Researchers are working on developing more ethical and 
    explainable AI systems that can be trusted in critical applications.
    """
    
    print("\n" + "="*100)
    print(" "*35 + "TEXT SUMMARIZATION TOOL")
    print(" "*25 + "Natural Language Processing Demonstration")
    print("="*100)
    
    print("\n📄 ORIGINAL ARTICLE:")
    print("-"*100)
    print(article.strip())
    print("-"*100)
    
    # Get original stats
    sentences = summarizer.tokenize_sentences(article)
    words = article.split()
    print(f"\n📊 Original Length: {len(words)} words, {len(sentences)} sentences")
    
    print("\n" + "="*100)
    print(" "*30 + "SUMMARIZATION RESULTS (3 sentences)")
    print("="*100)
    
    methods = [
        ('frequency', 'Frequency-Based Analysis'),
        ('tfidf', 'TF-IDF (Term Frequency-Inverse Document Frequency)'),
        ('position', 'Position-Based Scoring'),
        ('hybrid', 'Hybrid Approach (Recommended)')
    ]
    
    for method_key, method_name in methods:
        print(f"\n\n🔍 METHOD: {method_name}")
        print("-"*100)
        
        summary = summarizer.summarize(article, num_sentences=3, method=method_key)
        stats = summarizer.get_summary_stats(article, summary)
        
        print(f"\n✨ SUMMARY:")
        print(summary)
        
        print(f"\n📊 STATISTICS:")
        print(f"   • Summary Length: {stats['summary_words']} words, {stats['summary_sentences']} sentences")
        print(f"   • Compression Ratio: {stats['compression_ratio']}")
        print(f"   • Words Saved: {stats['original_words'] - stats['summary_words']} words")
    
    print("\n\n" + "="*100)
    print(" "*40 + "COMPARISON EXAMPLE")
    print("="*100)
    
    # Show different summary lengths
    print("\n📝 Same article with different summary lengths (using HYBRID method):\n")
    
    for num_sent in [2, 3, 5]:
        summary = summarizer.summarize(article, num_sentences=num_sent, method='hybrid')
        stats = summarizer.get_summary_stats(article, summary)
        
        print(f"\n{num_sent}-Sentence Summary ({stats['compression_ratio']} compression):")
        print("-"*100)
        print(summary)
    
    print("\n\n" + "="*100)
    print(" "*42 + "✅ DEMO COMPLETE")
    print("="*100)
    print("\n💡 TIP: Run 'python interactive_summarizer.py' to try with your own text!\n")


if __name__ == "__main__":
    demo()
