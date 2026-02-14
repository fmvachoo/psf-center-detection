# PSF Center Detection

Микросервис для предсказания центра точки функции рассеяния пятна (Point Spread Function) с использованием нейронных сетей.

## Описание

Проект представляет собой веб-приложение на Flask, которое использует обученные модели нейронных сетей для определения координат центра пятна на изображениях. Приложение контейнеризовано с помощью Docker и поддерживает CI/CD.

## Функциональность

- Загрузка изображений в формате PNG (drag & drop или выбор файла)
- Выбор модели из 4 доступных вариантов
- Предсказание координат центра пятна
- Визуализация результата с точкой в центре пятна на изображении
- Текстовое отображение предсказанных координат

## Доступные модели

- `allData_v2`
- `cnn_M_20x_k_4`
- `cnn_M_20x_k_6`
- `cnn_M_20x_k_8`

## Требования

- Python 3.10+
- Docker

## Установка и запуск

### Локальный запуск

```bash
git clone https://github.com/fmvachoo/psf-center-detection
cd psf-center-detection
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate  

pip install -r requirements.txt

python src/app.py
