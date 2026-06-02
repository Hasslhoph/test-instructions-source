# Новая тестовая инструкция

Это тестовый файл для проверки работы автоматической индексации.

## Описание

Проверяем, что GitHub Actions workflow запускается, indexer.py обрабатывает файл, и изменения пушатся в test-qa-knowledge-base.

## Шаги

1. Этот файл пушится в test-instructions-source
2. GitHub Actions запускает indexer.py
3. indexer.py создаёт файл в Instructions/ test-qa-knowledge-base
4. Обновляет MOC и файл модуля
5. Пушит изменения обратно
