# h) Segmentation using Region Grow

class Point(object):
 def __init__(self,x,y):
  self.x = x
  self.y = y

 def getX(self):
  return self.x
 def getY(self):
  return self.y

def getGrayDifference(img,present_point,temperory_point):
 return abs(int(img[present_point.x,present_point.y]) - int(img[temperory_point.x,temperory_point.y]))

def selectingDots(p):
 if p != 0:
  connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), \
     Point(0, 1), Point(-1, 1), Point(-1, 0)]
 else:
  connects = [ Point(0, -1), Point(1, 0),Point(0, 1), Point(-1, 0)]
 return connects

def regionGrow(img,seeds,thresh,p = 1):
 height, weight = img.shape
 seedMark = numpy.zeros(img.shape)
 seedList = []
 for seed in seeds:
  seedList.append(seed)
 label = 255
 connects = selectingDots(p)
 while(len(seedList)>0):
  present_point = seedList.pop(0)

  seedMark[present_point.x,present_point.y] = label
  for i in range(8):
   tmpX = present_point.x + connects[i].x
   tmpY = present_point.y + connects[i].y
   if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
    continue
   grayDiff = getGrayDifference(img,present_point,Point(tmpX,tmpY))
   if grayDiff < thresh and seedMark[tmpX,tmpY] == 0:
    seedMark[tmpX,tmpY] = label
    seedList.append(Point(tmpX,tmpY))
 return seedMark

def rgb_to_grayscale(pixel):
    R, G, B =pixel[0], pixel[1], pixel[2]
    return 0.2989 * R + 0.5870 * G + 0.1140 * B

def convertToGrayScale(img_array):
    img_width =len(img_array[0])
    img_height = len(img_array)
    out = numpy.empty([img_height, img_width])
    for i in range(0, img_height):
        for j in range(0, img_width):
            out[i][j] = rgb_to_grayscale(img_array[i][j])
    return out

def medianFilter(img):
    height,width = img.shape[0:2]
    mask = numpy.ones((3,3), numpy.float32)/9
    data_final = []
    data_final = numpy.zeros((len(img),len(img[0])))
    for i in range(2, height - 1):
        for j in range(2, width - 1):
            try:
                region = img[i-1: i+2, j-1: j+2]
                data_final[i][j] = numpy.median(region)
            except:
                pass
    return data_final


img = cv2.imread('dashcam_view_1.jpg')
img_noice_filtered = medianFilter(convertToGrayScale(img))

# Road
seeds = [Point(700,870)]
binaryImg = regionGrow(img_noice_filtered,seeds,4)
# cv2_imshow(binaryImg)
cv2.imwrite('image_segmented_Road.png', binaryImg)

# Car 1
seeds = [Point(570,790), Point(530,840), Point(510,840), Point(486,840), Point(535,896), Point(542,823)]
binaryImg = regionGrow(img_noice_filtered,seeds,4)
# cv2_imshow(binaryImg)
cv2.imwrite('image_segmented_Car1_onRoad.png', binaryImg)

# Car 2
# seeds = [Point(900,850), Point(960,1300)]
binaryImg = regionGrow(img_noice_filtered,seeds,4)
# cv2_imshow(binaryImg)
cv2.imwrite('image_segmented_FrontCar.png', binaryImg)

# Sky
seeds = [Point(220,1160), Point(160,1300), Point(80,1500), Point(160,1820)]
binaryImg = regionGrow(img_noice_filtered,seeds,3)
# cv2_imshow(binaryImg)
cv2.imwrite('image_segmented_Sky.png', binaryImg)

# Others
seeds = [Point(350,160)]
binaryImg = regionGrow(img_noice_filtered,seeds,6)
# cv2_imshow(binaryImg)
cv2.imwrite('image_segmented_OthersSegments.png', binaryImg)