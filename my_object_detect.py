import cv2
import tensorflow as tf
import numpy as np
import os,time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_utils
import json
from json import encoder
import pymysql



class my_object_detect(object):
    def gen():
        db = pymysql.connect(host='192.168.0.177', user='root', password = '4321', db='mysql', charset='utf8')
        cur=db.cursor()

        cap = cv2.VideoCapture(0,cv2.CAP_V4L)
        cap.set(3, 640) # set Width
        cap.set(4, 480) # set Height
        cap.set(5, 10)  # set frame


        # Init tf model

        MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09' #fast
        PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb' 
        PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt') 
        NUM_CLASSES = 90 

        fileAlreadyExists = os.path.isfile(PATH_TO_CKPT) 

        if not fileAlreadyExists:
            print('Model does not exsist !')
            exit

        # LOAD GRAPH
        print('Loading...')
        detection_graph = tf.Graph() 
        with detection_graph.as_default(): 
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid: 
                serialized_graph = fid.read() 
                od_graph_def.ParseFromString(serialized_graph) 
                tf.import_graph_def(od_graph_def, name='')
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True) 
        category_index = label_map_util.create_category_index(categories)
        print('Finish Load Graph..')

        print(type(category_index))
        print("dict['Name']: ", category_index[1]['name'])

        t_start=time.time()
        fps=0

        with detection_graph.as_default():
            with tf.compat.v1.Session(graph=detection_graph) as sess:
                while True:
                    success, frame = cap.read()
                    image_np_expanded = np.expand_dims(frame, axis=0) 
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0') 
                    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0') 
                    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0') 
                    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0') 
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        #             print('Running detection..') 
                    (boxes, scores, classes, num) = sess.run( 
                        [detection_boxes, detection_scores, detection_classes, num_detections], 
                        feed_dict={image_tensor: image_np_expanded})

        #             print('Done.  Visualizing..')
                    vis_utils.visualize_boxes_and_labels_on_image_array(
                            frame,
                            np.squeeze(boxes),
                            np.squeeze(classes).astype(np.int32),
                            np.squeeze(scores),
                            category_index,
                            use_normalized_coordinates=True,
                            line_thickness=8)

                    for i in range(0, 10):
                        if scores[0][i] >= 0.5:
                            name=category_index[int(classes[0][i])]['name']
                            print(name)



                    fps = fps + 1
                    mfps = fps / (time.time() - t_start)
                    cv2.putText(frame, "FPS " + str(int(mfps)), (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                    ret,jpeg = cv2.imencode('.jpg', frame)
                    img= jpeg.tobytes()


                    sql="INSERT INTO object(NAME) VALUES('"'+%s+'"')" %name 
                    cur.execute(sql)
                    db.commit()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
	