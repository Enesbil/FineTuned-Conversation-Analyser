#!/usr/bin/env python3
"""
Conversation Analysis Script for Marriage/Organizations Firm
Analyzes customer chat conversations using OpenAI GPT-4.1 with structured outputs.
"""

import json
import os
import sys
from typing import List, Dict, Any, Optional
import time
from pathlib import Path

import openai
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv('secrets.env')

class ConversationAnalyzer:
    def __init__(self):
        """Initialize the conversation analyzer with OpenAI client."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in secrets.env file")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Define the JSON schema for structured outputs
        self.response_schema = {
            "type": "object",
            "properties": {
                "overall_sentiment": {
                    "type": "string",
                    "enum": ["positive", "neutral", "negative"],
                    "description": "User's overall sentiment: positive, neutral, or negative"
                },
                "bot_understanding": {
                    "type": "string", 
                    "enum": ["poor", "acceptable", "good"],
                    "description": "How well the bot understood the user's request"
                },
                "bot_performance": {
                    "type": "string", 
                    "enum": ["poor", "acceptable", "good"],
                    "description": "How well the bot performed in finding relevant options"
                },
                "categories": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Düğün Mekanları", "Düğün Organizasyon", "Kına Gecesi", "Nişan ve Söz",
                            "Mezuniyet ve Balo", "Doğum Günü & Baby Shower", "Düğün Fotoğrafçıları", 
                            "Catering Firmaları", "Gelinlik ve Moda Evleri", "Abiye ve Damatlık",
                            "Orkestra & DJ", "Saç ve Makyaj", "Davetiye ve Hediyelikler", "Pasta",
                            "Alyans ve Takı", "Balayı", "Diğer"
                        ]
                    },
                    "minItems": 1,
                    "maxItems": 3,
                    "description": "Up to 3 relevant categories from the predefined list"
                },
                "to_improve_understanding": {
                    "type": ["string", "null"],
                    "description": "Explanation of understanding issues in Turkish (null if good)"
                },
                "to_improve_performance": {
                    "type": ["string", "null"],
                    "description": "Explanation of performance issues in Turkish (null if good)"
                }
            },
            "required": ["overall_sentiment", "bot_understanding", "bot_performance", "categories", "to_improve_understanding", "to_improve_performance"],
            "additionalProperties": False
        }
        
        # Define the analysis prompt
        self.analysis_prompt = """
You are an expert conversation analyst for a marriage/wedding organization firm. 

Analyze the following customer conversation transcript and return a JSON object with your analysis.

**Analysis Guidelines:**

1. **overall_sentiment**: Determine the user's overall sentiment throughout the conversation:
   - "positive": User is satisfied, engaged, and shows positive emotions
   - "neutral": User is matter-of-fact, neither clearly positive nor negative
   - "negative": User is frustrated, dissatisfied, or shows negative emotions
   Note: If a user leaves the chat abruptly without getting their intended result, this may indicate negative sentiment.

2. **bot_understanding**: Evaluate how well the bot understood what the user is asking. Not how well it was able to adress the request, just how well it understood.
   - "good": The bot perfectly understood the user's request/intent
   - "acceptable": The bot understood the basic request but missed some nuances or details
   - "poor": The bot fundamentally misunderstood the user's intent

3. **bot_performance**: Evaluate how well the bot performed in finding reasonable options (assuming the request was reasonable. For example if the user might have requested a wedding venue in a large area with a reasonable budget, the bot needs to be able to find a venue that matches the user's request. IMPORTANT: Do consider the possibility that the user is making an unreasonable request (e.g. low budget per attendee leading it to not be able to find venues) in those cases, if the bot fails to fulfill a request it may not be a performance issue but this consideration should not affect your judgment for the sentiment section):
   - "good": The bot found highly relevant and suitable options
   - "acceptable": The bot found some relevant options but could have done better
   - "poor": The bot failed to find reasonable options or provided irrelevant results

4. **categories**: Select 1-3 most relevant categories from the predefined list. If no category fits well, use ["Diğer"].

5. **to_improve_understanding**: Provide a preferably concise 1-2 sentence explanation of understanding issues:
   - If bot_understanding is "good": leave this field as null
   - If bot_understanding is "acceptable" or "poor": explain in one line what the bot misunderstood. Give the explanation in Turkish.

6. **to_improve_performance**: Provide a preferably concise 1-2 sentence explanation of performance issues:
   - If bot_performance is "good": leave this field as null
   - If bot_performance is "acceptable" or "poor": explain in one line how the bot's performance could be improved. Give the explanation in Turkish.

**Predefined Categories:**
["Düğün Mekanları", "Düğün Organizasyon", "Kına Gecesi", "Nişan ve Söz", "Mezuniyet ve Balo", "Doğum Günü & Baby Shower", "Düğün Fotoğrafçıları", "Catering Firmaları", "Gelinlik ve Moda Evleri", "Abiye ve Damatlık", "Orkestra & DJ", "Saç ve Makyaj", "Davetiye ve Hediyelikler", "Pasta", "Alyans ve Takı", "Balayı", "Diğer"]

Note: You may observe that the AI asks a few questions in the beginning without a response from the user. The few initial questions generally do get answered by the user even if not reflected on the transcript and the bot thus has that context in the rest of the conversation.

**Conversation Transcript:**
"""

    def load_conversations(self, file_path: str) -> List[Dict[str, Any]]:
        """Load conversations from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            print(f"Loaded {len(conversations)} conversations from {file_path}")
            return conversations
        
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{file_path}': {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading conversations: {e}")
            sys.exit(1)

    def analyze_conversation(self, conversation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a single conversation using OpenAI API with structured outputs."""
        try:
            conversation_id = conversation['metadata']['conversation_id']
            
            # Create properly formatted transcript from message list
            messages = conversation['transcript_list_of_messages']
            formatted_transcript = []
            
            for msg in messages:
                sender = msg['sender']
                text = msg['text']
                formatted_line = f"{sender}: {text}"
                formatted_transcript.append(formatted_line)
            
            cleaned_transcript = '\n\n'.join(formatted_transcript)
            
            # Prepare messages
            system_message = self.analysis_prompt
            user_message = f"Analyze the following conversation transcript:\n\n{cleaned_transcript}"
            
            
            # Make API call with structured outputs
            response = self.client.chat.completions.create(
                model="gpt-5",  # Placeholder as requested
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "conversation_analysis",
                        "schema": self.response_schema,
                        "strict": True
                    }
                },

            )
            
            # Parse the response
            analysis_result = json.loads(response.choices[0].message.content)
            
            return {
                "conversation_id": conversation_id,
                "llm_classification": analysis_result
            }
            
        except openai.APIError as e:
            print(f"OpenAI API error for conversation {conversation_id}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error for conversation {conversation_id}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error analyzing conversation {conversation_id}: {e}")
            return None

    def analyze_conversations(self, conversations: List[Dict[str, Any]], start: Optional[int] = None, end: Optional[int] = None) -> List[Dict[str, Any]]:
        """Analyze multiple conversations with progress tracking."""
        if start is not None and end is not None:
            conversations = conversations[start:end]
            print(f"Analyzing conversations {start+1}-{end} ({len(conversations)} total)...")
        else:
            print(f"Analyzing all {len(conversations)} conversations...")
        
        results = []
        failed_count = 0
        
        # Process conversations with progress bar
        for conversation in tqdm(conversations, desc="Analyzing conversations", unit="conv"):
            result = self.analyze_conversation(conversation)
            
            if result:
                results.append(result)
            else:
                failed_count += 1
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
        
        print(f"Successfully analyzed: {len(results)} conversations")
        if failed_count > 0:
            print(f"Failed to analyze: {failed_count} conversations")
        
        return results

    def save_results(self, results: List[Dict[str, Any]], output_file: str = "classification_results.json"):
        """Save analysis results to JSON file (appending to existing results)."""
        try:
            existing_results = []
            
            # Load existing results if file exists
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        existing_results = json.load(f)
                    print(f"Loaded {len(existing_results)} existing results")
                except (json.JSONDecodeError, Exception):
                    print("Existing file corrupted, starting fresh")
                    existing_results = []
            
            # Append new results
            all_results = existing_results + results
            
            # Save combined results
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            
            print(f"Results appended to '{output_file}'")
            print(f"New classifications: {len(results)}")
            print(f"Total classifications: {len(all_results)}")
            
            # Print summary statistics for new results only
            if results:
                self.print_summary_stats(results)
                
        except Exception as e:
            print(f"Error saving results: {e}")

    def print_summary_stats(self, results: List[Dict[str, Any]]):
        """Print summary statistics of the analysis results."""
        sentiments = [r['llm_classification']['overall_sentiment'] for r in results]
        bot_understanding = [r['llm_classification']['bot_understanding'] for r in results]
        bot_performance = [r['llm_classification']['bot_performance'] for r in results]
        
        print("\nAnalysis Summary:")
        print("─" * 50)
        
        # Sentiment distribution
        sentiment_counts = {s: sentiments.count(s) for s in ['positive', 'neutral', 'negative']}
        print("Sentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  • {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Bot understanding distribution
        understanding_counts = {p: bot_understanding.count(p) for p in ['good', 'acceptable', 'poor']}
        print("\nBot Understanding Distribution:")
        for understanding, count in understanding_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  • {understanding.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Bot performance distribution
        performance_counts = {p: bot_performance.count(p) for p in ['good', 'acceptable', 'poor']}
        print("\nBot Performance Distribution:")
        for performance, count in performance_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  • {performance.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Most common categories
        all_categories = []
        for result in results:
            all_categories.extend(result['llm_classification']['categories'])
        
        category_counts = {}
        for category in all_categories:
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print("\nTop 5 Categories:")
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for category, count in sorted_categories:
            percentage = (count / len(all_categories)) * 100
            print(f"  • {category}: {count} ({percentage:.1f}%)")


def get_user_input():
    """Get user input for conversations to analyze."""
    try:
        user_input = input("\nEnter conversations to analyze (examples: '10', 'all', '11-50'): ").strip()
        
        if user_input.lower() in ['all', 'a']:
            return None, None
        
        # Check for range format (e.g., "11-50")
        if '-' in user_input:
            try:
                start, end = map(int, user_input.split('-'))
                if start <= 0 or end <= 0 or start > end:
                    print("Please enter a valid range (e.g., '11-50').")
                    return get_user_input()
                return start - 1, end  # Convert to 0-based indexing
            except ValueError:
                print("Invalid range format. Use format like '11-50'.")
                return get_user_input()
        
        # Single number
        limit = int(user_input)
        if limit <= 0:
            print("Please enter a positive number.")
            return get_user_input()
        
        return 0, limit  # From start to limit
        
    except ValueError:
        print("Please enter a valid number, range, or 'all'.")
        return get_user_input()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


def main():
    """Main function to run the conversation analysis."""
    print("Conversation Analysis Tool for Marriage/Organizations Firm")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = ConversationAnalyzer()
        
        # Load conversations
        conversations = analyzer.load_conversations("cleaned_conversations.json")
        
        # Get user input for conversations to analyze
        start, end = get_user_input()
        
        # Confirm before proceeding
        if start is not None and end is not None:
            print(f"\nStarting analysis of conversations {start+1}-{end}...")
        else:
            print(f"\nStarting analysis of all {len(conversations)} conversations...")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return
        
        # Analyze conversations
        results = analyzer.analyze_conversations(conversations, start, end)
        
        if not results:
            print("No conversations were successfully analyzed.")
            return
        
        # Save results
        analyzer.save_results(results)
        
        print("\nAnalysis completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
