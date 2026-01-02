# 📚 Text Summarization Tool - Quick Start Guide

## What You've Got

A complete text summarization tool with:
- ✅ Main summarization engine (`text_summarizer.py`)
- ✅ Interactive mode (`interactive_summarizer.py`)
- ✅ Demo script (`demo.py`)
- ✅ Comprehensive documentation (`README.md`)

## Quick Start (3 Steps)

### 1️⃣ Run the Demo
See the tool in action with sample articles:
```bash
python demo.py
```

### 2️⃣ Try Interactive Mode
Summarize your own text:
```bash
python interactive_summarizer.py
```

### 3️⃣ Use in Your Code
```python
from text_summarizer import TextSummarizer

summarizer = TextSummarizer()
summary = summarizer.summarize(your_text, num_sentences=3, method='hybrid')
print(summary)
```

## Summarization Methods Explained

### 🔹 Frequency-Based
- Counts how often words appear
- Selects sentences with most frequent important words
- **Best for:** General articles with clear main topics

### 🔹 TF-IDF
- Identifies unique and important terms
- Balances frequency with rarity
- **Best for:** Technical or specialized content

### 🔹 Position-Based
- Prioritizes first and last sentences
- Assumes key info is at beginning/end
- **Best for:** News articles, structured content

### 🔹 Hybrid (⭐ Recommended)
- Combines all three methods
- Weighted: 50% TF-IDF + 30% Frequency + 20% Position
- **Best for:** Most use cases, balanced results

## Example Usage

### Basic Summarization
```python
from text_summarizer import TextSummarizer

article = """
Your lengthy article text here...
Multiple sentences and paragraphs...
"""

summarizer = TextSummarizer()
summary = summarizer.summarize(article, num_sentences=3)
print(summary)
```

### With Statistics
```python
summary = summarizer.summarize(article, num_sentences=3, method='hybrid')
stats = summarizer.get_summary_stats(article, summary)

print(f"Original: {stats['original_words']} words")
print(f"Summary: {stats['summary_words']} words")
print(f"Saved: {stats['compression_ratio']}")
```

### Compare Methods
```python
for method in ['frequency', 'tfidf', 'position', 'hybrid']:
    summary = summarizer.summarize(article, num_sentences=3, method=method)
    print(f"\n{method.upper()}:\n{summary}\n")
```

## Tips for Best Results

1. **Choose the right number of sentences:**
   - Short articles (< 10 sentences): 2-3 sentences
   - Medium articles (10-20 sentences): 3-5 sentences
   - Long articles (> 20 sentences): 5-8 sentences

2. **Method selection:**
   - Start with 'hybrid' - it works well for most cases
   - Try 'tfidf' for technical/academic content
   - Use 'frequency' for simple, repetitive content
   - Use 'position' for news articles

3. **Input quality:**
   - Works best with well-structured text
   - Ensure proper sentence punctuation
   - Remove excessive formatting/special characters

## File Structure

```
project/
│
├── text_summarizer.py          # Main summarization engine
├── interactive_summarizer.py   # Interactive CLI tool
├── demo.py                      # Demonstration script
├── USAGE_GUIDE.md              # This file
└── requirements.txt            # Dependencies (none required!)
```

## Common Use Cases

### 📰 News Article Summarization
```python
news = "Long news article..."
summary = summarizer.summarize(news, num_sentences=3, method='position')
```

### 📖 Research Paper Abstract
```python
paper = "Long research paper..."
summary = summarizer.summarize(paper, num_sentences=5, method='tfidf')
```

### 📧 Email Summary
```python
email = "Long email thread..."
summary = summarizer.summarize(email, num_sentences=2, method='hybrid')
```

### 📝 Blog Post Summary
```python
blog = "Long blog post..."
summary = summarizer.summarize(blog, num_sentences=4, method='hybrid')
```

## Troubleshooting

**Q: Summary is too short/long?**
- Adjust the `num_sentences` parameter

**Q: Summary doesn't capture main points?**
- Try different methods (especially 'hybrid' or 'tfidf')
- Ensure input text is well-structured

**Q: Getting same sentences repeatedly?**
- Input text might be too short
- Try reducing `num_sentences`

**Q: Want to customize stop words?**
- Edit the `stop_words` set in `TextSummarizer.__init__()`

## Next Steps

1. ✅ Run `demo.py` to see examples
2. ✅ Try `interactive_summarizer.py` with your text
3. ✅ Integrate into your projects
4. ✅ Read `README.md` for technical details

## Need Help?

- Check `README.md` for detailed documentation
- Review the code comments in `text_summarizer.py`
- Experiment with different methods and parameters

---

**Happy Summarizing! 🚀**
