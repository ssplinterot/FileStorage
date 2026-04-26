"""
• os.path.isdir(filepath) — встроенный метод, который проверяет, является ли указанный путь папкой.
• os.listdir(filepath) — читает содержимое папки и выдаёт список имен.
• jsonify — функция из Flask, которая берет питоновский список или словарь и превращает его в правильный HTTP-ответ в формате JSON.

http://localhost:8080/test_folder/ -- проверка католога
http://localhost:8080/my_first_file.txt -- для файла

"""

from flask import Flask, request, send_file, jsonify
import os, datetime

app = Flask(__name__)

STORAGE_DIR = os.path.abspath("storage")# Создаем отдельную папку для файлов, чтобы не работать в корне проекта
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def get_safe_path(filepath):
    # Превращаем путь в безопасный: убираем ".." и склеиваем с папкой storage
    safe_path = os.path.normpath(os.path.join(STORAGE_DIR, filepath))
    # Проверка: не пытается ли путь выйти за пределы STORAGE_DIR
    if not safe_path.startswith(STORAGE_DIR):
        return None
    return safe_path

@app.route('/<path:filepath>', methods=["PUT"])
def upload_file(filepath):
   target_path = get_safe_path(filepath)
   if not target_path:
        return "Доступ запрещен", 403
   
   os.makedirs(os.path.dirname(target_path), exist_ok=True)# Создаем подпапки, если их нет
   
   with open(target_path, 'wb') as f: # 'wb' (write binary). Записывем данные в файл. Открываем файл по пути filepath 
            #для записи ('w') в бинарном режиме ('b')  
            f.write(request.data) # Записываем данные на диск
            return "Файл успешно загружен\n", 201 # Возвращаем текст и Код 201 — файл создан/обновлен
    
"""@app.route('/<path:filepath>', methods=["GET"])
def download_file(filepath):
    return send_file(filepath) #соединила функцию скачивания чтобы не путалась информация в postman

@app.route('/<path:filepath>', methods=["DELETE"])
def delete_file(filepath):
    if not os.path.exists(filepath): # проверяем, существует ли вообще такой путь на диске
        return "Файл или папка не найдены", 404 
    os.remove(filepath)
    return "Файл успешно удалён\n", 200"""

@app.route('/<path:filepath>', methods=["GET","HEAD", "DELETE"])
def info_or_download_or_delete_file(filepath):
    target_path = get_safe_path(filepath)
    if not target_path:
        return "Доступ запрещен", 403
    
    if not os.path.exists(target_path): # проверяем, существует ли вообще такой путь на диске
        return "Файл или папка не найдены", 404 
    
    if request.method == "DELETE":
       os.remove(target_path)
       return "Файл успешно удалён\n", 200 
    
    if request.method == "HEAD":
        time = os.path.getmtime(target_path) #получение секунд
        readble_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S') # Превращение секунд в читаемую строку (Год-Месяц-День Часы:Минуты:Секунды)
        headers = { #сбор заголовков в словарь
            'FileSize': str(os.path.getsize(target_path)), 
            'FileTime': readble_time
        }
        return "", 200, headers #тело, статус, заголовки   
    
    if os.path.isdir(target_path): #проверяем, папка ли это
        files = os.listdir(target_path) # Если это GET запрос к папке, получаем список файлов
        return jsonify(files) # Превращаем список в JSON и возвращаем      
    return send_file(target_path, as_attachment=True)# Если это GET к файлу, отдаем сам файл. as_attachment=True - для сохранени файла при заходе в браузере

if __name__ == '__main__':
    app.run(debug = True, port = 8080)
        
