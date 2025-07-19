# CLI Interface

# Command-line interface to interact with the AI agent.

# cli_interface.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from planner_agent import PlannerAgent
from summarizer_agent import SummarizerAgent
from utils import print_banner, format_response, save_session_log

def main():
    # Load environment variables
    load_dotenv()
    
    print_banner()
    
    # Ask user for revision mode
    print("🔍 Choose your revision mode:")
    print("1. Full revision (all topics)")
    print("2. Keyword-based revision (filtered topics)")
    
    mode = input("Enter your choice (1/2) or (full/keyword): ").strip().lower()
    
    # Initialize OpenRouter client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    planner = PlannerAgent(client)
    summarizer = SummarizerAgent(client)

    if mode in ['2', 'keyword']:
        # Keyword-based revision
        keywords = input("📝 Enter keywords (comma-separated): ").strip()
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        if not keyword_list:
            print("❌ No keywords provided. Switching to full revision mode.")
            topics = planner.get_all_topics()
        else:
            topics = planner.filter_topics_by_keywords(keyword_list)
            print(f"\n🎯 Found {len(topics)} topics matching your keywords:")
            for i, topic in enumerate(topics, 1):
                print(f"  {i}. {topic}")
    else:
        # Full revision mode
        topic = input("📚 Enter a topic you want to revise: ")
        topics = planner.plan_subtopics(topic)

    if not topics:
        print("❌ No topics found. Please try different keywords or check your input.")
        return

    print(f"\n📝 Generating summaries for {len(topics)} topic(s)...\n")
    print("-" * 50)
    
    summaries = []
    for topic_item in topics:
        answer = summarizer.summarize(topic_item)
        summaries.append(answer)
        print(format_response(topic_item, answer))
    
    # Ask user if they want to save the session
    save_choice = input("\n💾 Save this revision session to file? (y/n): ").strip().lower()
    if save_choice in ['y', 'yes']:
        save_session_log(topics, summaries)
    
    print("\n✅ Revision session completed! Happy studying! 📚")

if __name__ == "__main__":
    main()