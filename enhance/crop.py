import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]
net = cv2.dnn.readNet("/home/decimal/Desktop/CHEQUE/cheque/OCR/app/model/frozen_east_text_detection.pb")


def crop1(image,segmentation=False):
    orig = image.copy()
    (H, W) = image.shape[:2]

    (newW, newH) = (512, 512)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < 0.5:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    boxes = non_max_suppression(np.array(rects), probs=confidences)
    y = []
    x = []
    SegmentedImage = np.zeros(orig.shape)

    for (startX, startY, endX, endY) in boxes:
        box = [startX, startY, endX, endY]
        box = np.array(box).astype(int)

        box[0] = max(box[0] - 10, 0)
        box[1] = max(box[1] - 10, 0)
        box[2] = 500 - max(500 - box[2] - 10, 0)
        box[3] = 500 - max(500 - box[3] - 10, 0)

        startX = int(startX)
        x.append(startX)
        startY = int(startY)
        y.append(startY)
        endX = int(endX)
        x.append(endX)
        endY = int(endY)
        y.append(endY)
        SegmentedImage[int(box[1] * rH):int(box[3] * rH),int(box[0] * rW):int(box[2] * rH), :] = orig[int(box[1] * rH):
                                                                                                      int(box[3] * rH),
                                                                                                 int(box[0] * rW):
                                                                                                 int(box[2] * rH),:]
    y = np.array(y)
    x = np.array(x)
    x_min,y_min = (max(min(x) - 10, 0), max(min(y) - 10, 0))
    x_max,y_max = (500 - max(min(500 - x) - 10, 0), 500 - max(min(500 - y) - 10, 0))

    cv2.imwrite("temp.jpg",SegmentedImage)

    if segmentation:
        return SegmentedImage[int(y_min*rH):int(y_max*rH),int(x_min*rW):int(x_max*rW)].astype('uint8')
    else:
        return orig[int(y_min*rH):int(y_max*rH),int(x_min*rW):int(x_max*rW)].astype('uint8')