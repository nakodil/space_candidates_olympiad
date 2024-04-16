import os
import csv


def has_required_fields(headings, required_fields):
    return all(field in headings for field in required_fields)


def reorder_csv(file_path, headings_order, data_accumulator):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='#')
        headings = next(reader)  # Читаем заголовки

        if not has_required_fields(headings, headings_order):
            print(f'Файл {file_path} не содержит нужных заголовков, игнорирую')
            return

        heading_indices = {heading: index for index, heading in enumerate(headings)}
        desired_indices = [heading_indices[heading] for heading in headings_order]

        for row in reader:
            reordered_row = [row[i] for i in desired_indices]
            data_accumulator.append(' '.join(reordered_row))


headings_order = ['id', 'name', 'surname', 'height', 'weight', 'eyesight', 'age', 'education', 'english_language']
headings_translation = ['id', 'имя', 'фамилия', 'рост', 'вес', 'зрение', 'возраст', 'образование', 'знание английского']
main_directory = os.path.dirname(os.path.abspath(__file__))
archive_directory = os.path.join(main_directory, 'Архив')
all_data = []

for filename in os.listdir(archive_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(archive_directory, filename)
        reorder_csv(file_path, headings_order, all_data)

os.system('cls')
print(' '.join(headings_translation))
for data in all_data:
    print(data)
