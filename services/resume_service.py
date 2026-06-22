import re


def extract_section(text: str, start_keywords: list[str], all_headings: list[str]) -> str:
    lines = text.splitlines()
    start_index = None

    for index, line in enumerate(lines):
        cleaned = line.strip().lower()

        if any(keyword in cleaned for keyword in start_keywords):
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        cleaned = line.strip().lower()

        if cleaned and any(
            cleaned == heading or cleaned.startswith(heading)
            for heading in all_headings
        ):
            break

        section_lines.append(line)

    return "\n".join(section_lines).strip()


def count_meaningful_lines(section_text: str) -> int:
    lines = [
        line.strip()
        for line in section_text.splitlines()
        if line.strip()
    ]

    meaningful_lines = [
        line
        for line in lines
        if len(line.split()) >= 2
    ]

    return len(meaningful_lines)


def analyze_resume(text: str) -> dict:
    text_lower = text.lower()

    all_headings = [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "education",
        "academic background",
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
        "freelance",
        "projects",
        "academic projects",
        "technical projects",
        "skills",
        "technical skills",
        "certifications",
        "certificates",
        "training",
        "awards",
        "honors",
        "publications",
        "research",
        "activities",
        "languages",
        "interests",
        "areas of interest",
    ]

    skill_categories = {
        "Programming": [
            "python",
            "sql",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            "php",
            "ruby",
            "go",
            "r",
        ],
        "Data Science": [
            "pandas",
            "numpy",
            "data analysis",
            "data analytics",
            "excel",
            "power bi",
            "tableau",
            "statistics",
            "visualization",
            "eda",
        ],
        "Machine Learning": [
            "machine learning",
            "deep learning",
            "scikit-learn",
            "tensorflow",
            "keras",
            "pytorch",
            "classification",
            "regression",
            "nlp",
            "computer vision",
        ],
        "Tools": [
            "git",
            "github",
            "jupyter",
            "google colab",
            "visual studio code",
            "vs code",
            "streamlit",
            "flask",
            "django",
            "fastapi",
            "docker",
            "mongodb",
            "mysql",
            "postgresql",
        ],
    }

    found_skills = {}
    total_found_skills = []

    for category, skills in skill_categories.items():
        matched = [skill for skill in skills if skill in text_lower]
        found_skills[category] = matched
        total_found_skills.extend(matched)

    unique_skills = set(total_found_skills)

    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)

    phone_match = re.search(
        r"(\+\d{1,3}[\s-]?\d{2,4}[\s-]?\d{6,10}|03\d{2}[\s-]?\d{7})",
        text,
    )

    linkedin_match = re.search(
        r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[\w\-]+",
        text,
        re.IGNORECASE,
    )

    location_detected = bool(
        re.search(
            r"\b(rawalpindi|islamabad|sukkur|karachi|lahore|pakistan|india|usa|uk|canada|uae|dubai)\b",
            text_lower,
        )
    )

    sections = {
        "education": bool(
            extract_section(text, ["education", "academic background"], all_headings)
            or "education" in text_lower
        ),
        "experience": bool(
            extract_section(
                text,
                ["experience", "work experience", "professional experience", "internship", "freelance"],
                all_headings,
            )
            or "experience" in text_lower
            or "internship" in text_lower
            or "freelance" in text_lower
        ),
        "projects": bool(
            extract_section(text, ["projects", "academic projects", "technical projects"], all_headings)
            or "project" in text_lower
        ),
        "skills": bool(
            extract_section(text, ["skills", "technical skills"], all_headings)
            or "skills" in text_lower
        ),
        "certifications": bool(
            extract_section(text, ["certifications", "certificates", "training"], all_headings)
            or "certification" in text_lower
            or "certificate" in text_lower
            or "training" in text_lower
        ),
    }

    projects_section = extract_section(
        text,
        ["projects", "academic projects", "technical projects"],
        all_headings,
    )

    certifications_section = extract_section(
        text,
        ["certifications", "certificates", "training"],
        all_headings,
    )

    project_count = count_meaningful_lines(projects_section)

    if project_count == 0 and sections["projects"]:
        project_count = 1

    cert_count = count_meaningful_lines(certifications_section)

    if cert_count == 0 and sections["certifications"]:
        cert_count = 1

    optional_sections = ["awards", "publications"]

    missing_sections = [
        section for section in optional_sections
        if section not in text_lower
    ]

    section_coverage_score = round((sum(sections.values()) / len(sections)) * 100)
    skills_match_score = min(len(unique_skills) * 5, 100)

    contact_items = [email_match, phone_match, linkedin_match]
    contact_completeness_score = round(
        (sum(1 for item in contact_items if item) / 3) * 100
    )

    keyword_coverage_score = min(len(unique_skills) * 6, 100)

    ats_score = round(
        (section_coverage_score * 0.35)
        + (skills_match_score * 0.30)
        + (contact_completeness_score * 0.20)
        + (keyword_coverage_score * 0.15)
    )

    if ats_score >= 90:
        grade = "A+"
    elif ats_score >= 80:
        grade = "A"
    elif ats_score >= 70:
        grade = "B"
    elif ats_score >= 60:
        grade = "C"
    else:
        grade = "Needs Work"

    word_count = len(text.split())

    if 350 <= word_count <= 850:
        resume_length_status = "Optimal Range ✓"
    elif word_count < 350:
        resume_length_status = "Too Short"
    else:
        resume_length_status = "Too Long"

    stats = {
        "resume_length": f"{word_count} words",
        "resume_length_status": resume_length_status,
        "skills_found": len(unique_skills),
        "projects": project_count,
        "certifications": cert_count,
        "sections_found": sum(sections.values()),
        "sections_total": len(sections),
    }

    strengths = []

    if len(unique_skills) >= 10:
        strengths.append("Strong technical keyword coverage detected.")

    if project_count >= 2:
        strengths.append("Multiple technical projects identified.")

    if email_match and phone_match and linkedin_match:
        strengths.append("Professional contact information is complete.")

    if ats_score >= 85:
        strengths.append("ATS-friendly resume structure detected.")

    if cert_count >= 1:
        strengths.append("Industry-relevant certifications identified.")

    recommendations = []

    if not phone_match:
        recommendations.append("Add a clearly formatted phone number.")

    if not linkedin_match:
        recommendations.append("Add a LinkedIn profile link.")

    if "github" not in text_lower:
        recommendations.append("Add GitHub profile or project repository links.")

    if project_count < 2:
        recommendations.append("Add more project-based evidence of practical skills.")

    if cert_count == 0:
        recommendations.append("Add relevant certifications or training if available.")

    recommendations.append("Add quantified achievements where possible.")
    recommendations.append("Highlight measurable project impact.")
    recommendations.append("Use role-specific keywords from each job description.")

    data_score = len(found_skills["Data Science"]) * 12
    ml_score = len(found_skills["Machine Learning"]) * 12
    programming_score = len(found_skills["Programming"]) * 10
    tools_score = len(found_skills["Tools"]) * 8

    matched_roles = [
        {
            "role": "Data Analyst Intern",
            "match": min(ats_score - 8 + data_score + tools_score // 3, 100),
        },
        {
            "role": "AI/ML Intern",
            "match": min(ats_score - 10 + ml_score + programming_score // 3, 100),
        },
        {
            "role": "Graduate Trainee Engineer",
            "match": min(ats_score - 5 + programming_score // 4, 100),
        },
        {
            "role": "Research Assistant",
            "match": min(ats_score - 12 + ml_score // 2 + data_score // 3, 100),
        },
    ]

    matched_roles = [
        {"role": role["role"], "match": max(round(role["match"]), 0)}
        for role in matched_roles
    ]

    excellent_for = [
        role["role"].replace(" Intern", " Internships").replace(" Roles", " Roles")
        for role in matched_roles
        if role["match"] >= 85
    ]

    if not excellent_for:
        excellent_for = ["Entry-level technical roles"]

    recruiter_verdict = {
        "excellent_for": excellent_for,
        "needs_stronger_evidence_for": [
            "Senior roles",
            "Research-intensive roles",
        ],
    }

    return {
        "email": email_match.group(0) if email_match else "Not found",
        "phone": phone_match.group(0) if phone_match else "Not found",
        "linkedin": linkedin_match.group(0) if linkedin_match else "Not found",
        "location": "Detected" if location_detected else "Not found",
        "found_skills": found_skills,
        "sections": sections,
        "missing_sections": missing_sections,
        "ats_score": ats_score,
        "grade": grade,
        "ats_breakdown": {
            "Keyword Coverage": keyword_coverage_score,
            "Contact Completeness": contact_completeness_score,
            "Section Coverage": section_coverage_score,
            "Skills Match": skills_match_score,
        },
        "stats": stats,
        "strengths": strengths,
        "recommendations": recommendations,
        "matched_roles": matched_roles,
        "recruiter_verdict": recruiter_verdict,
    }