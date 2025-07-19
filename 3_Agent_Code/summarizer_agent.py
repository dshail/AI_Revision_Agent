# Summarizer Agent

# This agent generates summaries based on the plan using dynamic prompt loading.
# summarizer_agent.py

from openai import OpenAI
import os
from typing import Dict, Any

class SummarizerAgent:
    def __init__(self, client: OpenAI):
        self.client = client
        self.system_prompt = self._load_prompt_template()
        self.session_memory = {}  # Store context for session memory

    def _load_prompt_template(self) -> str:
        """Load the system prompt from the prompts directory"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'revision_prompt.txt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("⚠️ Prompt template not found. Using default prompt.")
            return (
                "You are a helpful tutor preparing students for an AI/ML exam. "
                "Given a subtopic, generate a concise explanation suitable for revision. "
                "Be technically accurate, exam-oriented, and to the point."
            )

    def add_to_memory(self, topic: str, context: Dict[str, Any]):
        """Add topic context to session memory"""
        self.session_memory[topic] = context

    def get_from_memory(self, topic: str) -> Dict[str, Any]:
        """Retrieve topic context from session memory"""
        return self.session_memory.get(topic, {})

    def summarize(self, subtopic: str) -> str:
        """Generate a summary for the given subtopic"""
        # Check if we have previous context for this topic
        memory_context = self.get_from_memory(subtopic)
        
        # Prepare the user message with context if available
        user_message = f"Explain this subtopic for revision: {subtopic}"
        if memory_context:
            user_message += f"\n\nPrevious context: {memory_context.get('context', '')}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=messages,
                temperature=0.5
            )
            summary = response.choices[0].message.content.strip()
            
            # Store this summary in memory for potential follow-up
            self.add_to_memory(subtopic, {
                'summary': summary,
                'context': f"Previously explained {subtopic}",
                'timestamp': str(os.times())
            })
            
            return summary
            
        except Exception as e:
            print(f"❌ Error generating summary for {subtopic}: {str(e)}")
            return f"Unable to generate summary for {subtopic}. Please try again."
