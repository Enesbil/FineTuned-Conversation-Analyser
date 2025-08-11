#!/usr/bin/env python3
"""
Validate JSONL file format for OpenAI fine-tuning
"""

import json

def validate_jsonl(filename):
    print(f'🔍 Validating JSONL file: {filename}')
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f'📊 Total lines: {len(lines)}')
        
        valid_count = 0
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                print(f'❌ Line {i}: Empty line')
                continue
                
            try:
                json_obj = json.loads(line)
                
                # Check if it has required structure
                if 'messages' not in json_obj:
                    print(f'❌ Line {i}: Missing "messages" field')
                    continue
                    
                if not isinstance(json_obj['messages'], list):
                    print(f'❌ Line {i}: "messages" is not a list')
                    continue
                    
                if len(json_obj['messages']) != 3:
                    print(f'❌ Line {i}: Expected 3 messages, got {len(json_obj["messages"])}')
                    continue
                    
                # Check message roles
                roles = [msg.get('role') for msg in json_obj['messages']]
                expected_roles = ['system', 'user', 'assistant']
                if roles != expected_roles:
                    print(f'❌ Line {i}: Expected roles {expected_roles}, got {roles}')
                    continue
                
                # Check if assistant message has content
                assistant_msg = json_obj['messages'][2]
                if 'content' not in assistant_msg or not assistant_msg['content']:
                    print(f'❌ Line {i}: Assistant message missing content')
                    continue
                
                # Try to parse assistant response as JSON
                try:
                    assistant_json = json.loads(assistant_msg['content'])
                    required_fields = ['overall_sentiment', 'bot_understanding', 'bot_performance', 'bot_answered']
                    missing_fields = [field for field in required_fields if field not in assistant_json]
                    if missing_fields:
                        print(f'❌ Line {i}: Missing fields in assistant response: {missing_fields}')
                        continue
                except json.JSONDecodeError:
                    print(f'❌ Line {i}: Assistant content is not valid JSON')
                    continue
                    
                valid_count += 1
                if i <= 3:  # Show details for first 3
                    print(f'✅ Line {i}: Valid JSON with {len(json_obj["messages"])} messages')
                    
            except json.JSONDecodeError as e:
                print(f'❌ Line {i}: Invalid JSON - {e}')
                continue
        
        print(f'📋 Summary: {valid_count}/{len(lines)} lines are valid JSONL')
        
        if valid_count == len(lines):
            print('🎉 All lines are valid JSONL format!')
            return True
        else:
            print('⚠️ Some lines have issues - file needs fixing')
            return False
            
    except Exception as e:
        print(f'❌ Error reading file: {e}')
        return False

if __name__ == "__main__":
    is_valid = validate_jsonl('fine_tuning_data.jsonl')
    
    if is_valid:
        print("\n✅ File is ready for OpenAI fine-tuning upload!")
    else:
        print("\n❌ File needs to be fixed before upload")
