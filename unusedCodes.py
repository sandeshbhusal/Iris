''' 
#This can be useful, if we have to use an android device to stream our content. 
resp = requests.get("http://{}:8080/shot.jpg".format(host))
jpg = resp.content
f = cv2.imdecode(np.fromstring(jpg,dtype = np.uint8) , cv2.IMREAD_COLOR)
'''


                    cv2.circle(f, tuple(noseTopPosition), 3, (255, 0, 0), 2)
                    cv2.circle(f, tuple(noseBottomPosition), 3, (255, 0, 0), 2)
                    cv2.line(f, tuple(noseTopPosition), tuple(noseBottomPosition), (0, 255, 0), 2)
                    cv2.line(f, tuple(noseBottomPosition), tuple(noseLeftPixel), (0, 255, 2), 2)   
                    cv2.line(f, tuple(noseBottomPosition), tuple(noseRightPixel), (0, 255, 2), 2)                   
                    cv2.line(f, tuple(noseTopPosition), tuple(rightEye), (255, 0, 0), 2)
                    cv2.line(f, tuple(noseTopPosition), tuple(leftEye), (255, 0, 0), 2)