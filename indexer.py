import os
import sys
import re
import shutil
from pathlib import Path
from datetime import date

VAULT_PATH = os.environ.get('VAULT_PATH', os.path.join(os.getcwd(), 'vault'))
SOURCE_PATH = os.environ.get('SOURCE_PATH', os.path.join(os.getcwd(), 'source'))

MODULE_KEYWORDS = {
    'helpdesk': ['helpdesk', 'тикет', 'обращение', 'sla', 'тп', 'поддержка'],
    'knowledgebase': ['база знаний', 'статья', 'знаний', 'knowledge'],
    'library': ['библиотек', 'книг', 'библиотек'],
    'branding': ['брендирован', 'дизайн', 'тема', 'figma', 'зефир', 'legacy'],
    'gamification': ['геймификац', 'балл', 'рейтинг', 'бонус', 'доска почета'],
    'homepage': ['главная страниц', 'виджет', 'баннер', 'новост'],
    'hints': ['подсказк', 'hint', 'онбординг'],
    'workplaces': ['карта офис', 'бронирован', 'рабочее мест'],
    'university': ['университет', 'курс', 'компетенци', 'обучени'],
    'multilang': ['мультиязычн', 'перевод', 'multilang'],
    'notifications': ['уведомлен', 'notification'],
    'polls': ['опрос', 'голосован'],
    'assessment360': ['оценка 360', 'assessment360', 'компетенци', 'оценк'],
    'goals-tree': ['дерев', 'цел', 'goals'],
    'goals-cascade': ['каскад', 'цел', 'goals'],
    'mediagallery': ['галере', 'медиа', 'фото', 'видео'],
}

MODULE_NAMES = {
    'helpdesk': 'HelpDesk',
    'knowledgebase': 'База знаний',
    'library': 'Библиотека',
    'branding': 'Брендирование Битрикс24',
    'gamification': 'Геймификация',
    'homepage': 'Главная страница',
    'hints': 'Интерактивные подсказки',
    'workplaces': 'Карта офиса + Бронирование',
    'university': 'Корпоративный университет',
    'multilang': 'Мультиязычность',
    'notifications': 'Настройка уведомлений',
    'polls': 'Опросы',
    'assessment360': 'Оценка 360',
    'goals-tree': 'Управление целями. Дерево',
    'goals-cascade': 'Управление целями. Каскад',
    'mediagallery': 'Фото и видео галерея',
}


def detect_module(content: str, filepath: str) -> tuple:
    content_lower = content.lower()
    path_lower = filepath.lower()
    
    best_match = None
    best_score = 0
    
    for slug, keywords in MODULE_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in content_lower:
                score += content_lower.count(kw)
            if kw in path_lower:
                score += 2
        if score > best_score:
            best_score = score
            best_match = slug
    
    if best_match and best_match in MODULE_NAMES:
        return best_match, MODULE_NAMES[best_match]
    
    return 'unknown', 'Unknown'


def extract_title(content: str) -> str:
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return 'Untitled'


def vault_file_exists(vault_filename: str, vault_dir: str) -> bool:
    filepath = os.path.join(vault_dir, 'Instructions', vault_filename)
    return os.path.exists(filepath)


def create_vault_file(content: str, filepath: str, vault_dir: str) -> str:
    title = extract_title(content)
    module_slug, module_name = detect_module(content, filepath)
    today = date.today().isoformat()
    
    vault_filename = f"{module_name} - {title}.md"
    vault_filepath = os.path.join(vault_dir, 'Instructions', vault_filename)
    
    frontmatter = f"""---
title: "{module_name} - {title}"
module: "{module_name}"
type: instruction
version: ""
created: {today}
updated: {today}
tags:
  - type/instruction
  - module/{module_slug}
related: []
---

# {module_name} - {title}

**Модуль:** [[Module - {module_name}]]

"""
    vault_content = frontmatter + content
    
    os.makedirs(os.path.join(vault_dir, 'Instructions'), exist_ok=True)
    with open(vault_filepath, 'w', encoding='utf-8') as f:
        f.write(vault_content)
    
    print(f"  Created: Instructions/{vault_filename}")
    return vault_filename


def update_moc(vault_dir: str, module_name: str, vault_filename: str):
    moc_path = os.path.join(vault_dir, 'MOC - Инструкции.md')
    if not os.path.exists(moc_path):
        print(f"  Warning: MOC file not found at {moc_path}")
        return
    
    with open(moc_path, 'r', encoding='utf-8') as f:
        moc_content = f.read()
    
    title_without_ext = vault_filename.replace('.md', '')
    wikilink = f"- [[{title_without_ext}]]"
    
    if wikilink in moc_content:
        print(f"  Already in MOC: {wikilink}")
        return
    
    section_header = f"### {module_name}"
    if section_header not in moc_content:
        print(f"  Warning: Section '{section_header}' not found in MOC")
        return
    
    idx = moc_content.find(section_header)
    insert_pos = idx + len(section_header)
    moc_content = moc_content[:insert_pos] + '\n' + wikilink + moc_content[insert_pos:]
    with open(moc_path, 'w', encoding='utf-8') as f:
        f.write(moc_content)
    print(f"  Updated MOC: added {wikilink}")


def update_module_file(vault_dir: str, module_name: str, vault_filename: str):
    module_file = os.path.join(vault_dir, 'Modules', f'Module - {module_name}.md')
    if not os.path.exists(module_file):
        print(f"  Warning: Module file not found at {module_file}")
        return
    
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_without_ext = vault_filename.replace('.md', '')
    wikilink = f"- [[{title_without_ext}]]"
    
    if wikilink in content:
        print(f"  Already in module file: {wikilink}")
        return
    
    instructions_section = '## Инструкции'
    if instructions_section in content:
        insert_pos = content.find(instructions_section) + len(instructions_section)
        content = content[:insert_pos] + '\n' + wikilink + content[insert_pos:]
    else:
        content += f'\n\n## Инструкции\n{wikilink}\n'
    
    with open(module_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Updated module file: {module_file}")


def main():
    source_dir = SOURCE_PATH
    vault_dir = VAULT_PATH
    
    print(f"Source: {source_dir}")
    print(f"Vault: {vault_dir}")
    
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory not found: {source_dir}")
        sys.exit(1)
    if not os.path.isdir(vault_dir):
        print(f"Error: Vault directory not found: {vault_dir}")
        sys.exit(1)
    
    md_files = []
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    
    if not md_files:
        print("No .md files found in source")
        return
    
    print(f"Found {len(md_files)} .md files to index")
    
    for filepath in md_files:
        rel_path = os.path.relpath(filepath, source_dir)
        print(f"\nProcessing: {rel_path}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title = extract_title(content)
        module_slug, module_name = detect_module(content, rel_path)
        vault_filename = f"{module_name} - {title}.md"
        
        if vault_file_exists(vault_filename, vault_dir):
            print(f"  Skipping (already in vault): Instructions/{vault_filename}")
            continue
        
        vault_filename = create_vault_file(content, rel_path, vault_dir)
        update_moc(vault_dir, module_name, vault_filename)
        update_module_file(vault_dir, module_name, vault_filename)
    
    print(f"\n✅ Done. Indexed {len(md_files)} files.")


if __name__ == '__main__':
    main()
