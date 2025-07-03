import sys
from collections import defaultdict

def parse_log_line(line: str) -> dict:
        try:
            line_parts = line.strip().split(" ", 3)
            data, time, level, message = line_parts
            return {"data": data, "time": time, "level": level.upper(), "message": message}
       
        except ValueError:
            print(f"Невірний формат рядка логу: {line.strip()}")
            return {}
        

def load_logs(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding= 'utf-8') as file:
            list_of_lines = file.readlines()
        parsed_logs = []
        for line in list_of_lines:
            parsed = parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)
        return parsed_logs
    
    except FileNotFoundError:  
        print(f"Файл {file_path} не знайдено.")
        return []
   
    except Exception as e:
        print(f"Помилка при читанні файлу {file_path}: {e}")
        return []

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log["level"] == level, logs))

def count_logs_by_level(logs: list) -> dict:
    level_count = defaultdict(int)
    for log in logs:
        level_count[log["level"]] += 1
    return dict(level_count)

def display_log_counts(counts: dict):
    print (f"""\nРівень логування | Кількість
-----------------|----------
INFO             | {counts.get("INFO", 0)}
DEBUG            | {counts.get("DEBUG", 0)}
ERROR            | {counts.get("ERROR", 0)}
WARNING          | {counts.get("WARNING", 0)}""")

def display_filtered_logs(logs: list, level: str):
    print(f"\nДеталі логів для рівня '{level}':")
    for log in logs:
        print(f"{log["data"]} {log["time"]} - {log["message"]}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_лог_файлу> [рівень_логування]")

    else:
        file_path = sys.argv[1]
        level_filter = sys.argv[2].upper() if len(sys.argv) > 2 else None
        list_of_logs = load_logs(file_path)
        if list_of_logs:
            logs_count = count_logs_by_level(list_of_logs)
            display_log_counts(logs_count)

            if level_filter:
                filtered_logs = filter_logs_by_level(list_of_logs, level_filter)
                if filtered_logs:
                    display_filtered_logs(filtered_logs, level_filter)
                else:
                    print(f"\nЖодних записів для рівня '{level_filter}' не знайдено.")

        else:
            print("Логи не знайдено або файл порожній.")

if __name__ == "__main__":
    main()