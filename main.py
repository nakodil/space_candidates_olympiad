import os
import csv


def read_csv_files(directory):
    headings_template = {
        'id': 'id',
        'name': 'имя',
        'surname': 'фамилия',
        'height': 'рост',
        'weight': 'вес',
        'eyesight': 'зрение',
        'age': 'возраст',
        'education': 'образование',
        'english_language': 'знание английского'
    }
    all_filenames = os.listdir(directory)
    csv_filenames = [
        filename for filename in all_filenames
        if filename.endswith('.csv')
    ]
    all_data = []

    for filename in csv_filenames:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='#')
            file_headings = next(reader)

            if not check_headings(file_headings, headings_template):
                print(
                    f'{file_path} не содержит нужных заголовков, игнорирую'
                )
                continue

            heading_indices = get_heading_indices(file_headings)
            desired_indices = get_desired_indices(
                heading_indices, headings_template
            )
            extract_data(reader, all_data, desired_indices)

    return headings_template, all_data


def check_headings(file_headings, headings_template):
    return all(field in file_headings for field in headings_template)


def get_heading_indices(file_headings):
    return {heading: index for index, heading in enumerate(file_headings)}


def get_desired_indices(heading_indices, headings_template):
    return [heading_indices[heading] for heading in headings_template]


def extract_data(reader, all_data, desired_indices):
    for row in reader:
        reordered_row = [row[i] for i in desired_indices]
        all_data.append(' '.join(reordered_row))


def print_data(headings_template, all_data):
    print(' '.join(headings_template.values()))
    for data in all_data:
        print(data)


def main():
    directory = r'C:\Users\Me\Desktop\python_dev\space_candidate\Архив'
    headings_template, all_data = read_csv_files(directory)
    print_data(headings_template, all_data)


if __name__ == "__main__":
    main()
