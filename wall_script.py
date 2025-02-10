import cv2
import numpy as np

# Загружаем изображение
img = cv2.imread("wallpaper3.png")
img_h, img_w = img.shape[:2]  # Размеры оригинального изображения

# Размер окна просмотра
win_h, win_w = 600, 800  # Настроить под экран
scroll_y, scroll_x = 0, 0  # Смещение
step = 50  # Шаг прокрутки

# Глобальные переменные для рисования
drawing = False
start_point = None
rectangles = []

def draw_rectangle(event, x, y, flags, param):
    global start_point, drawing, img, scroll_y, scroll_x

    real_x = x + scroll_x  # Коррекция X
    real_y = y + scroll_y  # Коррекция Y

    if event == cv2.EVENT_LBUTTONDOWN:  # Начало рисования
        drawing = True
        start_point = (real_x, real_y)

    elif event == cv2.EVENT_MOUSEMOVE:  # Временный прямоугольник
        if drawing:
            img_temp = img.copy()
            cv2.rectangle(img_temp, start_point, (real_x, real_y), (0, 255, 0), 2)
            show_image(img_temp)

    elif event == cv2.EVENT_LBUTTONUP:  # Завершение рисования
        drawing = False
        end_point = (real_x, real_y)
        width, height = abs(end_point[0] - start_point[0]), abs(end_point[1] - start_point[1])

        rectangles.append((start_point, end_point, width, height))
        print(f"Wall({x}, {y}, {width}, {height}, texture_path, walls_group),")

        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
        show_image(img)

def scroll(event, x, y, flags, param):
    global scroll_y, scroll_x
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Колесо вверх
            if cv2.waitKey(1) & 0xFF == ord("s"):  # Shift + колесо = горизонтальная прокрутка
                scroll_x = max(0, scroll_x - step)
            else:
                scroll_y = max(0, scroll_y - step)
        else:  # Колесо вниз
            if cv2.waitKey(1) & 0xFF == ord("s"):  # Shift + колесо = горизонтальная прокрутка
                scroll_x = min(img_w - win_w, scroll_x + step)
            else:
                scroll_y = min(img_h - win_h, scroll_y + step)
        show_image(img)

def show_image(image):
    """ Отображение части изображения с учетом прокрутки """
    cropped = image[scroll_y:scroll_y + win_h, scroll_x:scroll_x + win_w]
    cv2.imshow("Scrollable Image", cropped)

cv2.namedWindow("Scrollable Image")
cv2.setMouseCallback("Scrollable Image", draw_rectangle)

show_image(img)

# Главный цикл
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("w"):  # Прокрутка вверх
        scroll_y = max(0, scroll_y - step)
    elif key == ord("s"):  # Прокрутка вниз
        scroll_y = min(img_h - win_h, scroll_y + step)
    elif key == ord("a"):  # Прокрутка влево
        scroll_x = max(0, scroll_x - step)
    elif key == ord("d"):  # Прокрутка вправо
        scroll_x = min(img_w - win_w, scroll_x + step)

    show_image(img)

cv2.destroyAllWindows()
