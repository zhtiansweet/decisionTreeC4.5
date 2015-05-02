# Decision Tree
_May 2015_  
_By Tian Zhang and Jingyao Qin_  
_Course: Machine Learning, Northwestern University, Evanston, IL_  

We implemented decision tree model based on C4.5 algorithm in this project. The decisionTree.py is the excution file which contains the main function, and the c45.py contains C4.5 and pruning algorithms.
##How to run the code
To run the program, please type command line in one of the formats below:  
Format_1: python filename.csv(execute) train unpru filename.csv(train) ratio filename.csv(metadata)  
Format_2: python filename.csv(execute) train pru filename.csv(train) ratio filename.csv(metadata) filename.csv(validate)  
Format_3: python filename.csv(execute) validate filename.xml(tree) filename.csv(validate)  
Format_4: python filename.csv(execute) predict filename.xml(tree) filename.csv(test)  
(Example: python decisionTree.py train pru btrain.csv 0.1 metadata.csv bvalidate.csv)  

Ratio means the percentage of data used to train the model of the whole training dataset. It should be in (0, 1].  
Please make sure that all files are in the same folder and the metadata.csv is in the example formate.

Format_1 will generate an unpruned tree in both unprunedTree.xml and formula_pruned.txt. And you could clearly view the tree by putting the xml file on http://codebeautify.org/xmlviewer. This process takes some time, please be patient.   
Format_2 will generate a pruned tree in both prunedTree.xml and formula_unpruned.txt. This process takes some time, please be patient.  
Format_3 will compute the accuracy of the input tree.  
Format_4 will make prediction on the test data and generate predict.csv.  
##C4.5 algorithm
For each node, we chose the attribute with the highest information gain ratio. The gain ratio was computed with gain and entropy as below.  
Nominal attribute:  
![equation](https://github.com/zhtiansweet/decisionTreeC4.5/blob/master/pictures/QQ20150502-1%402x.png)  
Numeric attribute:  
![equation](https://github.com/zhtiansweet/decisionTreeC4.5/blob/master/pictures/QQ20150502-2%402x.png)
##Missing Data
In the training process, we simply abandoned the missing ones and only use the existing values. As for the testing process, we decided the categories as the ones with highest possibility. Below is an example.  
![graph](https://github.com/zhtiansweet/decisionTreeC4.5/blob/master/pictures/QQ20150502-1%402x%20copy.png)  
Say an instance’s temperature value is missing. Since P(winner = 0) = 0.46875 and P(winner = 1) = 0.53125, we will decide the winner of this instance as 1.  
##Pruning Algorithm
We implemented Reduced Error Pruning. We traversed the whole tree with DFS. For each node, we replaced it with its most popular class, and the computed the prediction accuracy again. If the accuracy was not reduced, we would keep the change; otherwise, we would undo the change.  

Below is a learning curve of our decision tree model. Generally, both accuracies of unpruned and pruned trees increase with data ratio increasing. And for the same data ratio, the accuracy of pruned tree is always higher than that of unpruned tree.
![curve](https://github.com/zhtiansweet/decisionTreeC4.5/blob/master/pictures/Untitled.png)
