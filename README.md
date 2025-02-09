# Название проекта

В процессе

## Содержание

- [Технологии](#технологии)
- [Тестирование](#тестирование)
- [Contributing](#contributing)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии

- [Python](https://www.python.org/)
- [PyGame](https://www.pygame.org/)

## Описание проекта

Наш проект представляет собой 2D survival-horror написаный на pygame, в ней присутствует:

- полуоткрытый игровой мир
- NPC
- диалоги
- боевка
- и многое другое

## Разработка

По началу разработка шла очень быстро, но потом замедлилась мз-за проблем, таких как камера, открытый мир и боевая система.
Решали же мы проблемы по мере поступления, сначало была камера, по началу Даниил написал рабочий код другой игры и не смог сопоставить его с основным.

Работа камеры:

```python
class Camera:
    def __init__(self, width, height):
        # Инициализация камеры с заданной шириной и высотой
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Применение смещения камеры к сущности
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Обновление позиции камеры в зависимости от положения цели
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Ограничение прокрутки до размеров карты
        x = min(0, x)  # левая граница
        y = min(0, y)  # верхняя граница
        x = max(-(self.width - SCREEN.get_width()), x)  # правая граница
        y = max(-(self.height - SCREEN.get_height()), y)  # нижняя граница

        # Установка новой позиции камеры
        self.camera = pygame.Rect(x, y, self.width, self.height)
```

Боевая система,
Открытый мир был связан с камерой, поэтому его ращработк замедлилась из-за Даниила, но потом пришла новая проблема, мы не могли нарисовать карту

## Структура

```
│── app/                      # Основная папка с кодом игры
│   │── fighting/             # Модуль, отвечающий за боевую систему
│   │   │── fighting_systems.py  # Основная логика боевой системы
│   │   │── main_fighters.py     # Основные боевые персонажи
│   │   │── hero.py              # Класс героя
│   │   │── system.py            # Вспомогательные функции и механики
│   │   │── world.py             # Мир игры (карта, окружение)
│
│── data/                     # Папка для ресурсов (текстуры, музыка и т. д.)
│── main.py                   # Главный файл, запускающий игру
│── README.md                 # Документация проекта
│── requirements.txt          # Список зависимостей
│── .gitignore                # Файл игнорирования Git
```

### Установка зависимостей и требования

Убедитесь, что у вас установлен Python 3 и Pygame. Установите зависимости командой:

```bash
pip install -r requirements.txt
```

### Запуск

```bash
python main.py
```

## Contributing

Если хотите помочь с разработкой проекта или оповестить о баге используйте [Github](https://github.com/) или пишите на почту ***tebezdesneradi@gmail.com***

### Зачем вы разработали этот проект?

Для того чтобы отточить свои умения в Pygame и Python, а также для [Яндекс Лицея](https://lyceum.yandex.ru/) и показать возможности Pygame

## To do

* [X] Сделать основы Главного героя
* [X] Сделать камеру с плавным перемещением
* [X] Сделать боевую систему и злодеев
* [X] Написать сюжет и диалоги
* [X] Создать игровую карту
* [X] Добавить крутое README
* [X] Сделать презентацию
* [ ] Защитить проект

## Команда проекта

Оставьте пользователям контакты и инструкции, как связаться с командой разработки.

- Петров Михаил - Самый лучший чел на свете
- Кулевой Даниил - Лох который сидел со сгровшим процом 3 недели

## Источники

Мы вдохновлялись игрой [Undertale](https://store.steampowered.com/app/391540/Undertale/) и Нашей больной фантазией
