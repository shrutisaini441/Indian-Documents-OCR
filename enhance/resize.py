import cv2


def resized_image(image):
    if image.shape[1] > 4000 or image.shape[0] > 3000:
        resized = cv2.resize(image, None, fx=0.15, fy=0.15, interpolation=cv2.INTER_AREA)
    elif image.shape[1] > 3000 or image.shape[0] > 2000:
        resized = cv2.resize(image, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
    elif image.shape[1] > 2000 or image.shape[0] > 1200:
        resized = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    elif image.shape[1] > 1000 or image.shape[0] > 800:
        resized = cv2.resize(image, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
    else:
        resized = image
    return resized
