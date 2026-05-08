from pathlib import Path


def load_text_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    return file_path.read_text(encoding="utf-8")


def load_skill(skill_name: str) -> str:
    return load_text_file(f"app/skills/{skill_name}.md")


def load_knowledge(file_name: str) -> str:
    return load_text_file(f"app/knowledge/{file_name}.md")


def load_prompt(prompt_name: str) -> str:
    return load_text_file(f"app/prompts/{prompt_name}.md")