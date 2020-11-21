import json
from jsonschema import validate, ValidationError, SchemaError
import os
import sys
from prettytable import PrettyTable


x = PrettyTable()
x.field_names = ["Имя схемы", "Имя Таблицы", "Ошибки"]

dir_schema = "schema"
dir_event = "event"
for root, dirs, files in os.walk(dir_schema):
    for file in files:
        with open("schema\\" + file, "r") as read_file_schema:
            schema = json.load(read_file_schema)
        # Перебираем все схемы
        for root, dirs, files_events in os.walk(dir_event):

            for file_event in files_events:
                with open("event\\" + file_event, "r") as read_file_json:
                    data = json.load(read_file_json)

                # Перебираем все таблицы
                try:
                    for idx, item in enumerate(data):
                        try:
                            validate(item, schema)
                            sys.stdout.write("Запись #{}: OK\n".format(idx))
                        except SchemaError as sh:
                            # print("Ошибки в построении схемы")
                            # print(sh)
                            x.add_row([file, file_event, "Ошибки в построении схемы"+sh])
                        except ValidationError as e:
                            error = str(e)
                            linesoferror = error.split('\n')
                            # print(linesoferror[0])
                            x.add_row([file, file_event, linesoferror[0]])

                except TypeError:
                    # print("Файл пустой")
                    x.add_row([file, file_event, "Файл пустой"])

# Создаём отчёт
my_file = open('report.txt', 'w')

text_for_file = x
my_file.write(x.get_string())

my_file.close()
