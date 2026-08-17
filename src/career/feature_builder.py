def build_job_text(
    title: str | None,
    skills: set[str],
    description: str | None,
) -> str:
    """Build a weighted text representation of a job."""

    parts: list[str] = []

    if title:
        clean_title = title.strip()
        parts.extend([clean_title] * 3)

    if skills:
        for skill in sorted(skills):
            parts.extend([skill] * 3)

    if description:
        parts.append(description.strip())

    return " ".join(parts).lower()