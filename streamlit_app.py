import streamlit as st
from agent import clarification_agent, solution_agent, quality_assurance_agent, concise_answer_agent
from streamlit_shadcn_ui import button
import re
from collections import Counter

def add_copy_button(content: str, key_suffix: str):
    if button(text="Copy to Clipboard", key=f"copy_{key_suffix}", kwargs={"js_on_click": f"() => navigator.clipboard.writeText({repr(content)})"}):
        st.toast("Copied!")

def analyze_text_nlp(text: str):
    """Perform NLP analysis on the text"""
    analysis = {}
    
    # Basic statistics
    words = text.split()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    analysis['word_count'] = len(words)
    analysis['sentence_count'] = len(sentences)
    analysis['char_count'] = len(text)
    analysis['avg_word_length'] = sum(len(word) for word in words) / len(words) if words else 0
    
    # Word frequency
    word_freq = Counter(word.lower().strip('.,!?;:"()[]{}') for word in words if len(word) > 3)
    analysis['top_words'] = word_freq.most_common(5)
    
    # Question type detection
    question_lower = text.lower()
    if any(word in question_lower for word in ['what', 'define', 'explain']):
        analysis['question_type'] = '📚 Definition/Explanation'
        analysis['type_description'] = 'You want to understand a concept'
    elif any(word in question_lower for word in ['how', 'calculate', 'solve']):
        analysis['question_type'] = '🔢 Problem-Solving'
        analysis['type_description'] = 'You need help solving a problem'
    elif any(word in question_lower for word in ['why', 'reason']):
        analysis['question_type'] = '🤔 Reasoning/Analysis'
        analysis['type_description'] = 'You want to know the reasoning'
    elif any(word in question_lower for word in ['compare', 'difference', 'similar']):
        analysis['question_type'] = '⚖️ Comparison'
        analysis['type_description'] = 'You want to compare things'
    else:
        analysis['question_type'] = '💬 General Question'
        analysis['type_description'] = 'General inquiry'
    
    # Complexity analysis
    complex_words = [w for w in words if len(w) > 8]
    analysis['complexity_score'] = len(complex_words) / len(words) * 100 if words else 0
    
    if analysis['complexity_score'] < 10:
        analysis['complexity_label'] = '✅ Simple'
    elif analysis['complexity_score'] < 20:
        analysis['complexity_label'] = '📖 Moderate'
    else:
        analysis['complexity_label'] = '🎓 Advanced'
    
    # Named entity detection (simple version)
    capitalized = [word for word in words if word and word[0].isupper() and word.lower() not in ['i', 'a']]
    analysis['potential_entities'] = list(set(capitalized))[:5]
    
    return analysis

def display_nlp_analysis(question: str, solution: str = None):
    """Display NLP analysis in the sidebar - only once"""
    st.sidebar.header("🔬 NLP Analysis")
    st.sidebar.caption("Understanding your question using Natural Language Processing")
    
    # Question Analysis
    st.sidebar.subheader("Your Question")
    q_analysis = analyze_text_nlp(question)
    
    # Question stats in a cleaner format
    st.sidebar.markdown(f"""
    **📊 Question Stats:**
    - Contains **{q_analysis['word_count']} words** in **{q_analysis['sentence_count']} sentence(s)**
    - Average word length: **{q_analysis['avg_word_length']:.1f} characters**
    """)
    
    st.sidebar.markdown(f"""
    **🎯 Question Type:** {q_analysis['question_type']}  
    *{q_analysis['type_description']}*
    """)
    
    st.sidebar.markdown(f"""
    **📈 Complexity Level:** {q_analysis['complexity_label']}  
    *Based on vocabulary used*
    """)
    
    if q_analysis['potential_entities']:
        st.sidebar.markdown("**🏷️ Key Topics Detected:**")
        st.sidebar.write("• " + " • ".join(q_analysis['potential_entities']))
    
    if q_analysis['top_words']:
        st.sidebar.markdown("**🔑 Most Important Words:**")
        keywords = [f"**{word}** (used {count}x)" for word, count in q_analysis['top_words'][:3]]
        st.sidebar.write("• " + "\n• ".join(keywords))
    
    # Solution Analysis (if available)
    if solution:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📝 Answer Analysis")
        s_analysis = analyze_text_nlp(solution)
        
        st.sidebar.markdown(f"""
        **Answer Length:**
        - **{s_analysis['word_count']} words** across **{s_analysis['sentence_count']} sentences**
        - That's about **{s_analysis['word_count'] // q_analysis['word_count']}x longer** than your question
        """)
        
        # Compare complexity in simple terms
        if s_analysis['complexity_score'] > q_analysis['complexity_score'] + 5:
            complexity_note = "📚 The answer uses more technical language"
        elif s_analysis['complexity_score'] < q_analysis['complexity_score'] - 5:
            complexity_note = "✨ The answer is explained simply"
        else:
            complexity_note = "✅ The answer matches your question's level"
        
        st.sidebar.markdown(f"**Style:** {complexity_note}")

def main():
    st.set_page_config(
        page_title="Homework Helper",
        page_icon=":books:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS to style the app
    st.markdown("""
        <style>
            /* Ensure main background matches Streamlit's dark theme */
            .main .block-container {
                padding-top: 2rem;
            }
            /* General text color for better readability */
            body, .st-emotion-cache-1r6slb0, .st-emotion-cache-1y4p8pa {
                color: #fafafa;
            }

            .stButton>button {
                background-color: #28a745;
                color: white;
            }
            .stTextArea textarea {
                border-radius: 10px;
                border: 1px solid #d1d9e6;
            }
            /* Styling for info/success boxes and expanders for dark mode */
            .stAlert, .st-emotion-cache-1wivap2, .stExpander {
                background-color: #262730;
                border-radius: 10px;
                border: 1px solid #444;
            }
            .st-emotion-cache-p5msec {
                color: #fafafa;
            }
            .st-emotion-cache-ch2v7v {
                padding-top: 1rem;
            }
            .st-emotion-cache-10trblm {
                color: #fafafa;
            }
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #1e1e1e;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("Homework Helper 📚")
    st.write("""
        Welcome to the Homework Helper! Ask any homework question and get help from multiple AI agents.
        Enter your question in the text box below and press "Get Answer" to see the answers.
    """)

    # Input section
    st.header("Enter Your Homework Question")
    question = st.text_area("Type your question here:", height=150)

    if st.button("Get Answer"):
        if question.strip():
            # Clear sidebar and display NLP analysis once
            st.sidebar.empty()
            display_nlp_analysis(question)
            
            # Clarification agent
            with st.spinner("Checking clarity of the question..."):
                clarification_stream = clarification_agent(question)
                if clarification_stream is None:
                    return
                clarification = "".join(clarification_stream)
            
            # Stop if there was an API error
            if not clarification:
                return
            
            # A more robust check. The agent is prompted to say "The question is clear."
            if "the question is clear" not in clarification.lower():
                st.warning("Clarification Needed")
                st.info(clarification)
            else:
                # Solution agent
                with st.spinner("Generating solution..."):
                    solution_stream = solution_agent(question)
                    if solution_stream is None:
                        return
                    solution = "".join(solution_stream)
                
                if not solution:
                    st.error("Failed to generate solution. Please try again.")
                    return

                # Quality assurance agent
                with st.spinner("Reviewing solution for quality..."):
                    review_stream = quality_assurance_agent(solution)
                    if review_stream is None:
                        return
                    review = "".join(review_stream)

                # Concise answer agent
                with st.spinner("Generating concise answer..."):
                    concise_stream = concise_answer_agent(solution)
                    if concise_stream is None:
                        return
                    concise_answer = "".join(concise_stream)
                
                # Stop if any generation failed
                if not all([solution, review, concise_answer]):
                    st.error("An error occurred during generation. Please try again.")
                    return

                # Update sidebar with solution analysis (without duplicating question analysis)
                st.sidebar.markdown("---")
                st.sidebar.subheader("📝 Answer Analysis")
                s_analysis = analyze_text_nlp(solution)
                q_analysis = analyze_text_nlp(question)
                
                st.sidebar.markdown(f"""
                **Answer Length:**
                - **{s_analysis['word_count']} words** across **{s_analysis['sentence_count']} sentences**
                - That's about **{s_analysis['word_count'] // q_analysis['word_count']}x longer** than your question
                """)
                
                # Compare complexity in simple terms
                if s_analysis['complexity_score'] > q_analysis['complexity_score'] + 5:
                    complexity_note = "📚 The answer uses more technical language"
                elif s_analysis['complexity_score'] < q_analysis['complexity_score'] - 5:
                    complexity_note = "✨ The answer is explained simply"
                else:
                    complexity_note = "✅ The answer matches your question's level"
                
                st.sidebar.markdown(f"**Style:** {complexity_note}")

                # Display results
                st.header("Results")
                st.subheader("Concise Answer")
                add_copy_button(concise_answer, key_suffix="concise")
                st.success(concise_answer, icon="✅")
                
                st.subheader("Detailed Solution")
                add_copy_button(solution, key_suffix="solution")
                st.info(solution)

                # Add expanders for detailed agent reasoning
                st.header("Agent Reasoning")
                with st.expander("Clarification Agent Response"):
                    st.write(clarification)
                with st.expander("Quality Assurance Agent Response"):
                    st.write(review)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
