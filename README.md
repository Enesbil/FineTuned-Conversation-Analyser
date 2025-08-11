# Fine-Tuned Sentiment Analyzer

A comprehensive conversation analysis tool designed for marriage/wedding organizations to analyze customer interactions using OpenAI's GPT models. This project enables both automated analysis and manual labeling of conversations to evaluate bot performance and customer sentiment.

## Features

- **Automated Conversation Analysis**: Uses OpenAI's GPT models to analyze conversations and extract:
  - Overall customer sentiment (positive, neutral, negative)
  - Bot understanding quality (good, acceptable, poor)
  - Bot performance assessment (good, acceptable, poor)
  - Response completeness (whether bot answered the last message)
  - Conversation categorization

- **Manual Labeling Interface**: Beautiful web-based tool for creating ground truth labels
  - Interactive conversation viewer
  - Progress tracking and navigation
  - Export/import functionality for labels
  - Keyboard shortcuts for efficient labeling

- **Fine-Tuning Support**: Prepare data for OpenAI fine-tuning to improve analysis accuracy
  - JSONL format validation
  - Data quality checks
  - Ground truth integration

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fine-tuned-sentiment-analyser.git
cd fine-tuned-sentiment-analyser

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup OpenAI API

Create a `secrets.env` file in the project root:

```bash
cp secrets.env.example secrets.env
```

Edit `secrets.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Prepare Your Data

The tool expects conversation data in a specific JSON format. Use the provided preprocessing script:

```python
# Update process_conversations.py with your input file path
input_file = "your_conversations.json"
output_file = "cleaned_conversations.json"

python process_conversations.py
```

### 4. Analyze Conversations

Run the main analyzer:

```bash
python conversation_analyzer.py
```

Follow the prompts to select how many conversations to analyze.

## Usage Guide

### Conversation Analysis

The main analysis script (`conversation_analyzer.py`) provides several options:

- **Analyze specific number**: `10` (analyzes first 10 conversations)
- **Analyze range**: `11-50` (analyzes conversations 11 through 50)
- **Analyze all**: `all` or `a` (analyzes all conversations)

Results are saved to `classification_results.json` with detailed analysis for each conversation.

### Manual Labeling

1. Open `conversation_labeler.html` in your web browser
2. Load your conversation JSON file using the "Load Conversations" button
3. Navigate through conversations and provide manual labels
4. Export your ground truth labels when complete

**Keyboard Shortcuts:**
- `Ctrl + ←`: Previous conversation
- `Ctrl + →`: Next conversation
- `Ctrl + S`: Save current labels

### Data Processing

Use `process_conversations.py` to convert raw conversation data to the required format:

```python
def process_conversations_file(input_file, output_file, max_conversations=100):
    # Processes conversations and creates cleaned format
```

Expected input format:
```json
[
  {
    "conversation_id": "unique_id",
    "messages": [
      {
        "id": "message_id",
        "type": "TEXT",
        "sender_id": "sender_identifier",
        "content": {"text": "message content"},
        "created_at": "timestamp",
        "is_internal": false
      }
    ]
  }
]
```

### Fine-Tuning Preparation

1. Create manual ground truth using the labeling interface
2. Generate fine-tuning data (implement your own script based on ground truth)
3. Validate JSONL format:

```bash
python validate_jsonl.py
```

4. Upload to OpenAI and update model ID in `conversation_analyzer.py` line 174

## Configuration

### Analysis Categories

The tool categorizes conversations into predefined categories relevant to wedding/marriage organizations:

- Düğün Mekanları (Wedding Venues)
- Düğün Organizasyon (Wedding Organization)
- Kına Gecesi (Henna Night)
- Nişan ve Söz (Engagement)
- Mezuniyet ve Balo (Graduation & Prom)
- Doğum Günü & Baby Shower
- Düğün Fotoğrafçıları (Wedding Photographers)
- And more...

### Customization

To adapt for your domain:

1. **Update categories** in `conversation_analyzer.py` (lines 58-64)
2. **Modify analysis prompt** for your specific use case (lines 84-129)
3. **Adjust bot identification** in `process_conversations.py` (line 64)

## File Structure

```
fine-tuned-sentiment-analyser/
├── conversation_analyzer.py      # Main analysis script
├── conversation_labeler.html     # Manual labeling interface
├── process_conversations.py      # Data preprocessing
├── validate_jsonl.py            # JSONL validation for fine-tuning
├── requirements.txt             # Python dependencies
├── secrets.env.example          # Environment variables template
├── fine_tuning.jsonl           # Fine-tuning data (placeholder)
└── example-last-500-conversations.json  # Example data format
```

## Output Format

### Analysis Results

Each analyzed conversation produces:

```json
{
  "conversation_id": "unique_identifier",
  "llm_classification": {
    "overall_sentiment": "positive|neutral|negative",
    "bot_understanding": "good|acceptable|poor",
    "bot_performance": "good|acceptable|poor", 
    "bot_answered": true|false,
    "categories": ["Category1", "Category2"],
    "to_improve_understanding": "explanation or null",
    "to_improve_performance": "explanation or null"
  }
}
```

### Manual Labels Export

```json
{
  "exported_at": "2024-01-01T00:00:00.000Z",
  "total_labeled": 50,
  "labels": [
    {
      "conversation_id": "conv_123",
      "ground_truth": {
        "overall_sentiment": "positive",
        "bot_understanding": "good",
        "bot_performance": "acceptable",
        "bot_answered": true
      }
    }
  ]
}
```

## API Usage

### Basic Analysis

```python
from conversation_analyzer import ConversationAnalyzer

# Initialize
analyzer = ConversationAnalyzer()

# Load conversations
conversations = analyzer.load_conversations("your_file.json")

# Analyze specific range
results = analyzer.analyze_conversations(conversations, start=0, end=10)

# Save results
analyzer.save_results(results, "output.json")
```

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Dependencies

- **openai**: For GPT model integration
- **tqdm**: Progress bars during analysis
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is correctly set in `secrets.env`
2. **JSON Format Error**: Validate your input data format matches the expected structure
3. **Rate Limiting**: The tool includes automatic delays to prevent API rate limits
4. **Memory Issues**: For large datasets, process in smaller batches

### Performance Tips

- Use ranges (e.g., `1-100`) for large datasets
- Monitor API usage and costs
- Consider fine-tuning for better accuracy on your specific domain

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for marriage/wedding organization customer service analysis
- Uses OpenAI's GPT models for intelligent conversation analysis
- Inspired by the need for automated customer interaction quality assessment

## Support

For questions, issues, or contributions, please:

1. Check existing issues in the repository
2. Create a new issue with detailed information
3. Provide sample data and error messages when applicable

---

**Note**: This tool is designed for Turkish wedding/marriage organization conversations but can be adapted for other domains by modifying the categories and analysis prompts.
