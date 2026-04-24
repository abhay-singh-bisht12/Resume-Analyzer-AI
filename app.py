import streamlit as st
import matplotlib.pyplot as plt

from utils.pdf_reader import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.suggestions import get_suggestions

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄", layout="wide")


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def footer():
    st.markdown(
        "<div class='footer'>Made by <span>Abhay Singh Bisht</span></div>",
        unsafe_allow_html=True
    )


load_css()

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""


st.sidebar.markdown("""
<div class="sidebar-logo">
    <h2>📄 Resume AI</h2>
    <p>Skill Gap Finder</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Menu",
    ["🏠 Home", "📤 Upload Resume", "🎯 Analyze Job"]
)


st.markdown("""
<div class="top-header">
    <h1>Resume Analyzer AI</h1>
    <p>Upload resume, compare with job description, find missing skills and improve your chances.</p>
</div>
""", unsafe_allow_html=True)


if page == "🏠 Home":
    st.markdown("""
    <div class="hero-card">
        <div>
            <h2>Analyze Your Resume Like a Recruiter</h2>
            <p>This tool compares your resume skills with job requirements and tells you your match score.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Resume Parsing</h3>
            <p>Extracts text from PDF resume.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Skill Match</h3>
            <p>Compares resume skills with JD skills.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Suggestions</h3>
            <p>Shows missing skills and improvement tips.</p>
        </div>
        """, unsafe_allow_html=True)

    footer()


if page == "📤 Upload Resume":
    left, right = st.columns([1.4, 0.8])

    with left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-heading'>📤 Upload Your Resume</h2>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf")

        if uploaded_file is not None:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = extract_skills(resume_text)

            st.session_state.resume_text = resume_text
            st.session_state.resume_skills = resume_skills

            st.success("Resume uploaded and skills detected successfully!")

            st.markdown("<h3 class='mini-heading'>Detected Skills</h3>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='skill-pill-box'>{', '.join(resume_skills) if resume_skills else 'No skills detected.'}</div>",
                unsafe_allow_html=True
            )

            with st.expander("View Extracted Resume Text"):
                st.write(resume_text)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="side-card">
            <h3>🔥 What this app does</h3>
            <p>✅ Reads resume PDF</p>
            <p>✅ Detects skills</p>
            <p>✅ Compares with job description</p>
            <p>✅ Shows match percentage</p>
            <p>✅ Gives improvement suggestions</p>
        </div>
        """, unsafe_allow_html=True)

    footer()


if page == "🎯 Analyze Job":
    if not st.session_state.resume_skills:
        st.warning("Please upload your resume first.")
        footer()
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-heading'>📝 Paste Job Description</h2>", unsafe_allow_html=True)

        job_desc = st.text_area(
            "Job Description",
            placeholder="Example: We need a web developer with HTML, CSS, JavaScript, React, Git and SQL.",
            height=150
        )

        analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if analyze_btn:
            if not job_desc.strip():
                st.warning("Please enter job description first.")
            else:
                jd_skills = extract_skills(job_desc)

                if not jd_skills:
                    st.warning("No skills detected. Add skills like Python, SQL, JavaScript, React, etc.")
                else:
                    resume_skills = st.session_state.resume_skills

                    matched = sorted(list(set(resume_skills) & set(jd_skills)))
                    missing = sorted(list(set(jd_skills) - set(resume_skills)))
                    match_percent = (len(matched) / len(jd_skills)) * 100

                    st.markdown("<div class='result-wrapper'>", unsafe_allow_html=True)

                    m1, m2, m3 = st.columns(3)

                    with m1:
                        st.markdown(f"""
                        <div class="metric-card blue">
                            <h3>{match_percent:.2f}%</h3>
                            <p>Match Score</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with m2:
                        st.markdown(f"""
                        <div class="metric-card green">
                            <h3>{len(matched)}</h3>
                            <p>Matched Skills</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with m3:
                        st.markdown(f"""
                        <div class="metric-card red">
                            <h3>{len(missing)}</h3>
                            <p>Missing Skills</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.progress(int(match_percent))

                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📊 Result",
                        "📈 Graphs",
                        "💡 Suggestions",
                        "📄 Report"
                    ])

                    with tab1:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("<h3 class='mini-heading'>✅ Matched Skills</h3>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='success-box'>{', '.join(matched) if matched else 'No matched skills'}</div>",
                                unsafe_allow_html=True
                            )

                        with col2:
                            st.markdown("<h3 class='mini-heading'>❌ Missing Skills</h3>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='danger-box'>{', '.join(missing) if missing else 'None 🎉'}</div>",
                                unsafe_allow_html=True
                            )

                        st.markdown("<h3 class='mini-heading'>📌 Job Required Skills</h3>", unsafe_allow_html=True)
                        st.info(", ".join(jd_skills))

                    with tab2:
                        col_chart1, col_chart2 = st.columns(2)

                        with col_chart1:
                            fig1, ax1 = plt.subplots(figsize=(4, 3))
                            labels = ["Matched", "Missing"]
                            values = [len(matched), len(missing)]
                            colors = ["#16a34a", "#dc2626"]

                            ax1.bar(labels, values, color=colors, width=0.45)
                            ax1.set_title("Matched vs Missing Skills", fontweight="bold")
                            ax1.set_ylabel("Skill Count")
                            ax1.set_ylim(0, max(values) + 2)
                            ax1.spines["top"].set_visible(False)
                            ax1.spines["right"].set_visible(False)

                            st.pyplot(fig1, use_container_width=True)

                        with col_chart2:
                            fig2, ax2 = plt.subplots(figsize=(4, 3))
                            labels2 = ["Resume Skills", "JD Skills"]
                            values2 = [len(resume_skills), len(jd_skills)]
                            colors2 = ["#2563eb", "#7c3aed"]

                            ax2.bar(labels2, values2, color=colors2, width=0.45)
                            ax2.set_title("Resume vs JD Skill Count", fontweight="bold")
                            ax2.set_ylabel("Skill Count")
                            ax2.set_ylim(0, max(values2) + 2)
                            ax2.spines["top"].set_visible(False)
                            ax2.spines["right"].set_visible(False)

                            st.pyplot(fig2, use_container_width=True)

                    with tab3:
                        st.markdown("<h3 class='mini-heading'>💡 Smart Suggestions</h3>", unsafe_allow_html=True)

                        if missing:
                            for suggestion in get_suggestions(missing):
                                st.info("👉 " + suggestion)
                        else:
                            st.success("Great! Your resume matches all required skills.")

                        st.markdown("<h3 class='mini-heading'>🧠 Resume Improvement Tips</h3>", unsafe_allow_html=True)

                        if match_percent < 50:
                            st.error("Your resume is weak for this job. Add missing skills and relevant projects.")
                        elif match_percent < 80:
                            st.warning("Your resume partially matches this job. Improve missing skills.")
                        else:
                            st.success("Your resume is strong for this job role.")

                    with tab4:
                        report = f"""
Resume Analyzer Report

Match Percentage: {match_percent:.2f}%

Resume Skills:
{", ".join(resume_skills)}

Job Required Skills:
{", ".join(jd_skills)}

Matched Skills:
{", ".join(matched) if matched else "No matched skills"}

Missing Skills:
{", ".join(missing) if missing else "No missing skills"}

Suggestions:
"""

                        if missing:
                            for suggestion in get_suggestions(missing):
                                report += f"- {suggestion}\n"
                        else:
                            report += "- Your resume matches all required skills.\n"

                        st.download_button(
                            label="📥 Download Report",
                            data=report,
                            file_name="resume_analysis_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                    st.markdown("</div>", unsafe_allow_html=True)

        footer()