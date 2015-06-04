# Tian Zhang, Jingyao Qin
# 2015 May

import math
from xml.dom import  minidom
from xml.etree import ElementTree
import xml.etree.cElementTree as ET
import copy
import os


def entropy(x):
    entropyValue = 0
    for k in set(x):
        partition = float(x.count(k)) / len(x)
        entropyValue = entropyValue - partition * math.log(partition, 2)
    return entropyValue


def gainRatioNumeric(category,attributes):
    categories = []
    for i in range(len(attributes)):
        if not attributes[i] == "?":
            categories.append([float(attributes[i]),category[i]])
    categories = sorted(categories, key = lambda x:x[0])
    attri = [categories[i][0] for i in range(len(categories))]
    cate = [categories[i][1] for i in range(len(categories))]
    if len(set(attri))==1:
        return 0
    else:
        gainValues = []; divPoint = [];
        for i in range(1, len(cate)):
            if not attri[i] == attri[i-1]:
                gainValues.append(entropy(cate[:i]) * float(i) / len(cate) + entropy(cate[i:]) * (1-float(i) / len(cate)))
                divPoint.append(i)
        gain = entropy(cate) - min(gainValues)
        pValue = float(divPoint[gainValues.index(min(gainValues))])/len(cate)
        entryAttribute = -pValue * math.log(pValue,2) - (1 - pValue) * math.log((1 - pValue), 2)
        value = gain / entryAttribute
        return value


def gainRatioNominal(category, attributes):
    attribute = []
    categories = []
    offset = 0
    for a in range(len(attributes)):
        if not attributes[a] == "?":
            attribute.append(attributes[a])
            categories.append(category[a])
    for a in set(attribute):  
        categoryKind = []    
        partition = float(attribute.count(a)) / len(attribute)
        for b in range(len(categories)):
            if attribute[b] == a:
                categoryKind.append(categories[b])
        offset = offset + partition * entropy(categoryKind)
    entropyOfAttributes = entropy(attribute)
    gain = entropy(categories) - offset
    if entropyOfAttributes == 0:
        return 0
    else:
        result = gain / entropyOfAttributes
        return result


def divisionPoint(category, attributes):
    categories = []
    divPoint = []
    gainValues = []
    for a in range(len(attributes)):
        if not attributes[a] == "?":
            categories.append([float(attributes[a]),category[a]])
    categories = sorted(categories, key = lambda x:x[0])
    attrib = [categories[a][0] for a in range(len(categories))]
    categ = [categories[a][1] for a in range(len(categories))]
    for a in range(1, len(categ)):
        if not attrib[a] == attrib[a-1]:
            divPoint.append(a)
            gainValues.append(entropy(categ[:a]) * float(a) / len(categ) + entropy(categ[a:]) * (1 - float(a) / len(categ)))         
    return attrib[divPoint[gainValues.index(min(gainValues))]]
    

def buildTree(trainData,category,parent,attributesName,format):
    if len(set(category)) > 1:
        division = []
        for i in range(len(trainData)):
            # print i
            if set(trainData[i]) == set("?"):
                division.append(0)
            else:
                if (format[i] == "numeric"):
                    division.append(gainRatioNumeric(category,trainData[i]))    
                else:
                    division.append(gainRatioNominal(category,trainData[i]))
        if max(division) == 0:
            numMaximum = 0
            for cat in set(category):
                numCatagory = category.count(cat)
                if numCatagory > numMaximum:
                    numMaximum = numCatagory
                    mostCatagory = cat                
            parent.text = mostCatagory
        else:
            indexSelected = division.index(max(division))
            nameSelected = attributesName[indexSelected]
            if format[indexSelected] == "numeric":
                rightChildTrainData = [[] for i in range(len(trainData))]
                leftChildTrainData = [[] for i in range(len(trainData))]
                divPoint = divisionPoint(category,trainData[indexSelected])
                rightChildCategory = []
                leftChildCategory = []
                for i in range(len(category)):
                    if not trainData[indexSelected][i] == "?":
                        if float(trainData[indexSelected][i]) < float(divPoint):
                            #add trainData
                            for j in range(len(trainData)):
                                leftChildTrainData[j].append(trainData[j][i])
                            #add trainCategory
                            leftChildCategory.append(category[i])
                        else:
                            #add trainData 
                            for j in range(len(trainData)):
                                rightChildTrainData[j].append(trainData[j][i])
                            #add tranCategory
                            rightChildCategory.append(category[i])
                if len(leftChildCategory) > 3 and len(rightChildCategory) > 3:
                    p_l = float(len(leftChildCategory)) / (len(trainData[indexSelected]) - trainData[indexSelected].count("?"))
                    children = ElementTree.SubElement(parent,nameSelected,{'value':str(divPoint),"flag":"right","p":str(round(1-p_l,3))})
                    buildTree(rightChildTrainData, rightChildCategory, children, attributesName,format)
                    children = ElementTree.SubElement(parent,nameSelected,{'value':str(divPoint),"flag":"left","p":str(round(p_l,3))})
                    buildTree(leftChildTrainData, leftChildCategory, children, attributesName,format)
                else:
                    numMaximum = 0
                    for cat in set(category):
                        numCatagory = category.count(cat)
                        if numCatagory > numMaximum:
                            numMaximum = numCatagory
                            mostCatagory = cat                
                    parent.text = mostCatagory

            #not numeric
            else:
                for k in set(trainData[indexSelected]):
                    if not k == "?":
                        childTrainData = [[] for i in range(len(trainData))]
                        childCategory = []
                        for i in range(len(category)):
                            if trainData[indexSelected][i] == k:
                                childCategory.append(category[i])
                                for j in range(len(trainData)):
                                    childTrainData[j].append(trainData[j][i])
                        children = ElementTree.SubElement(parent,nameSelected,{'value':k,"flag":"nominal",'p':str(round(float(len(childCategory))/(len(trainData[indexSelected])-trainData[indexSelected].count("?")),3))}) 
                        buildTree(childTrainData,childCategory,children,attributesName,format)   
    else:
        parent.text = category[0]
        

def subTree(element, level = 0):
    value = "\n" + level * "    "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = value + "  "
        for z in element:
            subTree(z, level + 1)
        if not z.tail or not z.tail.strip():
            z.tail = value
    if level and (not element.tail or not element.tail.strip()):
        element.tail = value
    return element


def train(trainObjects,trainResult,xmlTree, format):
    #Record the name of attributes
    print "Training..."
    categories = []
    attributesName = trainObjects[0]
    # delete the whitespaces in attributes names
    for i in range(len(attributesName)):
        attributesName[i] = attributesName[i].strip()
    #store data sort by attributes
    trainData = [[] for i in range(len(attributesName))]
    
    for a in range(1,len(trainObjects)):
        categories.append(trainResult[a][0])
        for b in range(len(attributesName)):
            trainData[b].append(trainObjects[a][b])

    root = ElementTree.Element('unprunedTree')
    decisionTree = ElementTree.ElementTree(root)
    buildTree(trainData,categories,root,attributesName,format)
    decisionTree.write(xmlTree)

    return True


def predict(xmlTree, testObjects):
    attributesName = testObjects[0]
    for i in range(len(attributesName)):
        attributesName[i] = attributesName[i].strip()
    testAnswer = []
    doc = minidom.parse(xmlTree)
    root = doc.childNodes[0]
    for i in range(1, len(testObjects)):
        testAnswerlist = decision(root,testObjects[i],attributesName,1)
        answer = testAnswerlist
        testAnswer.append(answer)
    return testAnswer


def decision(root, objects, attributesName, p):
    if root.hasChildNodes():
        attributeNames = root.firstChild.nodeName
        if attributeNames == "#text":
            return decision(root.firstChild, objects, attributesName, p)  
        else:
            attribute = objects[attributesName.index(attributeNames)]
            if attribute == "?":
                subRoot = {}
                p_max = 0
                for child in root.childNodes:                    
                    if p_max < child.getAttribute("p"):
                        p_max = child.getAttribute("p")
                        child_max = child
                    subRoot = decision(child_max, objects, attributesName, p)
                return subRoot
            else:
                for child in root.childNodes:
                    if child.getAttribute("flag") == "right" and float(attribute) >= float(child.getAttribute("value")) or child.getAttribute("flag") == "nominal" and child.getAttribute("value")==attribute or child.getAttribute("flag") == "left" and float(attribute) <= float(child.getAttribute("value")):
                        return decision(child, objects, attributesName, p) 
    else:
        return root.nodeValue


def prune(xmlTree_input, testObjects, result):
    print "Pruning..."
    doc = ET.parse(xmlTree_input)
    root = doc.getroot()
    for children in root.iter():
        children.set('prune_check', '0')
    prunedtree = pruning(doc, testObjects, result)
    prunedtree.write('prunedTree.xml')
    os.remove('./temp.xml')


def pruning(tree, testObjects, result):
    root = tree.getroot()
    node_stack = []
    for children in root.iter():
        if not (children.text == "1" or children.text == "0" or children.text == "?" ):
            node_stack.append(children)
    for node in range(len(node_stack)):
        cut_parent = node_stack.pop()
        for cut in cut_parent: 
            if not (cut.text == "1" or cut.text == "0" or cut.text == "?" or cut.get("prune_check") == "1"):
                p_max = 0
                cut.set('prune_check', '1')
                oldtree = copy.deepcopy(tree)
                oldtree.write('temp.xml')
                before = validate('temp.xml', testObjects, result)
                for children in cut:
                    if p_max < children.get("p"):
                        p_max = children.get("p")
                        max_text = children.text
                cut.text = max_text
                tree.write('temp.xml')
                after = validate('temp.xml', testObjects, result)
                if after >= before:
                    return pruning(tree, testObjects, result)
                else:
                    return pruning(oldtree, testObjects, result)
    return tree


def validate(xmlTree, testObjects, result):
    testAnswer = predict(xmlTree, testObjects)
    wrongResult = 0
    for a in range(len(testAnswer)):
        if not testAnswer[a] == result[a]:
            wrongResult += 1
    accuracy = 1-float(wrongResult) / len(testAnswer)
    return accuracy


def countSplits(xmlTree):
    doc = ET.parse(xmlTree)
    root = doc.getroot()
    count = 0
    for children in root.iter():
        if not (children.text == "1" or children.text == "0" or children.text == "?" ):
            count += 1
    return count


def outPut_unpruned():
    count = 0;
    fomula = []
    tree = ET.ElementTree(file='unprunedTree.xml')
    for elem in tree.iter():
        count = count + 1
        if str(elem.text) == "None":
            stri = str(elem.tag) + "=" + str(elem.get('value'))
            fomula.append(stri)
            if str(elem.tag) == "unpruenedTree":
                fomula.pop()
        elif str(elem.text) == "0":
            stri = str(elem.tag) + "=" + str(elem.get('value'))
            fomula.append(stri)
            for i in range(0, count-2):
                fomula.pop()
            count = 0;
        else:
            stri = str(elem.tag) + "=" + str(elem.get('value'))
            fomula.append(stri)
            f=open('formula_unpruned.txt','a')
            k=' AND '.join(fomula)
            f.writelines(k+ " OR ")
            f.close()
            for i in range(0, count - 2):
                fomula.pop()
            count = 0;


def outPut_pruned():
    count = 0;
    fomula = []
    tree = ET.ElementTree(file='prunedTree.xml')
    for elem in tree.iter():
        count = count + 1
        if str(elem.text) == "None":
            stri = str(elem.tag) + "=" + str(elem.get('value'))
            fomula.append(stri)
            if str(elem.tag) == "prunedTree":
                fomula.pop()
        elif str(elem.text) == "0":
            stri = str(elem.tag) + "=" + str(elem.get('value'))
            fomula.append(stri)
            for i in range(0, count-2):
                fomula.pop()
            count = 0;
        else:
            stri = str(elem.tag) + "=" + str(elem.get('value'))
            fomula.append(stri)
            f=open('formula_pruned.txt','a')
            k=' AND '.join(fomula)
            f.writelines(k+ " OR ")
            f.close()
            for i in range(0, count - 2):
                fomula.pop()
            count = 0;


def error():
    print "Please type command line in one of the formats below: "
    print "Format_1: python filename.csv(execute) train unpru filename.csv(train) ratio filename.csv(metadata)"
    print "Format_2: python filename.csv(execute) train pru filename.csv(train) ratio filename.csv(metadata) filename.csv(validate)"
    print "Format_3: python filename.csv(execute) validate filename.xml(tree) filename.csv(validate)"
    print "Format_4: python filename.csv(execute) predict filename.xml(tree) filename.csv(test)"
    print "Example: python decisionTree.py train pru btrain.csv 0.1 metadata.csv bvalidate.csv"
