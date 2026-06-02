import os
import sys
import re
import json
import shutil
import subprocess
from datetime import date

VAULT_PATH = os.environ.get('VAULT_PATH', os.path.join(os.getcwd(), 'vault'))
SOURCE_PATH = os.environ.get('SOURCE_PATH', os.path.join(os.getcwd(), 'source'))
OPENCODE_MODEL = os.environ.get('OPENCODE_MODEL', 'opencode-go/deepseek-v4-flash')

MODULES = [
    ('helpdesk', 'HelpDesk', 'ithive.helpdesk'),
    ('knowledgebase', 'База знаний', 'ithive.knowledgebase'),
    ('library', 'Библиотека', 'ithive.library'),
    ('branding', 'Брендирование Битрикс24', 'ithive.changeportaldefaultheme'),
    ('gamification', 'Геймификация', 'ithive.gamification'),
    ('homepage', 'Главная страница', 'ithive.homepage'),
    ('hints', 'Интерактивные подсказки', 'ithive.hints'),
    ('workplaces', 'Карта офиса + Бронирование', 'ithive.workplaces'),
    ('university', 'Корпоративный университет', 'ithive.ipr'),
    ('multilang', 'Мультиязычность', 'ithive.b24multilanguage'),
    ('notifications', 'Настройка уведомлений', 'ithive.imsettingsforall'),
    ('polls', 'Опросы', 'ithive.polls'),
    ('assessment360', 'Оценка 360', 'ithive.assessment360'),
    ('goals-tree', 'Управление целями. Дерево', 'ithive.goalsmanagement2'),
    ('goals-cascade', 'Управление целями. Каскад', 'ithive.goalsmanagement'),
    ('mediagallery', 'Фото и видео галерея', 'ithive.mediagallery'),
]

MODULE_NAMES = {slug: name for slug, name, pkg in MODULES}
MODULES_PROMPT = '\n'.join([f'- {slug}: {name} ({pkg})' for slug, name, pkg in MODULES])
TRACKING_FILE = os.path.join(VAULT_PATH, '.indexed_files.json')


def load_indexed():
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as f:
            return set(json.load(f))
    return set()


def save_indexed(indexed_set):
    with open(TRACKING_FILE, 'w') as f:
        json.dump(sorted(indexed_set), f, indent=2)


def extract_title(content: str) -> str:
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else 'Untitled'


def find_opencode() -> str | None:
    for cmd in ['opencode', 'npx', 'opencode.exe']:
        if shutil.which(cmd):
            return cmd
    return None


def analyze_with_ai(filepath: str, content: str, vault_dir: str) -> dict:
    opencode_cmd = find_opencode()
    if not opencode_cmd:
        print('ERROR: opencode CLI not found')
        sys.exit(1)

    prompt = f"""Analyze this instruction file and return ONLY valid JSON.

FILE PATH: {filepath}

CONTENT:
{content[:2000]}

AVAILABLE MODULES:
{MODULES_PROMPT}

CRITICAL: module_name must be EXACTLY as shown in the list above, e.g. "HelpDesk" not "HelpDesk (ithive.helpdesk)". No parentheses, no extra text.

Return ONLY this JSON (no markdown, no code blocks, no extra text):
{{
  "module_slug": "slug from the list above",
  "module_name": "EXACT module name from the list above",
  "title": "short descriptive title (not the full filename, extract the real topic)",
  "description": "one sentence summary of what this instruction covers",
  "related_modules": ["slug1", "slug2"]
}}

If the module is unclear, choose the best match based on keywords and context."""

    try:
        args = [opencode_cmd, 'run', '--dir', vault_dir,
                '--dangerously-skip-permissions',
                '--model', OPENCODE_MODEL,
                '--print-logs', prompt]
        if opencode_cmd == 'npx':
            args = ['npx', '--yes', '@opencode-ai/cli', 'run',
                    '--dir', vault_dir,
                    '--dangerously-skip-permissions',
                    '--model', OPENCODE_MODEL,
                    '--print-logs', prompt]

        result = subprocess.run(args, capture_output=True, text=True, timeout=180)
        stderr_str = result.stderr.strip()

        if result.returncode != 0:
            print(f'  AI analysis failed (exit {result.returncode}): {stderr_str[:300]}')
            sys.exit(1)
    except FileNotFoundError:
        print('ERROR: opencode CLI not found')
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print('ERROR: AI analysis timed out (180s)')
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: AI analysis error: {e}')
        sys.exit(1)

    stdout = result.stdout.strip()
    for pattern in [r'```(?:json)?\s*\n?(.*?)```', r'(\{[\s\S]*?"module_slug"[\s\S]*?\})']:
        match = re.search(pattern, stdout, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    print(f'ERROR: AI response not parseable: {stdout[:300]}')
    sys.exit(1)


def clean_title(title: str, module_name: str) -> str:
    prefix = f'{module_name} - '
    if title.startswith(prefix):
        return title[len(prefix):]
    if title.startswith(module_name):
        return title[len(module_name):].lstrip(' -')
    return title


def vault_file_exists(vault_filename: str) -> bool:
    return os.path.exists(os.path.join(VAULT_PATH, 'Instructions', vault_filename))


def create_vault_file(content: str, title: str, module_slug: str, module_name: str) -> str:
    today = date.today().isoformat()
    title = clean_title(title, module_name)
    vault_filename = f'{module_name} - {title}.md'

    frontmatter = f'''---
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

'''
    vault_content = frontmatter + content

    os.makedirs(os.path.join(VAULT_PATH, 'Instructions'), exist_ok=True)
    with open(os.path.join(VAULT_PATH, 'Instructions', vault_filename), 'w', encoding='utf-8') as f:
        f.write(vault_content)

    print(f'  Created: Instructions/{vault_filename}')
    return vault_filename


def update_moc(module_name: str, vault_filename: str):
    moc_path = os.path.join(VAULT_PATH, 'MOC - Инструкции.md')
    if not os.path.exists(moc_path):
        print(f'  Warning: MOC file not found')
        return

    with open(moc_path, 'r', encoding='utf-8') as f:
        moc_content = f.read()

    title_without_ext = vault_filename.replace('.md', '')
    wikilink = f'- [[{title_without_ext}]]'

    if wikilink in moc_content:
        return

    section_header = f'### {module_name}'
    if section_header not in moc_content:
        print(f'  Warning: Section "{section_header}" not found in MOC')
        return

    idx = moc_content.find(section_header)
    insert_pos = idx + len(section_header)
    moc_content = moc_content[:insert_pos] + '\n' + wikilink + moc_content[insert_pos:]
    with open(moc_path, 'w', encoding='utf-8') as f:
        f.write(moc_content)
    print(f'  Updated MOC: added {wikilink}')


def update_module_file(module_name: str, vault_filename: str):
    module_file = os.path.join(VAULT_PATH, 'Modules', f'Module - {module_name}.md')
    if not os.path.exists(module_file):
        print(f'  Warning: Module file not found: Module - {module_name}.md')
        return

    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()

    title_without_ext = vault_filename.replace('.md', '')
    wikilink = f'- [[{title_without_ext}]]'

    if wikilink in content:
        return

    instructions_section = '## Инструкции'
    if instructions_section in content:
        insert_pos = content.find(instructions_section) + len(instructions_section)
        content = content[:insert_pos] + '\n' + wikilink + content[insert_pos:]
    else:
        content += f'\n\n## Инструкции\n{wikilink}\n'

    with open(module_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Updated module file: Module - {module_name}.md')


def main():
    print(f'Source: {SOURCE_PATH}')
    print(f'Vault: {VAULT_PATH}')
    print(f'Model: {OPENCODE_MODEL}')

    if not os.path.isdir(SOURCE_PATH):
        print(f'Error: Source directory not found: {SOURCE_PATH}')
        sys.exit(1)
    if not os.path.isdir(VAULT_PATH):
        print(f'Error: Vault directory not found: {VAULT_PATH}')
        sys.exit(1)

    indexed_set = load_indexed()

    md_files = []
    for root, dirs, files in os.walk(SOURCE_PATH):
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    if not md_files:
        print('No .md files found in source')
        return

    new_files = [f for f in md_files if os.path.relpath(f, SOURCE_PATH) not in indexed_set]
    print(f'Found {len(md_files)} .md files, {len(new_files)} new, {len(md_files) - len(new_files)} already indexed')

    indexed = 0
    for filepath in new_files:
        rel_path = os.path.relpath(filepath, SOURCE_PATH)
        print(f'\nProcessing: {rel_path}')

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        title = extract_title(content)

        result = analyze_with_ai(rel_path, content, VAULT_PATH)

        ai_slug = result.get('module_slug', '')
        ai_name = result.get('module_name', '')
        ai_title = result.get('title', title)

        for s, n in MODULE_NAMES.items():
            if ai_slug == s or (ai_name and (n.lower() in ai_name.lower() or ai_name.lower() in n.lower())):
                ai_slug, ai_name = s, n
                break

        if ai_slug not in MODULE_NAMES:
            print(f'  ERROR: AI returned unknown module "{ai_name}", slug "{ai_slug}"')
            sys.exit(1)

        module_slug, module_name, title = ai_slug, MODULE_NAMES[ai_slug], clean_title(ai_title, MODULE_NAMES[ai_slug])

        vault_filename = f'{module_name} - {title}.md'

        if vault_file_exists(vault_filename):
            print(f'  Skipping (already in vault): Instructions/{vault_filename}')
            indexed_set.add(rel_path)
            continue

        final_filename = create_vault_file(content, title, module_slug, module_name)
        update_moc(module_name, final_filename)
        update_module_file(module_name, final_filename)
        indexed_set.add(rel_path)
        indexed += 1

    save_indexed(indexed_set)
    print(f'\nDone. Indexed: {indexed}, skipped: {len(new_files) - indexed}')


if __name__ == '__main__':
    main()
