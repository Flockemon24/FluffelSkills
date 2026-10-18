from __future__ import annotations

import json
import sys
from pprint import pprint

from ai import (
    analyze_evidence_with_ai,
    FluffelSkillsAIError,
    FluffelSkillsConfigurationError,
)

from skill_engine import build_fluffelskills_profile

from job_catalog import JOB_PROFILES


# ============================================================
# TEST USER
# ============================================================

TEST_DATA = {
    "personal_details": {
        "age": 17,
        "country": "Germany",
        "education_status": "Student",
    },

    "goals": [
        "Become an AI Engineer",
        "Learn Machine Learning",
        "Build AI projects",
    ],

    "desired_job": "AI Engineer",

    "school_leaving_certificate": {
        "type": "Abitur",
        "expected_grade": 1.8,
    },

    "studies": [],

    "work_experience": [
        {
            "role": "Software Development Intern",
            "duration_months": 2,
            "description": (
                "Worked on a small internal software project."
            ),
        }
    ],

    "existing_skills": [
        {
            "name": "Python",
            "self_reported_level": 75,
        },
        {
            "name": "Git",
            "self_reported_level": 60,
        },
        {
            "name": "JavaScript",
            "self_reported_level": 40,
        },
    ],

    "uploaded_documents": [],

    "github_data": {
        "public_repositories": 8,
        "languages": [
            "Python",
            "JavaScript",
        ],
        "repositories": [
            {
                "name": "ai-chatbot",
                "language": "Python",
                "description": (
                    "AI chatbot using a language model API."
                ),
            },
            {
                "name": "flask-dashboard",
                "language": "Python",
                "description": (
                    "Small Flask web application."
                ),
            },
            {
                "name": "web-project",
                "language": "JavaScript",
                "description": (
                    "Small frontend project."
                ),
            },
        ],
    },

    "certificates": [],

    "skill_tests": [
        {
            "skill": "Python",
            "score": 82,
        },
        {
            "skill": "Git",
            "score": 68,
        },
    ],

    "projects": [
        {
            "name": "AI Chatbot",
            "description": (
                "Built a Python chatbot that communicates "
                "with an AI API."
            ),
            "technologies": [
                "Python",
                "API",
                "Git",
            ],
        },
        {
            "name": "Flask Dashboard",
            "description": (
                "Created a web dashboard using Flask."
            ),
            "technologies": [
                "Python",
                "Flask",
                "HTML",
                "CSS",
            ],
        },
    ],

    "employer_confirmations": [],

    "learning_progress": [
        {
            "skill": "Python",
            "progress": 80,
        },
        {
            "skill": "Git",
            "progress": 65,
        },
    ],

    "challenge_results": [
        {
            "skill": "Python",
            "score": 78,
        }
    ],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_separator(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def check_required_keys(
    data: dict,
    required_keys: list[str],
) -> None:
    missing = [
        key
        for key in required_keys
        if key not in data
    ]

    if missing:
        raise AssertionError(
            f"Fehlende Keys: {missing}"
        )


def check_skill_profile(
    profile: dict,
) -> None:

    assert "skills" in profile, (
        "skill_profile muss 'skills' enthalten."
    )

    assert isinstance(
        profile["skills"],
        list,
    ), "skills muss eine Liste sein."

    for skill in profile["skills"]:
        assert "name" in skill
        assert "category" in skill
        assert "level" in skill
        assert "confidence" in skill
        assert "sources" in skill
        assert "evidence" in skill

        assert 0 <= skill["level"] <= 100
        assert 0 <= skill["confidence"] <= 100

        assert isinstance(
            skill["sources"],
            list,
        )

        assert isinstance(
            skill["evidence"],
            list,
        )


def check_missing_skills(
    missing_skills: list[dict],
) -> None:

    allowed_statuses = {
        "missing",
        "not_verified",
        "partially_demonstrated",
    }

    for skill in missing_skills:
        assert "skill" in skill
        assert "status" in skill
        assert "importance" in skill
        assert "reason" in skill
        assert "evidence_gap" in skill

        assert skill["status"] in allowed_statuses

        assert 0 <= skill["importance"] <= 100


def check_job_match(
    job_match: int,
) -> None:

    assert isinstance(
        job_match,
        int,
    ), "job_match muss eine Ganzzahl sein."

    assert 0 <= job_match <= 100


# ============================================================
# MAIN TEST
# ============================================================

def main() -> int:

    print_separator(
        "FLUFFELSKILLS FULL INTEGRATION TEST"
    )

    print("🚀 Starte FluffelSkills-Test...")
    print()

    print("Testprofil:")
    pprint(TEST_DATA)

    # --------------------------------------------------------
    # 1. CHECK JOB PROFILE
    # --------------------------------------------------------

    print_separator(
        "1. JOB PROFILE"
    )

    job_name = TEST_DATA["desired_job"]

    if job_name not in JOB_PROFILES:
        print(
            f"❌ Beruf '{job_name}' wurde nicht gefunden."
        )
        return 1

    job_profile = JOB_PROFILES[job_name]

    print(
        f"✅ Job gefunden: {job_profile['title']}"
    )

    print(
        f"✅ Anforderungen: "
        f"{len(job_profile['required_skills'])}"
    )

    # --------------------------------------------------------
    # 2. AI EVIDENCE ANALYSIS
    # --------------------------------------------------------

    print_separator(
        "2. AI EVIDENCE ANALYSIS"
    )

    try:

        ai_result = analyze_evidence_with_ai(
            personal_details=TEST_DATA[
                "personal_details"
            ],
            goals=TEST_DATA[
                "goals"
            ],
            desired_job=TEST_DATA[
                "desired_job"
            ],
            school_leaving_certificate=TEST_DATA[
                "school_leaving_certificate"
            ],
            studies=TEST_DATA[
                "studies"
            ],
            work_experience=TEST_DATA[
                "work_experience"
            ],
            existing_skills=TEST_DATA[
                "existing_skills"
            ],
            uploaded_documents=TEST_DATA[
                "uploaded_documents"
            ],
            github_data=TEST_DATA[
                "github_data"
            ],
            certificates=TEST_DATA[
                "certificates"
            ],
            skill_tests=TEST_DATA[
                "skill_tests"
            ],
            projects=TEST_DATA[
                "projects"
            ],
            employer_confirmations=TEST_DATA[
                "employer_confirmations"
            ],
            learning_progress=TEST_DATA[
                "learning_progress"
            ],
            challenge_results=TEST_DATA[
                "challenge_results"
            ],
            output_language="Deutsch",
        )

    except FluffelSkillsConfigurationError as exc:

        print("❌ Konfigurationsfehler:")
        print(exc)

        return 1

    except FluffelSkillsAIError as exc:

        print("❌ AI-Fehler:")
        print(exc)

        return 1

    except Exception as exc:

        print("❌ Unerwarteter Fehler:")
        print(type(exc).__name__)
        print(exc)

        return 1

    print("✅ KI-Antwort erhalten.")

    # --------------------------------------------------------
    # 3. AI OUTPUT VALIDATION
    # --------------------------------------------------------

    print_separator(
        "3. AI OUTPUT VALIDATION"
    )

    check_required_keys(
        ai_result,
        [
            "skills",
            "skill_relations",
            "strength_candidates",
            "profile_improvements",
        ],
    )

    print("✅ Alle AI-Output-Keys vorhanden.")

    print(
        f"✅ Erkannte Skills: "
        f"{len(ai_result['skills'])}"
    )

    print(
        f"✅ Skill-Relations: "
        f"{len(ai_result['skill_relations'])}"
    )

    print(
        f"✅ Strength Candidates: "
        f"{len(ai_result['strength_candidates'])}"
    )

    print(
        f"✅ Profile Improvements: "
        f"{len(ai_result['profile_improvements'])}"
    )

    # --------------------------------------------------------
    # SHOW AI RESULT
    # --------------------------------------------------------

    print_separator(
        "AI RESULT"
    )

    print(
        json.dumps(
            ai_result,
            indent=2,
            ensure_ascii=False,
        )
    )

    # --------------------------------------------------------
    # 4. BUILD BACKEND PROFILE
    # --------------------------------------------------------

    print_separator(
        "4. FLUFFELSKILLS ENGINE"
    )

    final_profile = build_fluffelskills_profile(
        ai_analysis=ai_result,
        raw_data=TEST_DATA,
        job_profile=job_profile,
    )

    print("✅ Backend-Profil erzeugt.")

    # --------------------------------------------------------
    # 5. FINAL STRUCTURE
    # --------------------------------------------------------

    print_separator(
        "5. FINAL STRUCTURE"
    )

    check_required_keys(
        final_profile,
        [
            "skill_profile",
            "skill_graph",
            "strengths",
            "missing_skills",
            "job_match",
            "profile_improvements",
        ],
    )

    print(
        "✅ Finale Struktur ist korrekt."
    )

    # --------------------------------------------------------
    # 6. CHECK SKILLS
    # --------------------------------------------------------

    print_separator(
        "6. SKILL VALIDATION"
    )

    check_skill_profile(
        final_profile["skill_profile"]
    )

    print(
        "✅ Skill-Profil validiert."
    )

    for skill in final_profile[
        "skill_profile"
    ]["skills"]:

        print(
            f"  • {skill['name']}: "
            f"Level {skill['level']} | "
            f"Confidence {skill['confidence']}"
        )

    # --------------------------------------------------------
    # 7. CHECK MISSING SKILLS
    # --------------------------------------------------------

    print_separator(
        "7. MISSING SKILLS"
    )

    check_missing_skills(
        final_profile["missing_skills"]
    )

    print(
        "✅ Missing Skills validiert."
    )

    for skill in final_profile[
        "missing_skills"
    ]:

        print(
            f"  • {skill['skill']}: "
            f"{skill['status']} | "
            f"Importance {skill['importance']}"
        )

    # --------------------------------------------------------
    # 8. CHECK JOB MATCH
    # --------------------------------------------------------

    print_separator(
        "8. JOB MATCH"
    )

    job_match = final_profile[
        "job_match"
    ]

    check_job_match(job_match)

    print(
        f"✅ Job Match berechnet: "
        f"{job_match}%"
    )

    # --------------------------------------------------------
    # 9. SKILL GRAPH
    # --------------------------------------------------------

    print_separator(
        "9. SKILL GRAPH"
    )

    graph = final_profile[
        "skill_graph"
    ]

    assert len(graph["nodes"]) > 0, (
    "Skill Graph darf keine 0 Nodes enthalten."
)

    assert len(graph["nodes"]) >= len(
        final_profile["skill_profile"]["skills"]
    ), (
        "Der Skill Graph sollte mindestens "
        "alle erkannten Skills als Nodes enthalten."
    )

    assert "nodes" in graph
    assert "edges" in graph

    for skill in final_profile[
        "skill_profile"
    ]["skills"]:

        assert 0 <= skill["level"] <= 100
        assert 0 <= skill["confidence"] <= 95

    print(
        f"✅ Nodes: "
        f"{len(graph['nodes'])}"
    )

    print(
        f"✅ Edges: "
        f"{len(graph['edges'])}"
    )

    # --------------------------------------------------------
    # 10. FINAL JSON
    # --------------------------------------------------------

    print_separator(
        "10. FINAL FLUFFELSKILLS PROFILE"
    )

    print(
        json.dumps(
            final_profile,
            indent=2,
            ensure_ascii=False,
        )
    )

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print_separator(
        "✅ TEST ERFOLGREICH"
    )

    print(
        "Die komplette FluffelSkills-Pipeline funktioniert."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())