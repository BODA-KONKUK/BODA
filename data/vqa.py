__author__ = 'QingLi'
__version__ = '1.0'

# Interface for accessing the VQA dataset.

# This code is based on the code written by Qing Li for VizWiz Python API available at the following link: 
# (https://github.com/xxx)

# The following functions are defined:
#  VQA        - VQA class that loads VQA annotation file and prepares data structures.
#  getQuesIds - Get question ids that satisfy given filter conditions.
#  getImgIds  - Get image ids that satisfy given filter conditions.
#  loadQA    - Load questions and answers with the specified question ids.
#  showQA    - Display the specified questions and answers.
#  loadRes    - Load result file and create result object.

# Help on each function can be accessed by: "help(COCO.function)"

import json
import datetime
import copy
import random
import skimage.io as io
import matplotlib.pyplot as plt
import os

class VQA:
    def __init__(self, annotation_file=None):
        """
        Constructor of VQA helper class for reading and visualizing questions and answers.
        :param annotation_file (str): location of VQA annotation file
        :return:
        """
        # load dataset
        self.dataset = {}
        self.imgToQA = {}
        if annotation_file != None:
            print('loading dataset into memory...')
            time_t = datetime.datetime.utcnow()
            dataset = json.load(open(annotation_file, 'r'))
            print(datetime.datetime.utcnow() - time_t)
            self.dataset = dataset
            self.imgToQA = {x['image']:x for x in dataset}
        self.anns = {}

    def getImgs(self):
        return list(self.imgToQA.keys())

    def getAnns(self, imgs=[], ansTypes=[]):
        """
        Get annotations that satisfy given filter conditions. default skips that filter
        :param  imgs (str array): get annotations for given image names
              ansTypes  (str array)   : get annotations for given answer types
        :return: annotations  (dict array)   : dict array of annotations
        """
        anns = self.dataset
        
        imgs = imgs if type(imgs) == list else [imgs]
        if len(imgs) != 0:
            anns = [self.imgToQA[img] for img in imgs]
        
        ansTypes  = ansTypes  if type(ansTypes)  == list else [ansTypes]
        if len(ansTypes) != 0:
            anns = [ann for ann in anns if ann['answer_type'] in ansTypes]
       
        self.anns = anns
        return anns
    
    def getBestAnns(self, imgs=[], ansTypes=[]):
        """
        code by SOOH-J 
        Filter the best answer(only one answer with confidence)
        :param  imgs (str array): get annotations for given image names
              ansTypes  (str array)   : get annotations for given answer types
        :return: annotations  (dict array)   : dict array of annotations
        """
        try:
            anns = self.anns
        except:
            anns = self.getAnns(imgs,ansTypes)
            
        # include only answers with confidence
        confidence_anns = []
        for ann in anns:
            confidence_ann = [an for an in ann['answers'] if an.get('answer_confidence') == 'yes']
            if confidence_ann:
                ann_copy = ann.copy() 
                ann_copy['answers'] = confidence_ann
                try:
                    ann_copy['answer'] = max([con_ans['answer'] for con_ans in confidence_ann])
                except:
                    continue
                confidence_anns.append(ann_copy)
                
        return confidence_anns

    def showQA(self, anns):
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """
        if len(anns) == 0:
             return 0
        for ann in anns:
            print("Question: %s"%ann['question'])
            print("Answer: ")
            print('\n'.join([f"\tanswer:{x['answer']}, confidence:{x['answer_confidence']}" for x in ann['answers']]))
            print("SOOOO the best answer:")
            print(f"\t{ann['answer']}")
