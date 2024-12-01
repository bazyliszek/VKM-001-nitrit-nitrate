# Mapping of dietary sources of nitrates and nitrites. Part 1 of the risk assessment of nitrates and nitrites in food

Containes python scripts for methAI, version in Zenodo:
[![DOI](https://zenodo.org/badge/320275625.svg)](https://zenodo.org/doi/10.5281/zenodo.11530986XXX)

# Flow chart illustrating extraction strategy from the VetDuAt database. Elements are introduced to gain sensitivity (shown in green), and specificity (shown in red). Threshold for similarity is especially important to gain additional sensitivity, however a dictionary with forbidden words and segments is crucial for specificity. 

# Simplified pipeline
![alt text](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/main/VetDuAt_Fig_2109.png)

# Additional explanation can be found in the VKM report.


# Summary

[decisionTreeDimReduction.py](https://github.com/bazyliszek/methAI/blob/main/decisionTreeDimReduction.py) uses XXX

[createPcaSetv4.py](https://github.com/bazyliszek/methAI/blob/main/createPcaSetv4.py) takes as its input a folder containing files downloaded from TCGA. Reads the methylation data from each patient, then performs dimensional reduction to reduce the data to a smaller set, then separates the data into training, validation, and testing sets, then pickles the resulting object. That pickle file can be used by the rest of the program.



# Details
## createPcaSetv4.py
createPcaSetv4 is given a folder containing subfolders containing jhu files. It reads them and removes any that contain too many NAs, then reduces the datapoints to a given number of dimesions using either PCA to compress the locations together or a decision tree to select the locations most likely to be useful for further analysis.




# Abstract

Aberrant 

# Keywords
AI, VKM, nitrite, nitrate, foods, overview, foods

# Requirements
Python 3.0

