"""
• os.path.isdir(filepath) — встроенный метод, который проверяет, является ли указанный путь папкой.
• os.listdir(filepath) — читает содержимое папки и выдаёт список имен.
• jsonify — функция из Flask, которая берет питоновский список или словарь и превращает его в правильный HTTP-ответ в формате JSON.
"""

from flask import Flask, request, send_file, jsonify
import os, datetime

app = Flask(__name__)

@app.route('/<path:filepath>', methods=["PUT"])
def upload_file(filepath):
    file_content = request.data #данные которые прислал клиент
    with open(filepath, 'wb') as f: # 'wb' (write binary). Записывем данные в файл. Открываем файл по пути filepath 
            #для записи ('w') в бинарном режиме ('b')  
            f.write(file_content) # Записываем данные на диск
            return "Файл успешно загружен\n", 201 # Возвращаем текст и статус 201 (Created - Создано)
    
"""@app.route('/<path:filepath>', methods=["GET"])
def download_file(filepath):
    return send_file(filepath)""" #соединила функцию скачивания чтобы не путалась информация в postman

@app.route('/<path:filepath>', methods=["DELETE"])
def delete_file(filepath):
    if not os.path.exists(filepath): # проверяем, существует ли вообще такой путь на диске
        return "Файл или папка не найдены", 404 
    os.remove(filepath)
    return "Файл успешно удалён\n", 200

@app.route('/<path:filepath>', methods=["GET","HEAD"])
def info_or_download_file(filepath):
    if not os.path.exists(filepath): # проверяем, существует ли вообще такой путь на диске
        return "Файл или папка не найдены", 404 
    if os.path.isdir(filepath): #проверяем, папка ли это
        files = os.listdir(filepath) # Если это GET запрос к папке, получаем список файлов
        return jsonify(files) # Превращаем список в JSON и возвращаем
    
    if request.method == "HEAD":
     time = os.path.getmtime(filepath) #получение секунд
     readble_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S') # Превращение секунд в читаемую строку (Год-Месяц-День Часы:Минуты:Секунды)
     headers = { #сбор заголовков в словарь
         'FileSize': str(os.path.getsize(filepath)), 
         'FileTime': readble_time
    }
     return "", 200, headers #тело, статус, заголовки    
    return send_file(filepath, as_attachment=True)# Если это GET к файлу, отдаем сам файл. as_attachment=True - для сохранени файла при заходе в браузере

if __name__ == '__main__':
    app.run(debug = True, port = 8080)
        
