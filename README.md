# Mapping of dietary sources of nitrates and nitrites. Part 1 of the risk assessment of nitrates and nitrites in food

Containes python scripts and results, version in Zenodo:
[![DOI](https://zenodo.org/badge/320275625.svg)](https://zenodo.org/doi/10.5281/zenodo.11530986XXX)

Flow chart illustrating extraction strategy from the VetDuAt database. Elements are introduced to gain sensitivity (shown in green), and specificity (shown in red). Threshold for similarity is especially important to gain additional sensitivity, however a dictionary with forbidden words and segments is crucial for specificity. 

# Simplified pipeline
![Figure 1](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/blob/main/VetDuAt_Fig_2109.jpg)

# Additional explanation can be found in the VKM report.


# Summary

[extractions_of_items_from_vetduat.py](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/blob/main/extractions_of_items_from_vetduat.py) extracts food items from the VetDuAt database, provided as pickle file or excel file.  

[venn_intersections.py](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/blob/main/venn_intersections.py) produces excel files with food items at intersections of venn diagrams as well as raw venn diagrams 


# Abstract


# Keywords
AI, VKM, nitrite, nitrate, foods, overview, foods

# Requirements
Python 3.0; os; pickle; pandas import read_excel, ExcelWriter; re; csv; thefuzz; 

