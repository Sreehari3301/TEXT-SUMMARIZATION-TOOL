"""
Text Summarization Tool
A comprehensive NLP-based tool for summarizing lengthy articles using multiple techniques.
"""

import re
import heapq
from collections import defaultdict
import math


class TextSummarizer:
    """
    A text summarization tool using extractive summarization techniques.
    Implements TF-IDF and frequency-based approaches.
    """
    
    def __init__(self):
        self.stop_words = set([
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
            'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
            'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
            'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
            's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
        ])
    
    def preprocess_text(self, text):
        """Clean and preprocess the input text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep sentence structure
        text = re.sub(r'[^\w\s.!?]', '', text)
        return text.strip()
    
    def tokenize_sentences(self, text):
        """Split text into sentences."""
        # Simple sentence tokenization
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def tokenize_words(self, text):
        """Split text into words and remove stop words."""
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in self.stop_words and len(word) > 2]
    
    def calculate_word_frequencies(self, sentences):
        """Calculate word frequencies across all sentences."""
        word_freq = defaultdict(int)
        
        for sentence in sentences:
            words = self.tokenize_words(sentence)
            for word in words:
                word_freq[word] += 1
        
        # Normalize frequencies
        if word_freq:
            max_freq = max(word_freq.values())
            for word in word_freq:
                word_freq[word] = word_freq[word] / max_freq
        
        return word_freq
    
    def calculate_tfidf(self, sentences):
        """Calculate TF-IDF scores for words."""
        # Calculate term frequency for each sentence
        tf_matrix = []
        for sentence in sentences:
            words = self.tokenize_words(sentence)
            word_count = defaultdict(int)
            for word in words:
                word_count[word] += 1
            
            # Normalize by sentence length
            total_words = len(words)
            if total_words > 0:
                for word in word_count:
                    word_count[word] = word_count[word] / total_words
            
            tf_matrix.append(word_count)
        
        # Calculate inverse document frequency
        idf = defaultdict(float)
        total_sentences = len(sentences)
        
        for word in set(word for sentence in tf_matrix for word in sentence):
            doc_count = sum(1 for sentence in tf_matrix if word in sentence)
            idf[word] = math.log(total_sentences / (doc_count + 1))
        
        # Calculate TF-IDF
        tfidf_matrix = []
        for tf in tf_matrix:
            tfidf = {word: tf[word] * idf[word] for word in tf}
            tfidf_matrix.append(tfidf)
        
        return tfidf_matrix
    
    def score_sentences_frequency(self, sentences, word_freq):
        """Score sentences based on word frequency."""
        sentence_scores = {}
        
        for i, sentence in enumerate(sentences):
            words = self.tokenize_words(sentence)
            score = 0
            
            for word in words:
                score += word_freq.get(word, 0)
            
            # Normalize by sentence length to avoid bias towards longer sentences
            if len(words) > 0:
                sentence_scores[i] = score / len(words)
            else:
                sentence_scores[i] = 0
        
        return sentence_scores
    
    def score_sentences_tfidf(self, sentences, tfidf_matrix):
        """Score sentences based on TF-IDF."""
        sentence_scores = {}
        
        for i, tfidf in enumerate(tfidf_matrix):
            score = sum(tfidf.values())
            sentence_scores[i] = score
        
        return sentence_scores
    
    def score_sentences_position(self, sentences):
        """Score sentences based on their position (first and last sentences are important)."""
        sentence_scores = {}
        total = len(sentences)
        
        for i in range(total):
            if i == 0:
                sentence_scores[i] = 1.0  # First sentence is very important
            elif i == total - 1:
                sentence_scores[i] = 0.8  # Last sentence is important
            else:
                # Middle sentences get decreasing scores
                sentence_scores[i] = 0.5
        
        return sentence_scores
    
    def combine_scores(self, *score_dicts, weights=None):
        """Combine multiple scoring methods with optional weights."""
        if weights is None:
            weights = [1.0] * len(score_dicts)
        
        combined = defaultdict(float)
        
        for score_dict, weight in zip(score_dicts, weights):
            for key, value in score_dict.items():
                combined[key] += value * weight
        
        return combined
    
    def summarize(self, text, num_sentences=3, method='hybrid'):
        """
        Summarize the input text.
        
        Args:
            text (str): The input text to summarize
            num_sentences (int): Number of sentences in the summary
            method (str): Summarization method - 'frequency', 'tfidf', 'position', or 'hybrid'
        
        Returns:
            str: The summarized text
        """
        # Preprocess
        text = self.preprocess_text(text)
        sentences = self.tokenize_sentences(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Calculate scores based on method
        if method == 'frequency':
            word_freq = self.calculate_word_frequencies(sentences)
            scores = self.score_sentences_frequency(sentences, word_freq)
        
        elif method == 'tfidf':
            tfidf_matrix = self.calculate_tfidf(sentences)
            scores = self.score_sentences_tfidf(sentences, tfidf_matrix)
        
        elif method == 'position':
            scores = self.score_sentences_position(sentences)
        
        elif method == 'hybrid':
            # Combine all methods
            word_freq = self.calculate_word_frequencies(sentences)
            tfidf_matrix = self.calculate_tfidf(sentences)
            
            freq_scores = self.score_sentences_frequency(sentences, word_freq)
            tfidf_scores = self.score_sentences_tfidf(sentences, tfidf_matrix)
            position_scores = self.score_sentences_position(sentences)
            
            # Combine with weights: TF-IDF (0.5), Frequency (0.3), Position (0.2)
            scores = self.combine_scores(
                tfidf_scores, freq_scores, position_scores,
                weights=[0.5, 0.3, 0.2]
            )
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Get top sentences
        top_sentence_indices = heapq.nlargest(
            num_sentences, scores.keys(), key=lambda k: scores[k]
        )
        
        # Sort by original order to maintain coherence
        top_sentence_indices.sort()
        
        # Build summary
        summary = ' '.join([sentences[i] for i in top_sentence_indices])
        
        return summary
    
    def get_summary_stats(self, original_text, summary):
        """Get statistics about the summarization."""
        original_words = len(original_text.split())
        summary_words = len(summary.split())
        original_sentences = len(self.tokenize_sentences(original_text))
        summary_sentences = len(self.tokenize_sentences(summary))
        
        compression_ratio = (1 - summary_words / original_words) * 100 if original_words > 0 else 0
        
        return {
            'original_words': original_words,
            'summary_words': summary_words,
            'original_sentences': original_sentences,
            'summary_sentences': summary_sentences,
            'compression_ratio': f"{compression_ratio:.1f}%"
        }


def print_separator(char='=', length=80):
    """Print a separator line."""
    print(char * length)


def print_section_header(title):
    """Print a formatted section header."""
    print_separator()
    print(f"  {title}")
    print_separator()


def main():
    """Main function demonstrating the text summarization tool."""
    
    # Sample lengthy article
    sample_article = """
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
    explainable AI systems that can be trusted in critical applications. The future of AI holds immense 
    potential for solving complex problems and improving human lives, but it also requires careful 
    consideration of its societal impacts. As AI continues to evolve, it is crucial that we develop 
    appropriate regulations and guidelines to ensure its responsible development and deployment. 
    Education and public awareness about AI technologies are essential for preparing society for an 
    AI-driven future. Collaboration between technologists, policymakers, ethicists, and the public 
    will be key to harnessing the benefits of AI while mitigating its risks.
    """
    
    # Another sample article about climate change
    climate_article = """
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
    regions. Biodiversity is under threat as species struggle to adapt to rapidly changing habitats. The
    scientific consensus is clear that immediate action is needed to limit global warming to 1.5 degrees
    Celsius above pre-industrial levels to avoid catastrophic consequences. Transitioning to renewable
    energy sources such as solar, wind, and hydroelectric power is essential for reducing carbon emissions.
    Improving energy efficiency in buildings, transportation, and industry can significantly decrease our
    carbon footprint. Protecting and restoring forests, wetlands, and other natural carbon sinks is crucial
    for absorbing atmospheric carbon dioxide. Individual actions such as reducing consumption, choosing
    sustainable products, and advocating for climate policies also play an important role. International
    cooperation through agreements like the Paris Climate Accord is necessary to coordinate global efforts.
    While the challenge is daunting, technological innovations and growing public awareness offer hope for
    a sustainable future.
    """
    
    # Initialize the summarizer
    summarizer = TextSummarizer()
    
    print("\n")
    print_section_header("TEXT SUMMARIZATION TOOL - NLP DEMONSTRATION")
    print("\n")
    
    # Example 1: AI Article with different methods
    print_section_header("EXAMPLE 1: Artificial Intelligence Article")
    print("\n📄 ORIGINAL TEXT:")
    print(f"\n{sample_article.strip()}\n")
    
    methods = ['frequency', 'tfidf', 'position', 'hybrid']
    
    for method in methods:
        print(f"\n🔍 METHOD: {method.upper()}")
        print("-" * 80)
        
        summary = summarizer.summarize(sample_article, num_sentences=3, method=method)
        stats = summarizer.get_summary_stats(sample_article, summary)
        
        print(f"\n✨ SUMMARY:\n{summary}\n")
        print(f"📊 STATISTICS:")
        print(f"   • Original: {stats['original_words']} words, {stats['original_sentences']} sentences")
        print(f"   • Summary: {stats['summary_words']} words, {stats['summary_sentences']} sentences")
        print(f"   • Compression: {stats['compression_ratio']}")
        print()
    
    # Example 2: Climate Change Article
    print("\n")
    print_section_header("EXAMPLE 2: Climate Change Article")
    print("\n📄 ORIGINAL TEXT:")
    print(f"\n{climate_article.strip()}\n")
    
    print(f"\n🔍 METHOD: HYBRID (Best Results)")
    print("-" * 80)
    
    summary = summarizer.summarize(climate_article, num_sentences=4, method='hybrid')
    stats = summarizer.get_summary_stats(climate_article, summary)
    
    print(f"\n✨ SUMMARY:\n{summary}\n")
    print(f"📊 STATISTICS:")
    print(f"   • Original: {stats['original_words']} words, {stats['original_sentences']} sentences")
    print(f"   • Summary: {stats['summary_words']} words, {stats['summary_sentences']} sentences")
    print(f"   • Compression: {stats['compression_ratio']}")
    
    # Example 3: Custom input demonstration
    print("\n")
    print_section_header("EXAMPLE 3: Custom Text Summarization")
    
    custom_text = """
    The Internet of Things (IoT) refers to the network of physical devices embedded with sensors, 
    software, and connectivity that enables them to collect and exchange data. Smart home devices 
    like thermostats, security cameras, and lighting systems can be controlled remotely through 
    smartphones. In industrial settings, IoT sensors monitor equipment performance and predict 
    maintenance needs, reducing downtime and costs. Wearable fitness trackers collect health data 
    to help users monitor their physical activity and vital signs. Smart cities use IoT technology 
    to optimize traffic flow, manage energy consumption, and improve public services. However, the 
    proliferation of connected devices raises concerns about data privacy and cybersecurity. As more 
    devices come online, the risk of hacking and data breaches increases. Standardization and robust 
    security protocols are essential for the safe and effective deployment of IoT technologies.
    """
    
    print(f"\n📄 ORIGINAL TEXT:\n{custom_text.strip()}\n")
    
    summary = summarizer.summarize(custom_text, num_sentences=2, method='hybrid')
    stats = summarizer.get_summary_stats(custom_text, summary)
    
    print(f"\n✨ SUMMARY:\n{summary}\n")
    print(f"📊 STATISTICS:")
    print(f"   • Original: {stats['original_words']} words, {stats['original_sentences']} sentences")
    print(f"   • Summary: {stats['summary_words']} words, {stats['summary_sentences']} sentences")
    print(f"   • Compression: {stats['compression_ratio']}")
    
    print("\n")
    print_separator()
    print("  ✅ DEMONSTRATION COMPLETE")
    print_separator()
    print("\n")


if __name__ == "__main__":
    main()
