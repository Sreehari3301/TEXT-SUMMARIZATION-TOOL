"""
Interactive Text Summarization Tool
Allows users to input their own text and get summaries with different methods.
"""

from text_summarizer import TextSummarizer, print_separator, print_section_header


def get_multiline_input():
    """Get multiline text input from user."""
    print("\n📝 Enter or paste your text (press Ctrl+Z then Enter on Windows, or Ctrl+D on Unix when done):")
    print("-" * 80)
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return '\n'.join(lines)


def interactive_mode():
    """Run the summarizer in interactive mode."""
    summarizer = TextSummarizer()
    
    print("\n")
    print_separator('=', 80)
    print("  INTERACTIVE TEXT SUMMARIZATION TOOL")
    print_separator('=', 80)
    print("\n")
    
    while True:
        print("\n" + "="*80)
        print("OPTIONS:")
        print("  1. Summarize your own text")
        print("  2. Use sample article (AI)")
        print("  3. Use sample article (Climate Change)")
        print("  4. Exit")
        print("="*80)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '4':
            print("\n👋 Thank you for using the Text Summarization Tool!\n")
            break
        
        if choice == '1':
            text = get_multiline_input()
            if not text.strip():
                print("\n❌ No text entered. Please try again.")
                continue
        
        elif choice == '2':
            text = """
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
            print("\n📄 Using sample AI article...")
        
        elif choice == '3':
            text = """
            Climate change represents one of the most pressing challenges facing humanity in the 21st century.
            The Earth's average temperature has risen by approximately 1.1 degrees Celsius since the pre-industrial
            era, primarily due to human activities that release greenhouse gases into the atmosphere. Carbon dioxide
            emissions from burning fossil fuels for energy, transportation, and industrial processes are the main
            contributors to global warming. Deforestation further exacerbates the problem by reducing the planet's
            capacity to absorb carbon dioxide. The consequences of climate change are already visible around the world.
            Extreme weather events such as hurricanes, droughts, and heatwaves have become more frequent and intense.
            Rising sea levels threaten coastal communities and small island nations. Arctic ice is melting at an
            alarming rate, endangering polar ecosystems and contributing to further warming. Changes in precipitation
            patterns affect agriculture and water resources, potentially leading to food insecurity in vulnerable
            regions. Transitioning to renewable energy sources such as solar, wind, and hydroelectric power is 
            essential for reducing carbon emissions. International cooperation through agreements like the Paris 
            Climate Accord is necessary to coordinate global efforts.
            """
            print("\n📄 Using sample Climate Change article...")
        
        else:
            print("\n❌ Invalid choice. Please try again.")
            continue
        
        # Get summarization parameters
        print("\n" + "-"*80)
        try:
            num_sentences = int(input("Enter number of sentences for summary (default 3): ").strip() or "3")
        except ValueError:
            num_sentences = 3
            print("Using default: 3 sentences")
        
        print("\nAvailable methods:")
        print("  1. Frequency-based")
        print("  2. TF-IDF")
        print("  3. Position-based")
        print("  4. Hybrid (Recommended)")
        
        method_choice = input("\nSelect method (1-4, default 4): ").strip() or "4"
        
        method_map = {
            '1': 'frequency',
            '2': 'tfidf',
            '3': 'position',
            '4': 'hybrid'
        }
        
        method = method_map.get(method_choice, 'hybrid')
        
        # Generate summary
        print("\n" + "="*80)
        print("🔄 Processing...")
        print("="*80)
        
        try:
            summary = summarizer.summarize(text, num_sentences=num_sentences, method=method)
            stats = summarizer.get_summary_stats(text, summary)
            
            print(f"\n✨ SUMMARY ({method.upper()} method):")
            print("-"*80)
            print(summary)
            print("-"*80)
            
            print(f"\n📊 STATISTICS:")
            print(f"   • Original: {stats['original_words']} words, {stats['original_sentences']} sentences")
            print(f"   • Summary: {stats['summary_words']} words, {stats['summary_sentences']} sentences")
            print(f"   • Compression Ratio: {stats['compression_ratio']}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue
        
        # Ask if user wants to try another method
        another = input("\n\nWould you like to try a different method on the same text? (y/n): ").strip().lower()
        
        while another == 'y':
            print("\nAvailable methods:")
            print("  1. Frequency-based")
            print("  2. TF-IDF")
            print("  3. Position-based")
            print("  4. Hybrid")
            
            method_choice = input("\nSelect method (1-4): ").strip()
            method = method_map.get(method_choice, 'hybrid')
            
            try:
                summary = summarizer.summarize(text, num_sentences=num_sentences, method=method)
                stats = summarizer.get_summary_stats(text, summary)
                
                print(f"\n✨ SUMMARY ({method.upper()} method):")
                print("-"*80)
                print(summary)
                print("-"*80)
                
                print(f"\n📊 STATISTICS:")
                print(f"   • Original: {stats['original_words']} words, {stats['original_sentences']} sentences")
                print(f"   • Summary: {stats['summary_words']} words, {stats['summary_sentences']} sentences")
                print(f"   • Compression Ratio: {stats['compression_ratio']}")
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
            
            another = input("\n\nTry another method? (y/n): ").strip().lower()


if __name__ == "__main__":
    interactive_mode()
