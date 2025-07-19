# Planner Agent

# This agent decides how to break down the revision task and manages syllabus-aware planning.

# planner_agent.py

from openai import OpenAI
import json
import os
from typing import List

class PlannerAgent:
    def __init__(self, client: OpenAI):
        self.client = client
        self.syllabus = self._load_syllabus()
        self.system_prompt = (
            "You are a planner agent that breaks down academic topics into 3–5 focused subtopics "
            "suitable for quick revision before an exam. Keep subtopics concise and specific."
        )

    def _load_syllabus(self) -> dict:
        """Load the syllabus from JSON file"""
        try:
            syllabus_path = os.path.join(os.path.dirname(__file__), 'syllabus.json')
            with open(syllabus_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Syllabus file not found. Using basic planning mode.")
            return {}

    def get_all_topics(self) -> List[str]:
        """Get all topics from the syllabus"""
        all_topics = []
        for category, topics in self.syllabus.items():
            all_topics.extend(topics)
        return all_topics

    def filter_topics_by_keywords(self, keywords: List[str]) -> List[str]:
        """Filter syllabus topics based on keywords"""
        filtered_topics = []
        all_topics = self.get_all_topics()
        
        for topic in all_topics:
            topic_lower = topic.lower()
            for keyword in keywords:
                if keyword.lower() in topic_lower:
                    if topic not in filtered_topics:
                        filtered_topics.append(topic)
                    break
        
        return filtered_topics

    def get_topics_by_category(self, category: str) -> List[str]:
        """Get topics from a specific category"""
        return self.syllabus.get(category, [])

    def plan_subtopics(self, user_topic: str) -> List[str]:
        """Break down a user topic into subtopics using AI"""
        # First check if the topic exists in syllabus
        syllabus_topics = self.filter_topics_by_keywords([user_topic])
        
        if syllabus_topics:
            return syllabus_topics[:5]  # Limit to 5 topics
        
        # If not in syllabus, use AI to break down
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Break down this topic for revision: {user_topic}"}
        ]
        response = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages,
            temperature=0.3
        )
        content = response.choices[0].message.content
        return [line.strip(" -1234567890. ") for line in content.strip().split("\n") if line.strip()]
