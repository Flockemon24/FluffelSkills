from __future__ import annotations

from collections import defaultdict
from typing import Any


# ============================================================
# SKILL NORMALIZATION
# ============================================================

SKILL_ALIASES = {
    "python": "Python",
    "python programming": "Python",

    "javascript": "JavaScript",
    "js": "JavaScript",

    "git": "Git",
    "git/github": "Git",

    "machine learning": "Machine Learning",
    "ml": "Machine Learning",

    "deep learning": "Deep Learning",
    "dl": "Deep Learning",

    "statistics": "Statistics",
    "statistik": "Statistics",

    "data visualization": "Data Visualization",

    "api development": "API Development",

    "cloud deployment": "Cloud Deployment",

    "data preprocessing": "Data Preprocessing",

    "model evaluation": "Model Evaluation",
}


def normalize_skill_name(name: str) -> str:
    key = name.strip().lower()

    return SKILL_ALIASES.get(
        key,
        name.strip(),
    )


# ============================================================
# SOURCE WEIGHTS
# ============================================================

# Used for calculating how strong the evidence is.
SOURCE_CONFIDENCE = {
    "skill_test": 80,
    "challenge_result": 70,
    "employer_confirmation": 80,
    "project": 50,
    "github": 40,
    "work_experience": 35,
    "learning_progress": 35,
    "certificate": 30,
    "uploaded_document": 25,
    "self_report": 15,
}


# ============================================================
# DIRECT SCORES
# ============================================================

def _find_direct_scores(
    skill_name: str,
    raw_data: dict[str, Any],
) -> list[float]:

    scores: list[float] = []

    normalized = normalize_skill_name(skill_name)

    # Skill tests
    for test in raw_data.get("skill_tests") or []:
        if not isinstance(test, dict):
            continue

        test_skill = normalize_skill_name(
            str(test.get("skill", ""))
        )

        if test_skill == normalized:
            score = test.get("score")

            if isinstance(score, (int, float)):
                scores.append(
                    max(0, min(100, float(score)))
                )

    # Challenge results
    for challenge in raw_data.get("challenge_results") or []:
        if not isinstance(challenge, dict):
            continue

        challenge_skill = normalize_skill_name(
            str(challenge.get("skill", ""))
        )

        if challenge_skill == normalized:
            score = challenge.get("score")

            if isinstance(score, (int, float)):
                scores.append(
                    max(0, min(100, float(score)))
                )

    # Learning progress
    for progress in raw_data.get("learning_progress") or []:
        if not isinstance(progress, dict):
            continue

        progress_skill = normalize_skill_name(
            str(progress.get("skill", ""))
        )

        if progress_skill == normalized:
            value = progress.get("progress")

            if isinstance(value, (int, float)):
                scores.append(
                    max(0, min(100, float(value)))
                )

    return scores


# ============================================================
# LEVEL CALCULATION
# ============================================================

def _find_self_reported_level(
    skill_name: str,
    raw_data: dict[str, Any],
) -> float | None:

    normalized = normalize_skill_name(
        skill_name
    )

    for skill in raw_data.get(
        "existing_skills",
        [],
    ):

        if not isinstance(skill, dict):
            continue

        reported_name = normalize_skill_name(
            str(skill.get("name", ""))
        )

        if reported_name != normalized:
            continue

        value = skill.get(
            "self_reported_level"
        )

        if isinstance(value, (int, float)):
            return max(
                0,
                min(100, float(value)),
            )

    return None


def calculate_skill_level(
    skill: dict[str, Any],
    raw_data: dict[str, Any],
) -> int:

    skill_name = normalize_skill_name(
        skill["name"]
    )

    # --------------------------------------------------------
    # 1. Direct measurements
    # --------------------------------------------------------

    direct_scores = _find_direct_scores(
        skill_name,
        raw_data,
    )

    self_report = _find_self_reported_level(
        skill_name,
        raw_data,
    )

    # --------------------------------------------------------
    # 2. Strongest case:
    # direct test / challenge / learning measurements
    # --------------------------------------------------------

    if direct_scores:
        measurements = list(direct_scores)

        if self_report is not None:
            measurements.append(
                self_report
            )

        base_level = (
            sum(measurements)
            / len(measurements)
        )

    # --------------------------------------------------------
    # 3. Only self-report
    # --------------------------------------------------------

    elif self_report is not None:
        base_level = self_report

    # --------------------------------------------------------
    # 4. No numerical measurement
    # --------------------------------------------------------

    else:
        source_types = {
            evidence["source_type"]
            for evidence in skill.get(
                "evidence",
                [],
            )
        }

        base_level = 30

        if "project" in source_types:
            base_level += 10

        if "github" in source_types:
            base_level += 5

        if "work_experience" in source_types:
            base_level += 10

        if "employer_confirmation" in source_types:
            base_level += 15

        if "certificate" in source_types:
            base_level += 5

        if "challenge_result" in source_types:
            base_level += 10

    # --------------------------------------------------------
    # 5. Practical evidence gives only a small bonus.
    # It must NOT overpower direct test results.
    # --------------------------------------------------------

    source_types = {
        evidence["source_type"]
        for evidence in skill.get(
            "evidence",
            [],
        )
    }

    practical_sources = (
        "project",
        "github",
        "work_experience",
        "employer_confirmation",
    )

    practical_count = sum(
        1
        for source in practical_sources
        if source in source_types
    )

    if direct_scores or self_report is not None:
        base_level += min(
            practical_count * 3,
            9,
        )

    return round(
        max(
            0,
            min(100, base_level),
        )
    )

# ============================================================
# CONFIDENCE CALCULATION
# ============================================================

def calculate_confidence(
    skill: dict[str, Any],
) -> int:

    source_types = {
        evidence["source_type"]
        for evidence in skill.get("evidence", [])
    }

    if not source_types:
        return 0

    source_scores = [
        SOURCE_CONFIDENCE[source]
        for source in source_types
        if source in SOURCE_CONFIDENCE
    ]

    if not source_scores:
        return 0

    # Durchschnittliche Qualität der vorhandenen Nachweise.
    base_score = sum(source_scores) / len(source_scores)

    # Unterschiedliche unabhängige Quellen erhöhen die Sicherheit.
    diversity_bonus = min(
        20,
        (len(source_types) - 1) * 5,
    )

    confidence = round(
        base_score + diversity_bonus
    )

    return min(
        confidence,
        95,
    )

# ============================================================
# SKILL PROFILE
# ============================================================

def build_skill_profile(
    ai_analysis: dict[str, Any],
    raw_data: dict[str, Any],
) -> dict[str, Any]:

    skills: list[dict[str, Any]] = []

    for candidate in ai_analysis.get("skills", []):
        name = normalize_skill_name(
            candidate["name"]
        )

        level = calculate_skill_level(
            candidate,
            raw_data,
        )

        confidence = calculate_confidence(
            candidate
        )

        skills.append({
            "name": name,
            "category": candidate["category"],
            "level": level,
            "confidence": confidence,
            "sources": sorted({
                evidence["source_type"]
                for evidence in candidate["evidence"]
            }),
            "evidence": candidate["evidence"],
            "justification": (
                "Level und Confidence wurden aus den "
                "vorhandenen Nachweisen berechnet."
            ),
        })

    # Remove duplicate skills.
    unique: dict[str, dict[str, Any]] = {}

    for skill in skills:
        existing = unique.get(skill["name"])

        if existing is None:
            unique[skill["name"]] = skill
            continue

        # Keep the stronger evidence result.
        if (
            skill["confidence"],
            skill["level"],
        ) > (
            existing["confidence"],
            existing["level"],
        ):
            unique[skill["name"]] = skill

    return {
        "skills": list(unique.values())
    }


# ============================================================
# MISSING SKILLS
# ============================================================

def build_missing_skills(
    skill_profile: dict[str, Any],
    job_profile: dict[str, Any],
) -> list[dict[str, Any]]:

    current = {
        skill["name"]: skill
        for skill in skill_profile["skills"]
    }

    result = []

    for requirement in job_profile["required_skills"]:
        name = requirement["skill"]
        target_level = requirement["target_level"]
        importance = requirement["importance"]

        skill = current.get(name)

        if skill is None:
            result.append({
                "skill": name,
                "status": "not_verified",
                "importance": importance,
                "reason": (
                    "Für dieses Skill liegen derzeit "
                    "keine ausreichenden Nachweise vor."
                ),
                "evidence_gap": (
                    "Keine verifizierbare Evidenz vorhanden."
                ),
            })
            continue

        if skill["level"] < target_level:
            result.append({
                "skill": name,
                "status": "partially_demonstrated",
                "importance": importance,
                "reason": (
                    f"Aktueller Level {skill['level']} "
                    f"liegt unter dem Ziellevel {target_level}."
                ),
                "evidence_gap": (
                    f"{target_level - skill['level']} "
                    "Punkte bis zum Ziellevel."
                ),
            })

    return sorted(
        result,
        key=lambda item: item["importance"],
        reverse=True,
    )


# ============================================================
# JOB MATCH
# ============================================================

def calculate_job_match(
    skill_profile: dict[str, Any],
    job_profile: dict[str, Any],
) -> int:

    current = {
        skill["name"]: skill
        for skill in skill_profile["skills"]
    }

    weighted_score = 0.0
    total_weight = 0.0

    for requirement in job_profile["required_skills"]:
        skill_name = requirement["skill"]
        target_level = requirement["target_level"]
        weight = requirement["importance"]

        skill = current.get(skill_name)

        if skill is None:
            effective_level = 0
        else:
            # Slightly reduce the effective score when evidence
            # confidence is low.
            effective_level = skill["level"] * (
                0.5
                + 0.5 * skill["confidence"] / 100
            )

        ratio = min(
            effective_level / target_level,
            1.0,
        )

        weighted_score += ratio * weight
        total_weight += weight

    if total_weight == 0:
        return 0

    return round(
        weighted_score / total_weight * 100
    )


def build_skill_graph(
    skill_profile: dict[str, Any],
    ai_analysis: dict[str, Any],
    job_profile: dict[str, Any],
) -> dict[str, Any]:

    nodes_by_name: dict[str, dict[str, str]] = {}

    # Bereits nachgewiesene Skills
    for skill in skill_profile.get("skills", []):
        nodes_by_name[skill["name"]] = {
            "skill": skill["name"],
            "category": skill["category"],
        }

    # Skills aus AI-Relations ergänzen
    for relation in ai_analysis.get("skill_relations", []):
        for skill_name in (
            relation["from_skill"],
            relation["to_skill"],
        ):
            normalized_name = normalize_skill_name(skill_name)

            if normalized_name not in nodes_by_name:
                nodes_by_name[normalized_name] = {
                    "skill": normalized_name,
                    "category": "Other",
                }

    # Zielskills des Berufs ergänzen
    for requirement in job_profile.get("required_skills", []):
        skill_name = normalize_skill_name(
            requirement["skill"]
        )

        if skill_name not in nodes_by_name:
            nodes_by_name[skill_name] = {
                "skill": skill_name,
                "category": "Target Skill",
            }

    edges = []

    for relation in ai_analysis.get(
        "skill_relations",
        [],
    ):
        edges.append({
            "from_skill": normalize_skill_name(
                relation["from_skill"]
            ),
            "to_skill": normalize_skill_name(
                relation["to_skill"]
            ),
            "relationship": relation["relationship"],
            "reason": relation["reason"],
        })

    return {
        "nodes": list(nodes_by_name.values()),
        "edges": edges,
    }

# ============================================================
# MAIN ENGINE
# ============================================================

def build_fluffelskills_profile(
    ai_analysis: dict[str, Any],
    raw_data: dict[str, Any],
    job_profile: dict[str, Any],
) -> dict[str, Any]:

    skill_profile = build_skill_profile(
        ai_analysis,
        raw_data,
    )

    missing_skills = build_missing_skills(
        skill_profile,
        job_profile,
    )

    job_match = calculate_job_match(
        skill_profile,
        job_profile,
    )

    return {
        "skill_profile": skill_profile,
        "skill_graph": build_skill_graph(
            skill_profile=skill_profile,
            ai_analysis=ai_analysis,
            job_profile=job_profile,
        ),
        "strengths": ai_analysis.get(
            "strength_candidates",
            [],
        ),
        "missing_skills": missing_skills,
        "job_match": job_match,
        "profile_improvements": ai_analysis.get(
            "profile_improvements",
            [],
        ),
    }