import essentia
import essentia.standard
import essentia.streaming
from essentia.standard import *

import numpy as np
import sys
import time
import os

from pandas import DataFrame
import pandas as pd

# OMG THIS MIGHT BE ONE OF THE MOST BEAUTIFUL PIECES OF CODE I'VE WRITTEN IN A LONG TIME

supported_formats = ['.mp3','.wav','.ogg','.flac','wma','.m4a'] # need to check if all of these are actually supported. So far, mp3 and wav have been tested.

#This function iterates through the directory specified in 'root' and returns an array with the paths of all files in there. Just trust me on this.
def addAllTheFiles(root):
    files = [ os.path.join(root,f) for f in os.listdir(root) if os.path.isfile(os.path.join(root,f))]
    dirs = [ d for d in os.listdir(root) if os.path.isdir(os.path.join(root,d))]
    for d in dirs:
        print ("---" + d+ " -- " +os.path.join(root,d))
        files_in_d = addAllTheFiles(os.path.join(root,d))
        for f in files_in_d:
            if os.path.exists(f):
                filename, file_extension = os.path.splitext(f.split('/')[-1])
                if file_extension in supported_formats:
                    files.append(f)
    return files

# This returns those 4 statistical values of any data array
def getstuffs(data,hopsize=1024): #'data' must be an np.array
    data = np.array(data)
    stds = []# to hold all the frame stds

    #break up frames
    for i in range(0,len(data),hopsize):
        thisdata = list(data)[i:i+hopsize]
        thisdata = np.array(thisdata)
        stds.append(float(thisdata.std()))

    #yay all the values
    stds = np.array(stds)
    mean_std = stds.mean()
    std_std = stds.std()

    mean = data.mean()
    std = data.std()

    return [mean, std, mean_std, std_std] # <- yeah, these ones

# Main extraction engine
def extractTheIsh(filename):
    print "Extracting "+filename
    sampleRate = 44100
    # load 30 seconds after first 30 seconds
    start_time = time.time()
    
    try:
        loader = EasyLoader(filename=filename,startTime=30,endTime=60,sampleRate=sampleRate)
        audio = loader()
    except Exception as oops:
        #print "Looks like we couldn't load this: "+filename
        #print "So we skip it. :P"
        return []
    try:
        yay = LowLevelSpectralExtractor() # this'll get us the timbre features
        rhythmyay = RhythmDescriptors() # this gets us all the rhythm features
        
        stuff = yay(audio) #gets you a TON of stuffs. Returns a humungous tuple that's too big to unpack.
        rstuff = rhythmyay(audio) #this too
    except Exception as oops:
        print "Something went wrong. Skipping."
        print oops
        return []
    #pull out the stuff we need
    mfccs = stuff[5]
    mfccs = mfccs.transpose()
    flux = stuff[21]
    rolloff = stuff[23]
    
    highBPM = rstuff[5]
    highAMP = rstuff[7]
    lowBPM = rstuff[8]
    lowAMP = rstuff[10]
    histogram = rstuff[11] # the bpm histogram. Hallelujah.
    BHSUM1 = sum(histogram[40:90]) # we sum the bins of certain bpm ranges. Because we can.
    BHSUM2 = sum(histogram[90:140])
    BHSUM3 = sum(histogram[140:250])
    try:
        H_L_Ratio = 1.0*highBPM/lowBPM
    except Exception as oops:
        H_L_Ratio = 0.0
    
    #spectral centroid requires jumping through some hoops
    f = FrameCutter()
    centroid = []
    while True:
        frame = f(audio)
        if not len(frame):
            break
        s = Spectrum()
        spec = s(frame)
        s_c = SpectralCentroidTime()
        centroid_single = s_c(spec)
        centroid.append(centroid_single)
    
    #yay now we compile the features into a feature array
    features = []
    features.append(highBPM)
    features.append(highAMP)
    features.append(lowBPM)
    features.append(lowAMP)
    features.append(H_L_Ratio)
    features.append(BHSUM1)
    features.append(BHSUM2)
    features.append(BHSUM3)
    for mfcc in mfccs:
        features.extend(getstuffs(mfcc))
    features.extend(getstuffs(centroid))
    features.extend(getstuffs(flux))
    features.extend(getstuffs(rolloff))
    
    features = np.array(features)
    #print(" Time taken --- %s seconds ---" % (time.time() - start_time))
    return tuple(features)

# builds a CSV containing all extracted features
def buildtheCSV(features,filename):

    headers = ['highBPM','highAMP','lowBPM','lowAMP','HighLowRatio','BHSUM1','BHSUM2','BHSUM3']

    featname = ['MFCC0','MFCC1','MFCC2','MFCC3','MFCC4','MFCC5','MFCC6','MFCC7','MFCC8','MFCC9','MFCC10','MFCC11','MFCC12','Spec_Centroid','Spec_Flux','Spec_Rolloff']
    statname = ['mean', 'std', 'mean_std', 'std_std']

    for feat in featname:
        for stat in statname:
            headers.append(feat+"_"+stat)

    header = ""
    for thing in headers:
	    header += (thing + ",")

    print "No. of columns:",len(headers)
    features = np.array(features)
    np.savetxt(filename, features, delimiter=",", fmt='%s',header=header)
    print "Wrote file: "+filename

def extractFeaturesOfThese(root,files, whichfeatures):
    allfeatures = []
    for track in files:
        stuff = extractTheIsh(os.path.join(root,track))
        if not stuff == []:
            allfeatures.append(stuff)
            
    #this is to get all the column headers
    headers = ['bh_highpeakbpm','bh_highpeakamp','bh_lowpeakbpm','bh_lowpeakamp','bh_highlowratio','bhsum1','bhsum2','bhsum3']

    featname = ['mfcc0','mfcc1','mfcc2','mfcc3','mfcc4','mfcc5','mfcc6','mfcc7','mfcc8','mfcc9','mfcc10','mfcc11','mfcc12','centroid','flux','rolloff']
    statname = ['mean', 'std', 'mean_std', 'std_std']

    for feat in featname:
        for stat in statname:
            headers.append(stat+"_"+feat)
    
    # create a pandas dataframe to make life easy. I hope.
    df = pd.DataFrame(data = allfeatures, columns=headers)
    
    #TheFeatures = df.filter(whichfeatures, axis=1)
    
    return df.as_matrix(whichfeatures)

