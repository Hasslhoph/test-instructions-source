# Тест opencode run с deepseek-v4-flash (попытка 2)

Проверяем что obsidian-indexer с deepseek-v4-flash корректно обрабатывает инструкцию.

## Описание

Этот тест проверяет полный pipeline: пуш в source → GitHub Actions → opencode run → obsidian-indexer → push в knowledge base.

## Ожидаемый результат

- Новый файл появится в Instructions/
- MOC - Инструкции.md обновится
- Modules/Module - {имя}.md обновится
- Коммит от QA Indexer Bot в test-qa-knowledge-base
