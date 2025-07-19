# Utility Functions

# Helper functions used by agents.

# utils.py

import json
import os
from typing import List

def print_banner():
    print("=" * 60)
    print("🤖 AI Revision Agent for AI/ML Exam Preparation")
    print("=" * 60)
    print("📚 Covering: AI, ML, DL, GenAI, and Agent AI")
    print("=" * 60)

def format_response(subtopic: str, answer: str) -> str:
    return (
        f"\n🔹 **Subtopic**: {subtopic}\n"
        f"{'-'*50}\n"
        f"{answer}\n"
        f"{'-'*50}\n"
    )

def load_syllabus() -> dict:
    """Load the syllabus from JSON file"""
    try:
        syllabus_path = os.path.join(os.path.dirname(__file__), 'syllabus.json')
        with open(syllabus_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Syllabus file not found.")
        return {}

def filter_topics_by_keywords(keywords: List[str]) -> List[str]:
    """Filter syllabus topics based on keywords"""
    syllabus = load_syllabus()
    filtered_topics = []
    
    # Get all topics from syllabus
    all_topics = []
    for category, topics in syllabus.items():
        all_topics.extend(topics)
    
    # Filter by keywords
    for topic in all_topics:
        topic_lower = topic.lower()
        for keyword in keywords:
            if keyword.lower() in topic_lower:
                if topic not in filtered_topics:
                    filtered_topics.append(topic)
                break
    
    return filtered_topics

def save_session_log(topics: List[str], summaries: List[str], filename: str = None):
    """Save the current session to a log file"""
    if not filename:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"revision_session_{timestamp}.txt"
    
    output_dir = os.path.join(os.path.dirname(__file__), 'sample_output')
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("🤖 AI Revision Agent - Session Log\n")
        f.write("=" * 50 + "\n\n")
        
        for topic, summary in zip(topics, summaries):
            f.write(f"🔹 Topic: {topic}\n")
            f.write("-" * 30 + "\n")
            f.write(f"{summary}\n")
            f.write("-" * 30 + "\n\n")
    
    print(f"📄 Session saved to: {filepath}")
    return filepath
