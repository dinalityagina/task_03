# Домашнее задание №3 Веб-сервис 
Курс “Python для разработки”

## Установка
1.  Клонируйте репозиторий:
    ```
    git clone https://github.com/your-username/task_03.git
    cd task_03
    ```
2.  Установите необходимые библиотеки:
    ```
    pip install -r requirements.txt
    ```
3. Запуск бэкенда:
    ```
    uvicorn backend.main:app --reload 
    ```    
4. Запуск UI:
    ```
    streamlit run app.py
    ```    
## Структура проекта
-   `/backend/data.csv`: Исходный датасет.
-   `/backend/main.py`: бэкэнд сервер 
-   `/fronend/app.py`: Клиент 
-   `requirements.txt`: Список зависимостей.

## Данные
Используется датасет (https://drive.google.com/file/d/1mDP_tVimEehAKV1va-m1SaKMGs7de8JP/view) RU_Electricity_Market_PZ_dayahead_price_volume.csv 

## Лицензия
Этот проект распространяется под лицензией MIT.requirements.txt