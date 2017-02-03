###This code is in part adapted from https://github.com/cmusatyalab/openface/blob/master/demos/compare.py
###To make the  

import openface
import os
import time
import cv2
import pickle

def load_model_and_Dlib(pathtoalign,pathtomodel):
    
    s = time.time()
    align=openface.AlignDlib(pathtoalign)
    model=openface.TorchNeuralNet(pathtomodel,96)
    e = time.time()-s
    print "Loading models took {} seconds".format(e)
    
    return align,model
    
    
def getEmbedd(imgpath,align,model):
    
    bgrimg = cv2.imread(imgpath)
    rgbimg=cv2.cvtColor(bgrimg,cv2.COLOR_BGR2RGB)
    embedd=[]
    imgbb = align.getLargestFaceBoundingBox(rgbimg,skipMulti=True)
    alignimg = align.align(96,rgbimg,imgbb,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    
    if alignimg is not None:
        embedd =  model.forward(alignimg)
    else:
        print(imgpath)  

    return embedd
    

if __name__ == '__main__':
    
    pathtoalign = "models/dlib/shape_predictor_68_face_landmarks.dat"
    pathtomodel = "models/openface/nn4.small2.v1.t7"
    
    align, model = load_model_and_Dlib(pathtoalign,pathtomodel)
    
    embeddings=[]
    imgpaths=[]
 
    
    for folder_name in os.listdir("lfw_faces/"):
        if folder_name != ".DS_Store":
            for file_name in os.listdir("lfw_faces/"+folder_name):
                if file_name != ".DS_Store":
                    imgpaths.append("lfw_faces/"+folder_name+"/"+file_name)
    imgpaths_sorted = sorted(imgpaths,key=str.lower)
    
    s = time.time()
    print("Beginning")
    for imgpath in imgpaths_sorted:
        embeddings.append(getEmbedd(imgpath,align,model))
       
    print("Ending. Time {}".format(time.time()-s))
    pickle.dump(embeddings, open("embeddings","wb")) 
