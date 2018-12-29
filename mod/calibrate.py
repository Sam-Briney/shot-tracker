# import json
# from random import randint
# import os
# import os.path
# import cv2
#
# def saveCal(image, lower_bound, upper_bound):
#     max_saved = 14
#
#     try:
#         previous = open("color-calibrations/list.json", "r+")
#         data = json.loads(previous.read())
#         previous.close()
#     except:
#         data = {"calibrations": []}
#
#     try:
#         os.remove("color-calibrations/list.json")
#     except:
#         print "lost calibrations"
#
#     if len(data["calibrations"]) > max_saved:
#         os.remove(data["calibrations"][max_saved][0])
#         data["calibrations"].pop()
#
#     imgPath = "color-calibrations/images/0.jpg"
#     while os.path.isfile(imgPath):
#         imgPath = "color-calibrations/images/" + str(randint(0, 1000)) + ".jpg"
#
#     data["calibrations"].insert(0, [imgPath, lower_bound, upper_bound])
#     cv2.imwrite(imgPath, image)
#
#     newList = open("color-calibrations/list.json", "w")
#
#     newList.write(json.dumps(data))
#     newList.close()
#
# def getCalibrations():
#     File = open("color-calibrations/list.json", "r")
#
#     calibrations = json.loads(File.read())
#     File.close();
#     return calibrations
