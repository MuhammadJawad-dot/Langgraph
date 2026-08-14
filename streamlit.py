import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from app.sub_graphs.research_graph import research_graph
from fpdf import FPDF


# Setup page
st.set_page_config(page_title="AI Research Agent", layout="wide")
st.title("🤖 AI Research Agent")

# Initialize session state for thread_id
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4()) # Generate a unique ID for the session

# Create the graph config
config = {"configurable": {"thread_id": st.session_state.thread_id}}
# Check current state of the graph
snapshot = research_graph.get_state(config)
def generate_pdf(report):
    pdf = FPDF()
    pdf.add_page()
    
    # Helper to clean text for the PDF
    def clean_text(text):
        return str(text).encode('latin-1', 'replace').decode('latin-1')

    # Helper to add standard sections
    def add_section(title, body):
        pdf.set_font("helvetica", style="B", size=14)
        pdf.write(8, clean_text(title))
        pdf.ln(10)
        
        pdf.set_font("helvetica", size=12)
        pdf.write(6, clean_text(body))
        pdf.ln(10)
        
    # Helper to add lists
    def add_list_section(title, items):
        pdf.set_font("helvetica", style="B", size=14)
        pdf.write(8, clean_text(title))
        pdf.ln(10)
        
        pdf.set_font("helvetica", size=12)
        for i, item in enumerate(items, 1):
            pdf.write(6, clean_text(f"{i}. {item}"))
            pdf.ln(8)
        pdf.ln(5)

    # Build the PDF
    add_section("Title", report.title)
    add_section("Executive Summary", report.executive_summary)
    
    add_list_section("Key Findings", report.key_findings)
    
    add_section("Detailed Analysis", report.detailed_analysis)
    
    add_list_section("Fact-Checked Claims", report.fact_checked_claims)
    add_section("Conclusion", report.conclusion)
    add_list_section("Sources", report.sources)
    
    return bytes(pdf.output())



# If the graph hasn't started yet, show the input box
if not snapshot.next and "final_report" not in (snapshot.values or {}):
    question = st.text_input("Enter your research question:")
    
    if st.button("Start Research") and question:
        with st.spinner("Researching..."):
            initial_state = {
                "question": question,
                "messages": [HumanMessage(content=f"Research this question: {question}")],
            }
            # Start the graph
            research_graph.invoke(initial_state, config=config)
            # Rerun the page to load the next step
            st.rerun()
# Check if graph is waiting for approval
if snapshot.next and "human_approval" in snapshot.next:
    state = snapshot.values
    
    st.warning("⚠️ Human Approval Required")
    st.subheader(f"Question: {state['question']}")
    
    # Show Claims
    with st.expander("View Claims", expanded=True):
        for i, claim in enumerate(state.get("claims", []), 1):
            st.write(f"{i}. {claim}")
            
    # Show Fact Checks
    with st.expander("View Fact Checks", expanded=True):
        for i, check in enumerate(state.get("fact_checks", []), 1):
            st.markdown(f"**Claim:** {check.get('claim', '')}")
            st.write(f"**Status:** {check.get('status', '').upper()}")
            st.write(f"**Evidence:** {check.get('evidence', '')}")
            st.divider()

    # Approve / Reject Logic
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve Research", use_container_width=True):
            response = {"decision": "approved", "feedback": ""}
            research_graph.invoke(Command(resume=response), config=config)
            st.rerun()
            
    with col2:
        # For rejection, we need an input box for feedback
        feedback = st.text_input("Rejection Feedback:")
        if st.button("❌ Reject & Retry", use_container_width=True):
            if feedback:
                response = {"decision": "rejected", "feedback": feedback}
                research_graph.invoke(Command(resume=response), config=config)
                st.rerun()
            else:
                st.error("Please provide feedback before rejecting.")
# If graph is finished and we have a final report
if not snapshot.next and snapshot.values and "final_report" in snapshot.values:
    st.success("Research Completed!")
    report = snapshot.values["final_report"]
    
    st.header(report.title)
    st.subheader("Executive Summary")
    st.write(report.executive_summary)
    
    st.subheader("Key Findings")
    for finding in report.key_findings:
        st.write(f"- {finding}")
        
    st.subheader("Detailed Analysis")
    st.write(report.detailed_analysis)
    
    st.subheader("Fact-Checked Claims")
    for index, claim in enumerate(report.fact_checked_claims, 1):
        st.write(f"{index}. {claim}")
        
    st.subheader("Conclusion")
    st.write(report.conclusion)
    
    st.subheader("Sources")
    for index, source in enumerate(report.sources, 1):
        st.write(f"{index}. {source}")
    
    # st.divider()
    # if st.button("Start New Research"):
    #     st.session_state.thread_id = str(uuid.uuid4()) # Generate new ID to reset
    #     st.rerun()
        st.divider()
    
    # Put the buttons side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Start New Research", use_container_width=True):
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()
            
    with col2:
        # Generate the PDF in the background
        pdf_bytes = generate_pdf(report)
        
        # Display the download button
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_bytes,
            file_name="AI_Research_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

