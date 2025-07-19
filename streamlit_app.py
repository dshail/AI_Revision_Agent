"""
AI Revision Agent - Streamlit Web Interface
A web-based interface for the AI Revision Agent
"""

import streamlit as st
import os
import sys
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Add the 3_Agent_Code directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '3_Agent_Code'))

from planner_agent import PlannerAgent
from summarizer_agent import SummarizerAgent
from utils import load_syllabus, save_session_log

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Revision Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with improved colors
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .summary-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        color: #212529;
    }
    .topic-item {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #2196f3;
        color: #1565c0;
        font-weight: 500;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'planner' not in st.session_state:
        st.session_state.planner = None
    if 'summarizer' not in st.session_state:
        st.session_state.summarizer = None
    if 'topics' not in st.session_state:
        st.session_state.topics = []
    if 'summaries' not in st.session_state:
        st.session_state.summaries = {}
    if 'syllabus' not in st.session_state:
        st.session_state.syllabus = load_syllabus()
    if 'show_summaries' not in st.session_state:
        st.session_state.show_summaries = False
    if 'generated_summaries' not in st.session_state:
        st.session_state.generated_summaries = []

def setup_openrouter_client():
    """Setup OpenRouter client"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("🔑 OpenRouter API key not found! Please set OPENROUTER_API_KEY in your .env file.")
        st.info("💡 Create a .env file in your project root with: OPENROUTER_API_KEY=your_key_here")
        st.stop()
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        st.session_state.client = client
        st.session_state.planner = PlannerAgent(client)
        st.session_state.summarizer = SummarizerAgent(client)
        st.success("✅ OpenRouter client initialized successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize OpenRouter client: {str(e)}")
        with st.expander("🔍 Error Details"):
            st.code(str(e))
        return False

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Revision Agent</h1>
        <p>Your AI-powered study companion for AI, ML, DL, GenAI, and Agent AI</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with options"""
    st.sidebar.header("🎯 Revision Options")
    
    # Revision mode selection
    revision_mode = st.sidebar.radio(
        "Choose Revision Mode:",
        ["🔍 Keyword-based Revision", "📚 Topic-based Revision", "📖 Browse Syllabus"],
        help="Select how you want to approach your revision"
    )
    
    st.sidebar.markdown("---")
    
    # Display syllabus categories
    if st.session_state.syllabus:
        st.sidebar.subheader("📋 Available Categories")
        for category, topics in st.session_state.syllabus.items():
            with st.sidebar.expander(f"{category.replace('_', ' ')} ({len(topics)} topics)"):
                for topic in topics[:5]:  # Show first 5 topics
                    st.write(f"• {topic}")
                if len(topics) > 5:
                    st.write(f"... and {len(topics) - 5} more")
    
    return revision_mode

def keyword_revision_interface():
    """Interface for keyword-based revision"""
    st.subheader("🔍 Keyword-based Revision")
    st.write("Enter keywords to find matching topics from our comprehensive syllabus.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keywords_input = st.text_input(
            "Enter keywords (comma-separated):",
            placeholder="e.g., neural, transformer, learning",
            help="Enter keywords separated by commas to find related topics"
        )
    
    with col2:
        search_button = st.button("🔍 Search Topics", type="primary")
    
    # Handle search
    if search_button and keywords_input:
        keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
        
        if keywords:
            with st.spinner("Searching for matching topics..."):
                filtered_topics = st.session_state.planner.filter_topics_by_keywords(keywords)
                
                if filtered_topics:
                    st.session_state.found_topics = filtered_topics
                    st.session_state.search_performed = True
                    st.success(f"🎯 Found {len(filtered_topics)} matching topics!")
                else:
                    st.session_state.found_topics = []
                    st.session_state.search_performed = True
                    st.warning("❌ No topics found matching your keywords. Try different keywords or check spelling.")
    
    # Display found topics if search was performed
    if hasattr(st.session_state, 'search_performed') and st.session_state.search_performed:
        if hasattr(st.session_state, 'found_topics') and st.session_state.found_topics:
            st.subheader("📋 Matching Topics")
            for i, topic in enumerate(st.session_state.found_topics, 1):
                st.markdown(f"""
                <div class="topic-item">
                    <strong>{i}. {topic}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            # Generate summaries button
            if st.button("📝 Generate Summaries", type="primary", key="generate_keyword"):
                generate_summaries_directly(st.session_state.found_topics)
        
        # Clear search button
        if st.button("🔄 New Search", type="secondary"):
            st.session_state.search_performed = False
            st.session_state.found_topics = []
            st.rerun()

def topic_revision_interface():
    """Interface for topic-based revision"""
    st.subheader("📚 Topic-based Revision")
    st.write("Enter a topic and let AI break it down into subtopics for you.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic_input = st.text_input(
            "Enter a topic to revise:",
            placeholder="e.g., Deep Learning, Machine Learning, Transformers",
            help="Enter any AI/ML topic you want to study"
        )
    
    with col2:
        plan_button = st.button("🧩 Plan Revision", type="primary")
    
    if plan_button and topic_input:
        with st.spinner("Planning your revision..."):
            subtopics = st.session_state.planner.plan_subtopics(topic_input)
            
            if subtopics:
                st.session_state.planned_topics = subtopics
                st.session_state.plan_created = True
                st.success(f"📋 Created revision plan with {len(subtopics)} subtopics!")
            else:
                st.session_state.planned_topics = []
                st.session_state.plan_created = True
                st.error("❌ Failed to create revision plan. Please try a different topic.")
    
    # Display planned topics if plan was created
    if hasattr(st.session_state, 'plan_created') and st.session_state.plan_created:
        if hasattr(st.session_state, 'planned_topics') and st.session_state.planned_topics:
            st.subheader("🧩 Revision Plan")
            for i, subtopic in enumerate(st.session_state.planned_topics, 1):
                st.markdown(f"""
                <div class="topic-item">
                    <strong>{i}. {subtopic}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            # Generate summaries button
            if st.button("📝 Generate Summaries", type="primary", key="generate_topic"):
                generate_summaries_directly(st.session_state.planned_topics)
        
        # Clear plan button
        if st.button("🔄 New Plan", type="secondary"):
            st.session_state.plan_created = False
            st.session_state.planned_topics = []
            st.rerun()

def browse_syllabus_interface():
    """Interface for browsing the syllabus"""
    st.subheader("📖 Browse Syllabus")
    st.write("Explore our comprehensive syllabus and select topics to study.")
    
    if st.session_state.syllabus:
        # Category selection
        selected_category = st.selectbox(
            "Choose a category:",
            list(st.session_state.syllabus.keys()),
            format_func=lambda x: x.replace('_', ' ')
        )
        
        if selected_category:
            topics = st.session_state.syllabus[selected_category]
            st.write(f"**{selected_category.replace('_', ' ')}** ({len(topics)} topics)")
            
            # Topic selection
            selected_topics = st.multiselect(
                "Select topics to study:",
                topics,
                help="You can select multiple topics for revision"
            )
            
            if selected_topics:
                st.session_state.topics = selected_topics
                
                # Display selected topics
                st.subheader("📋 Selected Topics")
                for i, topic in enumerate(selected_topics, 1):
                    st.markdown(f"""
                    <div class="topic-item">
                        <strong>{i}. {topic}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Generate summaries button
                if st.button("📝 Generate Summaries", type="primary", key="generate_browse"):
                    generate_summaries_directly(selected_topics)

def generate_summaries_directly(topics):
    """Generate summaries for the given topics directly"""
    if not topics:
        st.warning("No topics selected for summary generation.")
        return
    
    # Check if API key is available
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("🔑 OpenRouter API key not found! Please set OPENROUTER_API_KEY in your .env file.")
        return
    
    # Check if agents are initialized
    if not st.session_state.summarizer:
        st.error("❌ Summarizer agent not initialized!")
        return
    
    st.markdown("---")
    st.subheader("📝 Generated Summaries")
    
    # Create a container for summaries
    summary_container = st.container()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    summaries = []
    
    for i, topic in enumerate(topics):
        status_text.text(f"🔄 Processing {i+1}/{len(topics)}: {topic}")
        progress_bar.progress((i + 1) / len(topics))
        
        try:
            # Generate summary
            summary = st.session_state.summarizer.summarize(topic)
            
            if summary and summary.strip():
                summaries.append(summary)
                st.session_state.summaries[topic] = summary
                
                # Display summary in container
                with summary_container:
                    st.success(f"✅ Generated summary for: **{topic}**")
                    
                    # Use expander for better organization
                    with st.expander(f"📖 {topic}", expanded=True):
                        st.write(summary)
                    
                    st.markdown("---")
                
            else:
                st.warning(f"⚠️ Empty summary received for: {topic}")
                
        except Exception as e:
            error_msg = f"Failed to generate summary for {topic}: {str(e)}"
            st.error(f"❌ {error_msg}")
            
            # Show detailed error for debugging
            with st.expander("🔍 Error Details"):
                st.code(f"Topic: {topic}\nError: {str(e)}")
    
    status_text.text("✅ All summaries processed!")
    progress_bar.progress(1.0)
    
    # Session saving option
    if summaries:
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("💾 Save Session", type="secondary", key="save_session"):
                save_current_session(topics, summaries)
        
        with col2:
            if st.button("🔄 Start New Session", type="secondary", key="new_session"):
                st.session_state.topics = []
                st.session_state.summaries = {}
                st.rerun()
        
        st.success(f"🎉 Summary generation complete! Generated {len(summaries)} summaries.")
    else:
        st.warning("⚠️ No summaries were generated. Please check your API key and try again.")

def display_summary(topic, summary):
    """Display a formatted summary"""
    st.markdown(f"""
    <div class="summary-box">
        <h3>🔹 {topic}</h3>
        <div style="white-space: pre-wrap;">{summary}</div>
    </div>
    """, unsafe_allow_html=True)

def save_current_session(topics, summaries):
    """Save the current session to a file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"streamlit_session_{timestamp}.txt"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join("3_Agent_Code", "sample_output")
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = save_session_log(topics, summaries, filename)
        st.success(f"💾 Session saved successfully to: {filepath}")
        
        # Offer download
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        st.download_button(
            label="📥 Download Session File",
            data=content,
            file_name=filename,
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ Failed to save session: {str(e)}")

def main():
    """Main Streamlit application"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Setup OpenRouter client
    if not st.session_state.client:
        if not setup_openrouter_client():
            st.stop()
    
    # Display sidebar and get revision mode
    revision_mode = display_sidebar()
    
    # Main content area
    if revision_mode == "🔍 Keyword-based Revision":
        keyword_revision_interface()
    elif revision_mode == "📚 Topic-based Revision":
        topic_revision_interface()
    elif revision_mode == "📖 Browse Syllabus":
        browse_syllabus_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>🤖 AI Revision Agent | Built with Streamlit & OpenRouter</p>
        <p>Happy studying! 📚✨</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()