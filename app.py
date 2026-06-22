import streamlit as st

from services.pdf_service import extract_text_from_pdf
from services.resume_service import analyze_resume


st.set_page_config(
    page_title="DocPilot AI",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
        .main-title {
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 0;
        }
        .subtitle {
            font-size: 20px;
            color: #9ca3af;
            margin-bottom: 30px;
        }
        .score-card {
            padding: 30px;
            border-radius: 18px;
            background: linear-gradient(135deg, #111827, #1f2937);
            border: 1px solid #374151;
            margin: 24px 0;
        }
        .score-number {
            font-size: 64px;
            font-weight: 900;
            margin: 0;
        }
        .score-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 22px;
        }
        .score-mini-card {
            padding: 14px;
            border-radius: 12px;
            background: #0f172a;
            border: 1px solid #334155;
        }
        .score-mini-label {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 6px;
        }
        .score-mini-value {
            font-size: 24px;
            font-weight: 800;
            color: #f8fafc;
        }
        .skill-chip {
            background: #2563eb;
            color: white;
            padding: 7px 13px;
            border-radius: 999px;
            margin: 5px;
            display: inline-block;
            font-size: 14px;
        }
        .small-card {
            padding: 18px;
            border-radius: 14px;
            background: #111827;
            border: 1px solid #374151;
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-title">📄 DocPilot AI</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Premium document intelligence for resumes, proposals, and PDFs.</p>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload your resume or PDF document",
    type=["pdf"],
)

if uploaded_file:
    st.info(f"Processing: {uploaded_file.name}")

    try:
        extracted_text = extract_text_from_pdf(uploaded_file)

        if not extracted_text:
            st.warning("No readable text found. This may be a scanned/image-based PDF.")
            st.stop()

        st.success("PDF text extracted successfully.")

        analysis = analyze_resume(extracted_text)
        score = analysis["ats_score"]
        breakdown = analysis["ats_breakdown"]

        if score >= 85:
            score_label = "Excellent"
            score_message = "Your resume is well-structured and ATS-friendly."
        elif score >= 70:
            score_label = "Good"
            score_message = "Your resume is strong but can be improved."
        elif score >= 50:
            score_label = "Needs Improvement"
            score_message = "Your resume needs stronger structure and keyword coverage."
        else:
            score_label = "Weak"
            score_message = "Your resume may struggle during ATS screening."

        st.markdown("## Resume Analysis")

        st.markdown(
                  
            f"""<div class="score-card">
<p style="color:#9ca3af; margin-bottom:4px;">ATS Readiness Score</p>
<p class="score-number">{score}%</p>
<h2 style="color:#38bdf8; margin-top:0;">{score_label}</h2>
<p style="font-size:17px; color:#d1d5db;">Grade: <b>{analysis["grade"]}</b></p>
<p style="font-size:17px; color:#d1d5db;">{score_message}</p>

<div class="score-grid">
    <div class="score-mini-card">
        <div class="score-mini-label">Keyword Coverage</div>
        <div class="score-mini-value">{breakdown["Keyword Coverage"]}%</div>
    </div>
    <div class="score-mini-card">
        <div class="score-mini-label">Contact Completeness</div>
        <div class="score-mini-value">{breakdown["Contact Completeness"]}%</div>
    </div>
    <div class="score-mini-card">
        <div class="score-mini-label">Section Coverage</div>
        <div class="score-mini-value">{breakdown["Section Coverage"]}%</div>
    </div>
    <div class="score-mini-card">
        <div class="score-mini-label">Skills Match</div>
        <div class="score-mini-value">{breakdown["Skills Match"]}%</div>
    </div>
</div>
</div>""",
            unsafe_allow_html=True,
        )
      

        st.caption(f"{score}% ATS Readiness")
        st.progress(score / 100)

        st.markdown("### ATS Breakdown")

        breakdown_cols = st.columns(4)

        with breakdown_cols[0]:
            st.metric("Keyword Coverage", f"{breakdown['Keyword Coverage']}%")

        with breakdown_cols[1]:
            st.metric("Contact Completeness", f"{breakdown['Contact Completeness']}%")

        with breakdown_cols[2]:
            st.metric("Section Coverage", f"{breakdown['Section Coverage']}%")

        with breakdown_cols[3]:
            st.metric("Skills Match", f"{breakdown['Skills Match']}%")

        st.markdown("### Resume Statistics")

        stats = analysis["stats"]
        stat_cols = st.columns(5)

        stat_cols[0].metric(
            "Resume Length",
            stats["resume_length"],
            stats["resume_length_status"],
        )
        stat_cols[1].metric("Skills Found", stats["skills_found"])
        stat_cols[2].metric("Projects", stats["projects"])
        stat_cols[3].metric("Certifications", stats["certifications"])
        stat_cols[4].metric(
            "Sections",
            f'{stats["sections_found"]}/{stats["sections_total"]}',
        )

        st.markdown("### Recruiter Verdict")

        verdict = analysis["recruiter_verdict"]

        verdict_col1, verdict_col2 = st.columns(2)

        with verdict_col1:
            st.markdown("**Excellent candidate for:**")
            for item in verdict["excellent_for"]:
                st.success(f"✓ {item}")

        with verdict_col2:
            st.markdown("**Future Growth Areas:**")
            for item in verdict["needs_stronger_evidence_for"]:
                st.warning(f"• {item}")

        st.markdown("### Top Matched Roles")

        role_cols = st.columns(len(analysis["matched_roles"]))

        for index, role in enumerate(analysis["matched_roles"]):
            with role_cols[index]:
                st.metric(role["role"], f'{role["match"]}%')
                st.progress(role["match"] / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Contact Information")

            email = analysis["email"]
            linkedin = analysis["linkedin"]

            email_html = (
                f'<a href="mailto:{email}" style="color:#93c5fd; text-decoration:none;">{email}</a>'
                if email != "Not found"
                else "Not found"
            )

            linkedin_html = "Not found"

            if linkedin != "Not found":
                linkedin_url = (
                    linkedin if linkedin.startswith("http")
                    else f"https://{linkedin}"
                )

                linkedin_html = (
                    f'<a href="{linkedin_url}" target="_blank" '
                    f'style="color:#93c5fd; text-decoration:none;">'
                    f"{linkedin}</a>"
                )

            st.markdown(
                f"""
                <div class="small-card">📧 <b>Email:</b> {email_html}</div>
                <div class="small-card">📱 <b>Phone:</b> {analysis["phone"]}</div>
                <div class="small-card">🔗 <b>LinkedIn:</b> {linkedin_html}</div>
                <div class="small-card">📍 <b>Location:</b> {analysis["location"]}</div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("### Skills Found")

            for category, skills in analysis["found_skills"].items():
                if skills:
                    st.markdown(f"**{category} ({len(skills)})**")
                    skills_html = " ".join(
                        f'<span class="skill-chip">{skill.title()}</span>'
                        for skill in skills
                    )
                    st.markdown(skills_html, unsafe_allow_html=True)

        st.markdown("### Resume Sections Detected")

        section_cols = st.columns(len(analysis["sections"]))

        for index, (section, exists) in enumerate(analysis["sections"].items()):
            with section_cols[index]:
                if exists:
                    st.success(f"✓ {section.title()} Found")
                else:
                    st.warning(f"✗ {section.title()} Missing")

        if analysis["missing_sections"]:
            st.markdown("### Optional Sections to Consider")
            st.info(
                "Optional sections that may strengthen some applications: "
                + ", ".join(
                    section.title()
                    for section in analysis["missing_sections"]
                )
            )
        else:
            st.markdown("### Missing Sections")
            st.success("No critical sections missing.")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### Strengths")
            for strength in analysis["strengths"]:
                st.success(strength)

        with col4:
            st.markdown("### Top Improvements")
            for recommendation in analysis["recommendations"]:
                st.warning(recommendation)

        st.success(
            f"""
            Resume Assessment Summary

            ATS Score: {score}%
            Grade: {analysis["grade"]}

            Strong candidate for AI/ML internships, Data Analyst roles,
            Graduate Trainee programs, and Research Assistant opportunities.
            """
        )

        with st.expander("Developer View: Extracted Text"):
            st.text_area(
                label="PDF Content",
                value=extracted_text,
                height=420,
            )

        st.download_button(
            label="Download Extracted Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain",
        )

    except RuntimeError as error:
        st.error(str(error))