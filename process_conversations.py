#!/usr/bin/env python3
"""
Process conversation data from JSON file and create cleaned output for sentiment analysis.
"""

import json
import re
from typing import Dict, List, Any, Optional


def decode_unicode_escapes(text: str) -> str:
    """Decode Unicode escape sequences to actual characters."""
    try:
        return text.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        # Fallback: try direct decode
        try:
            return text.encode().decode('unicode_escape')
        except:
            return text


def clean_text(text: str) -> str:
    """Clean text by removing markdown, decoding Unicode, and trimming whitespace."""
    if not text:
        return ""
    
    # Decode Unicode escape sequences
    text = decode_unicode_escapes(text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'__(.*?)__', r'\1', text)      # Bold underline
    text = re.sub(r'_(.*?)_', r'\1', text)        # Italic underline
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def process_conversation(conv_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process a single conversation and return cleaned format.
    Returns None if conversation has no valid messages.
    """
    conversation_id = conv_data.get("conversation_id", "")
    messages = conv_data.get("messages", [])
    
    # Filter for TEXT messages that are not internal
    valid_messages = []
    for msg in messages:
        if (msg.get("type") == "TEXT" and 
            msg.get("is_internal", False) is False and
            msg.get("content", {}).get("text")):
            valid_messages.append(msg)
    
    if not valid_messages:
        return None
    
    # Process messages and determine sender labels
    processed_messages = []
    bot_sender_id = "bf17272dc3f0"  # Known bot ID
    
    for msg in valid_messages:
        sender_id = msg.get("sender_id")
        text = msg.get("content", {}).get("text", "")
        
        if not text or sender_id is None:
            continue
            
        # Determine sender label
        if sender_id == bot_sender_id:
            sender = "Bot"
        else:
            sender = "User"
        
        processed_messages.append({
            "message_id": msg.get("id", ""),
            "sender": sender,
            "text": clean_text(text),
            "timestamp": msg.get("created_at", "")
        })
    
    if not processed_messages:
        return None
    
    # Build transcript_full_text
    transcript_lines = []
    for msg in processed_messages:
        transcript_lines.append(f"{msg['sender']}: {msg['text']}")
    transcript_full_text = "\n".join(transcript_lines)
    
    # Build metadata
    start_time = processed_messages[0]["timestamp"]
    total_messages = len(processed_messages)
    
    return {
        "metadata": {
            "conversation_id": conversation_id,
            "start_time_utc": start_time,
            "total_messages": total_messages
        },
        "transcript_full_text": transcript_full_text,
        "transcript_list_of_messages": processed_messages
    }


def process_conversations_file(input_file: str, output_file: str, max_conversations: int = 100):
    """
    Process conversations from input file and save cleaned format to output file.
    """
    print(f"Loading conversations from {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return
    
    if not isinstance(data, list):
        print("Error: Expected JSON array at root level")
        return
    
    print(f"Found {len(data)} conversations in file")
    
    # Process conversations
    cleaned_conversations = []
    processed_count = 0
    
    for i, conv_data in enumerate(data):
        if processed_count >= max_conversations:
            break
            
        cleaned_conv = process_conversation(conv_data)
        if cleaned_conv:
            cleaned_conversations.append(cleaned_conv)
            processed_count += 1
            
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1} conversations, {processed_count} valid")
    
    print(f"\nSuccessfully processed {processed_count} conversations")
    
    # Save output
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_conversations, f, ensure_ascii=False, indent=2)
    
    print(f"Done! Saved {len(cleaned_conversations)} conversations to {output_file}")


if __name__ == "__main__":
    input_file = "last-500-conversation-dugunbuketi.json"
    output_file = "cleaned_conversations.json"
    max_conversations = 100
    
    process_conversations_file(input_file, output_file, max_conversations)