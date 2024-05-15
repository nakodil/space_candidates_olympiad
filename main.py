import os
import csv


def read_csv_files(directory) -> list[dict]:
    all_candidates = []
    csv_filenames = [
        filename for filename in os.listdir(directory)
        if filename.endswith('.csv') or filename.endswith('.CSV')
    ]
    print(f'В директории {directory} найдено {len(csv_filenames)} CSV файлов.')
    if not csv_filenames:
        return
    for filename in csv_filenames:
        file_path = os.path.join(directory, filename)
        current_file_candidates = get_candidates(file_path)
        print(f'Из файла отобрано кандидатов: {len(current_file_candidates)}')
        all_candidates += current_file_candidates
    return all_candidates


def get_candidates(file_path: str) -> list[dict]:
    headings_template = [
        'id',
        'name',
        'surname',
        'height',
        'weight',
        'eyesight',
        'age',
        'education',
        'english_language'
    ]

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='#')
        headings = next(reader)
        if not all(header in headings_template for header in headings):
            print(f'\nОшибка! {file_path} не содержит нужных заголовков')
            return dict()
        else:
            print(f'\nОтбор кандидатов из {file_path}:')

        candidates = []
        for row in reader:
            candidate_data = [col for col in row]
            ordered_candidate = {key: None for key in headings_template}
            for key, value in zip(headings, candidate_data):
                ordered_candidate[key] = value

            if candidate_is_ok(ordered_candidate):
                candidates.append(ordered_candidate)
    return candidates


def candidate_is_ok(candidate: dict) -> bool:
    print(f' - Кандидат {candidate["name"]} {candidate["surname"]}', end=' ')
    if int(candidate['age']) < 20:
        print('не прошел провекру: возраст меньше 20')
        return False
    if int(candidate['age']) > 59:
        print('не прошел провекру: возраст больше 59')
        return False
    if int(candidate['height']) < 150:
        print('не прошел провекру: рост меньше 150')
        return False
    if int(candidate['height']) > 190:
        print('не прошел провекру: рост больше 190')
        return False
    if int(candidate['weight']) < 50:
        print('не прошел провекру: вес меньше 50')
        return False
    if int(candidate['weight']) > 90:
        print('не прошел провекру: вес больше 90')
        return False
    if float(candidate['eyesight']) != 1.0:
        print('не прошел провекру: зрение не 1.0')
        return False
    if candidate['education'] not in ('PhD', 'Master'):
        print(
            'не прошел провекру: образование не магистр или не кандидат/доктор'
        )
        return False
    if candidate['english_language'] != 'true':
        print('не прошел провекру: нет знания английсткого языка')
        return False
    print('— OK')
    return True


def get_sorted_candidates(candidates: list[dict]) -> list[dict]:
    age_preferred = []
    age_unpreferred = []
    for candidate in candidates:
        age = int(candidate['age'])
        if 27 <= age <= 37:
            age_preferred.append(candidate)
        else:
            age_unpreferred.append(candidate)
    age_preferred.sort(key=lambda dict: (dict['name'], dict['surname']))
    age_unpreferred.sort(key=lambda dict: (dict['name'], dict['surname']))
    return age_preferred + age_unpreferred


def regenerate_ids(candidates: list[dict]) -> list[dict]:
    for i, candidate in enumerate(candidates, start=1):
        candidate['id'] = str(i)
    return candidates


def save_to_csv(directory: str, candidates: list[dict]) -> None:
    if not candidates:
        print('Нет кандидатов для сохранения, программа завершена.')
        return
    file_path = os.path.join(directory, 'result.csv')
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='#')
            for candidate in candidates:
                candidate = {
                    key: value for key, value in candidate.items()
                    if key not in ['eyesight', 'age', 'english_language']
                }
                candidate_str = candidate.values()
                writer.writerow(candidate_str)
    except PermissionError:
        print(f'\nОшибка! Закройте файл {file_path} и повторите попытку.')
    else:
        print(f'\nВсего отобрано кандидатов: {len(candidates)}')
        print(f'Отобранные кандидаты сохранены в {file_path}')


def main():
    os.system('cls')
    directory = input('Введите абсолютынй путь к директории с файлами: ')
    candidates = read_csv_files(directory)
    if not candidates:
        print('Нет файлов с данными о кандидатах, программа завершена.')
        return
    candidates = get_sorted_candidates(candidates)
    candidates = regenerate_ids(candidates)
    save_to_csv(directory, candidates)


if __name__ == "__main__":
    candidates = []
    main()
