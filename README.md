# Supplementary material for: Mapping of dietary sources of nitrates and nitrites. Part 1 of the risk assessment of nitrates and nitrites in food

Containes python scripts and results, version in Zenodo:
[![DOI](https://zenodo.org/badge/320275625.svg)](https://zenodo.org/doi/10.5281/zenodo.14253302)

Flow chart illustrating extraction strategy from the VetDuAt database. Elements are introduced to gain sensitivity (shown in green), and specificity (shown in red). Threshold for similarity is especially important to gain additional sensitivity, however a dictionary with forbidden words and segments is crucial for specificity. 

# Simplified pipeline
![Figure 1](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/blob/main/VetDuAt_Fig_2109.jpg)

# Summary

[extractions_of_items_from_vetduat.py](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/blob/main/extractions_of_items_from_vetduat.py) extracts food items from the VetDuAt database, database is provided as excel file or pickle object.  

[venn_intersections.py](https://github.com/bazyliszek/VKM-001-nitrit-nitrate/blob/main/venn_intersections.py) produces excel files with food items at intersections of venn diagrams as well as raw venn diagrams, input comes from the firs file 


# Abstract
A pragmatic approach was applied to identify nitrate and/or nitrite containing products on the Norwegian market. The VetDuAt database, a comprehensive but not exhaustive database of food items on the Norwegian market, was the single source used to identify these food items. 
The commercial food information database ‘VetDuAt.no’ is a Norwegian database with information about brand level food items and their ingredients. The database contains information such as food item name, nutrient content, and the list of ingredients. It is not a food composition database and does not include information about the amount of nitrates and nitrates in foods. VKM used a snapshot of this database obtained in Excel format from the creators at VetDuAt.no (dated 30.05.2024), including 71497 foods. The purpose of extracting data from the VetDuAt database was to identify and obtain information about food items on the Norwegian market to which nitrate and/or nitrite were added either as additives or as plant extracts. The database was also used to identify foods naturally containing nitrates and nitrites, such as celery and spinach. The database includes foods from manufacturers in Norway as well as imported products. However, food items from some brands (e.g. First Price, Jacobs, Eldorado, Fersk&Ferdig, Fiskemannen, Folkets and Rema 1000) were not part of this database at the time of data extraction. All preprocessing and extraction of data were performed using Python 3.0 (see Abbreviations and glossary for expressions in this section). We utilized packages in the Python library, such as Pickle, Pandas, Re, CSV, to load, read, and reformat file content. To identify the four food additives and other information in the ingredient lists of the food items in the database, the Fuzz package was used to look for similarities between text and indicated keywords, utilizing the fuzzy string-matching technique. A comprehensive, simplified flow chart illustrating the extraction strategy. During the extraction, different elements were introduced to gain both sensitivity and specificity of the search. 

We used fuzzy string-matching with the Levenshtein distance algorithm to identify similar, but not identical elements in the data. This technique was employed to capture similar words, especially when words were misspelled, or punctuation was introduced. The Python code was designed to extract, process, and analyse information from the database, using fuzzy string-matching technique, focusing on certain food additives (e.g., nitrates, nitrites), foods that are known for having high occurrence of naturally occurring nitrates and nitrites, as well as vegetable extracts. 

The text in the ingredients lists was prepared for fuzzy string-matching to extract food items containing nitrites, nitrates, or specific food items as specified below. The column titled ‘ingredients content’ (Norwegian: ‘ingredienser’) was used for extraction. Since this column contains strings of multiple words, certain symbols (i.e.: ‘)’, ’-‘, ’%’, ’_’ ,’]’,  ‘}’) were stripped from the text prior to processing as they are unrelated to the ingredient names they would be found next to. Other symbols (i.e.: ‘,’,  ‘(‘,  ‘.’,  ‘:’,  ‘\’, ‘[‘,  ‘;’, ‘{‘) were treated as separators, dividing two ingredient names as they were the ones most likely to be followed by other characters. To further increase sensitivity (the number of items matched and discovered), we ran the search twice, once in which it divided the ingredients list on only the separators mentioned above, and once where it also divided them on spaces between individual words in addition to the mentioned characters. This approach increases sensitivity of the search.

Word matching and extraction strategy
We created the function ‘matchesAnyIndex’ that returns the index of all elements in the VetduAt database containing an ingredient that fuzzy matched at least one of the provided keywords. During extractions, different fuzzy cutoffs were tested to determine the optimal word similarity threshold, of which 100 is a total match and 0 is no match. Cutoffs of 95 and 80 were applied and compared for sensitivity of the search strategy. Results were further manually curated by inspecting false positives in the search result to further improve accuracy. The ‘no-spaces’ version was able to find complex key phrases such as ‘vegetable extract’ while the spaces version was able to pick up cases where the nitrate/nitrite related key word was part of a larger phrase or had additional words such as ‘preservative’ appended to it. 
The code saved excel files containing only the rows with at least one keyword/name for nitrate/nitrite/extracts/food, as well as additional columns showing the matched keyword and how strongly it was associated with the closest word in the table.
During extraction, certain terms that should not be matched were identified and omitted in the code. This approach automatically excluded any content with a forbidden segment, even if it only partially matched the search terms. Similarly, any item that exactly matched a forbidden word was also excluded. For example, ‘salat’ (English: “salad”) would match ‘salt,’ so ‘salt’ was added as an excluded word to prevent mismatches. However, if ‘salt’ was in the forbidden segments, it would block matches like ‘nitritsalt.’ By placing ‘salt’ in the forbidden words section, it only excluded the exact word ‘salt’ but not ‘nitritsalt’.
Additionally, special handling was implemented for E numbers due to inconsistencies in their recording in the database (e.g., ‘konserveringsmiddel,’ ‘middel,’ ‘konserveringsmiddel-E,’ ‘E-,’ etc.), which could lead to missed matches.
Finally, we refined our search using the created function `compareIndex` to assess the impact of further lowering the fuzzy matching cutoffs (70, 60) which was compared to the high cutoffs (95, 80) to assess additional gain of lowering this cutoff (Figure 2.1.3-1). In this way we could assess whether lowering the cutoff had an additional gain or only contributed to noise in the search.

# Additional explanation can be found in the VKM report.

# Keywords
AI, VKM, nitrite, nitrate, foods, overview, foods

# Requirements
Python 3.0; os; pickle; pandas import read_excel, ExcelWriter; re; csv; thefuzz; 

