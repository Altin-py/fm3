#!/usr/bin/env python3
"""
"""
def get_mask(data):
    """ Kantenerkennung und Ausfüllen des umschlossenen Bereichs """
    # Bild glätten
    data = smooth_image(data)
    mask = np.zeros(data.shape)

    # Binärbild erstellen
    binary_img, points = border_canny(data)

    # Konturen finden
    # contours, _ = cv2.findContours(binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area < 12e4 or area > 18e4:
            continue
        cv2.drawContours(mask, contours, i, 255, thickness=-1)

    return mask
