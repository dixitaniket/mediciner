import cv2
import os
import numpy as np
import re
from pytesseract import pytesseract

def preprocessing_image(path=None, image=None):
    if path is not None:
        image = cv2.imread(path, 0)
        original_image = cv2.imread(path)
    else:
        image = image
        original_image = image
    dst = cv2.fastNlMeansDenoisingColored(original_image, None, 10, 10, 7, 15)
    #     show_image(dst)
    image = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_MEAN_C, 21, 7)
    countors, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    countors = sorted(countors, key=cv2.contourArea, reverse=True)
    images = []
    for i in range(2):
        x, y, w, h = cv2.boundingRect(countors[i])
        mask = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        cv2.drawContours(mask, [countors[i]], -1, (255, 255, 255), -1)
        image_ = cv2.bitwise_not(image)
        data = cv2.bitwise_and(original_image, original_image, mask=mask)
        cropped_image = data[y:y + h, x:x + w]
        cropped_image_ = cv2.adaptiveThreshold(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY), 255,
                                               cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_MEAN_C, 21, 7)
        images.append([image_, cropped_image_, cropped_image])

    return images


def get_text_predictions(images):
    mapper = {}
    for i in range(len(images[0])):
        data = pytesseract.image_to_string(images[0][i])
        data = data.strip().split("\n")
        print(data)
        data = [re.sub('[?|$|.|!|\'|>|<|_|*|`|~|-]', "", string) for string in data]
        for j in data:
            j = list(j.split(" "))
            for x in j:
                if len(x) == 0 or len(x) == 1:
                    continue
                else:
                    if x not in mapper.keys():
                        mapper[x] = 0
                    else:
                        mapper[x] += 1
    s = ""

    ans = sorted(mapper.items(), key=lambda x: x[1], reverse=True)
    print(ans)
    max_counts=ans[0][1]
    for i in ans:
        if i[1]==max_counts:
            s+=i[0]
            s+=" "
    return s

