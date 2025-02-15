import cv2
import numpy as np

# Загружаем изображение
img = cv2.imread("data/image/world/map.png")
img_h, img_w = img.shape[:2]  # Размеры оригинального изображения

win_h, win_w = 1000, 1800  # Настроить под экран
scroll_y, scroll_x = 0, 0  # Смещение
step = 50  # Шаг прокрутки

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
        x1, y1 = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])
        x2, y2 = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])
        width, height = x2 - x1, y2 - y1

        rectangles.append((x1, y1, width, height))

        print(f"Plant({x1}, {y1}, {width}, {height}, texture_path, walls_group),")

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        show_image(img)

def scroll(event, x, y, flags, param):
    global scroll_y, scroll_x
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Колесо вверх
            scroll_y = max(0, scroll_y - step)
        else:  # Колесо вниз
            scroll_y = min(img_h - win_h, scroll_y + step)
        show_image(img)

def show_image(image):
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
    elif key == ord("w"):
        scroll_y = max(0, scroll_y - step)
    elif key == ord("s"):
        scroll_y = min(img_h - win_h, scroll_y + step)
    elif key == ord("a"):
        scroll_x = max(0, scroll_x - step)
    elif key == ord("d"):
        scroll_x = min(img_w - win_w, scroll_x + step)

    show_image(img)

cv2.destroyAllWindows()
