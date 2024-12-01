# Extracting informations from VetDuAt database for nitrites, nitrates, foods and extracts 

# Importing libraries
import os
import pickle
from pandas import read_excel, ExcelWriter
import re
import csv
from thefuzz import fuzz

# Annotating found items to KBS ontology (here not used)
#fuzzyMatchCodes = True # Include 3 columns describing the closest match in the "KBS.FoodEx2.Nitritt.txt" file
fuzzyMatchCodes = False # Don't include those columns

forceReload = False # overide the pickel object if needed
folder = "C:/Users/maww/Documents/Python_Scripts/VKM-P001"
#dataFileAddress = folder + "/VETDUAT\ Uttrekk\ Eks\ Nonfood\ 2024.xlsx"
dataFileAddress = folder + "/VETDUAT Uttrekk Eks Nonfood 2024.xlsx"
pickleFileAddress = folder + "/pickledNor.pkl"

fileSuffix = "_combined_2109"

# Finding the correct pathways for raw files from VetDuAt

if os.path.exists(pickleFileAddress) and forceReload == False:
    with open(pickleFileAddress, "rb") as pickleFile:
        dataFrame = pickle.load(pickleFile)
else:
    with open(dataFileAddress, "rb") as dataFile:
        dataFrame = read_excel(dataFile)
        
    with open(pickleFileAddress, "wb") as pickleFile:
        pickle.dump(dataFrame, pickleFile)

print(f"there are {dataFrame.shape} objects in this database")


print (dataFrame.columns)


#fuzzy_cuttoff controls how generous the fuzzy string matching is.
#lower_cutoff can be used to test how much more will be included by making the fuzzy_cuttoff more generous (lower), 
# # and omitting allready good stuff (>80 = fazzy_cutoff)
#these numbers are a percentage describing how close two strings need to be for the fuzzy matching to consider them to be the same.

#fuzzy_cuttoff = 95
fuzzy_cuttoff = 80
#lower_cuttoff = 70 #this has found natriumsitrat and other natrium or kalium (with other salt)`
lower_cuttoff = 60 #still finding natrium sitrat ...
#lower_cuttoff = 90 # natrium sitrat is gone now ... natrium [n]itrat

#Preparations for E numbers - creates three regular expressions, one to find phrases starting with an E, followed by a space then numbers,
#another to find phrases starting with an E and going straight to numbers, and finally one to find phrases starting with an E and any amount of
#spaces before going to numbers
enum_with_space = r'E\s\d+'
enum_without_space = r'E\d+'
enum_any_spaces = r'e\s*\d+'

#English key words (not used, as we had norwegian database)
Nitrates_EN = ["Ammonium nitrate bicarbonate", "Chile saltpeter", "Chilean nitrate", "E 251", "E 252", "Niter", "Nitrate", "Nitrate of potash", "Potassium nitrate", "Saltpeter", "Soda niter", "Sodium nitrate"]
Nitrites_EN = ["E 249", "E 250", "Nitrite", "Nitrous acid, potassium salt", "Nitrous acid, sodium salt", "Potassium nitrite", "Sodium nitrite"]
Extracts_EN = ["Vegetable extract", "Plant extract", "Botanical extract", "Herbal extract", "Veggie extract", "Vegetable broth", "Phyto extract", "Plant essence", 
                 "Vegetable essence", "Plant concentrate", "Vegetable concentrate", "Vegetable tincture", "Plant-derived extract"]
Foods_EN = ["Spinach", "Celery", "Rucola", "Lettuce", "Cabbage"] 


#Norwegian key  word that went for matching according to the protocol 
Nitrates_NO_exact = ["Ammoniumnitrat bikarbonat","Ammoniumnitratbikarbonat", "E 251", "E 252"]
Nitrates_NO_fuzzy = ["Kaliumnitrat", "Niter", "Nitrat", "Nitrat av kaliumklorid", "Salpeter", "Natriumnitrat"]
Nitrates_NO_all = []
Nitrates_NO_all.extend(Nitrates_NO_exact)
Nitrates_NO_all.extend(Nitrates_NO_fuzzy)
Nitrites_NO_exact = ["E 249", "E 250"]
Nitrites_NO_fuzzy = ["Nitritt", "Kaliumnitritt", "Natriumnitritt", "nitritsalt", "nitritsalt"]
Nitrites_NO_all = []
Nitrites_NO_all.extend(Nitrites_NO_exact)
Nitrites_NO_all.extend(Nitrites_NO_fuzzy)
Extracts_NO_exact = []
Extracts_NO_fuzzy = ["Grønnsaksekstrakt",  "Planteekstrakt" , "Urteekstrakt",  "Grønnsaksbuljong", "Fytoekstrakt",
               "Planteessens", "Grønnsaksessens", "Plantekonsentrat", "Grønnsakskonsentrat", "Grønnsakstinktur"]
Foods_NO_exact = [] 
Foods_NO_fuzzy = ["Spinat", "Selleri", "Rucola", "Salat", "Kål", "Rødbete", "hvitkål", 
                  "rødtkål", "hodekål", "stangselleri", "sellerirot", "grønnkål", "tare"] 

#automatically reject anything that includes something listed in forbidden segments even if it is only a small part of that thing.
#Also exclude anything written in forbidden words as long as that makes up the full thing. 

#Salat matches salt, so salt has been added as an excluded word that is never found. If salt was in the forbidden segments though, 
# it would prevent nitritsalt from being found. By putting salt in the forbidden words section instead 
# it only excludes the exact word salt.

forbiddenSegments = ["sitr", "sellerifrø", "kålrabi", "kålrot", "løk", "vin", "benzoat", "citrat", "selenit", "løl", "tøk", "læk", "løg", "lök", "kaliumiaktat", 
                     "natriumlaktrat", "salter"]

forbiddenWords = ["salt", "salter", "ammoniumbikarbonat", "KALIUMBITARTRAT", 
                  "natriumsistrat", "natriumsitater", "natriumtartrat", 
                  "eller", "HVITLO", "hvitlø", 
                  "ananaskonsentrat", "beteeekstrakt", "eple konsentrat", "epleekstrakt", "eplekonsentrat", "eple konsentrat", 
                  "eplekonsetrat", "Epplekonsentrat", "erteekstrakt 1", "gjæreekstrakt", "grønnte sekstrakt", "grønnteekstrakt",  
                  "/gærekstrakt", "/epleekstrakt", "jærekstrakt", "KANELEKSTRAKT", "kanelekstrakt*", "kanelekstrakt", "lønneekstrakt", 
                  "mynteekstrakt", "smaksekstrakt", "østerekstrakt",
                  "pæreekstrakt", "pærekonsentrat", "rekeekstrakt", "roseekstrakt", "teekstrakt", "teekstrakt*", "teekstrakter", "tekonsentrat^", 
                  "gærekstrakt", "gærsekstrakt", 
                  "rødbeterød", "/Gulrotsekstrakt", "beteekstrakt", "erteekstrakt", "grønn teekstrakt", "grønn teekstrakt*", 
                  "gulrotekstrakt", "plommekonsentrat", "proteinekstrakt", 
                  "tre", "Spianata"] #"tareekstrakt" was removed  #"ammoniumnitrat bikarbonat"

# Preparation for removing these characters from the whole text before doing any matching. 
# Commas aren't listed here as it uses them to split the sections but they also get removed.
punctuation = [")","-","%","_","]", "}"]

# Following block of code handles different eNumber formats
def fixEnums(keyList):
    #"E(Any number)" causes it to add "E (that number)"
    #"E (Any number)" causes it to add "E(that number)"
    to_add = []
    for current in keyList:
        if re.match(enum_with_space, current):
            to_add.append("konserveringsmiddel E " + current[2:])
            to_add.append("konserveringsmiddel E" + current[2:])
            to_add.append("konserveringsmiddel E-" + current[2:])
            to_add.append("middel E " + current[2:])
            to_add.append("middel E" + current[2:])
            to_add.append("middel E-" + current[2:])
            to_add.append("E" + current[2:])
            to_add.append("E-" + current[2:])
        elif re.match(enum_without_space, current):
            to_add.append("konserveringsmiddel E " + current[1:])
            to_add.append("konserveringsmiddel E" + current[1:])
            to_add.append("konserveringsmiddel E-" + current[1:])
            to_add.append("middel E " + current[1:])
            to_add.append("middel E" + current[1:])
            to_add.append("middel E-" + current[1:])
            to_add.append("E " + current[1:])
            to_add.append("E-" + current[1:])
    keyList.extend(to_add)

# Not used
#fixEnums(Nitrates_EN)
#fixEnums(Nitrites_EN)
#fixEnums(Extracts_EN)
#fixEnums(Foods_EN)

# Used 
fixEnums(Nitrates_NO_exact)
fixEnums(Nitrites_NO_exact)
fixEnums(Extracts_NO_exact)
fixEnums(Foods_NO_exact)


# The code splits the ingredients string on following puntuations: , ( . : backslash [ and {
punctSplit = r',|\(|\.|:|\\|\[|;|{'
punctAndSpaceSplit = r'\s|,|\(|\.|:|\\|\[|;|{'

# Returns the index of all elements in a dataframe (df) that have an ingredient the fuzzy-matches one of the keywords provided.
def matchesAnyIndex(df, keywords_exact, keywords_fuzzy, negative_keywords = [], ingredients_name = "Ingredienser"):
    matchingIndex = []
    first_keywords = []
    foundWithSpace = []
    for i in range(0, len(df[ingredients_name])):
        for splitOnSpace in [False, True]:
            if splitOnSpace == True:
                if i in matchingIndex:
                    continue
            rawString = str(df[ingredients_name][i])
            for symbol in punctuation:
                rawString = rawString.replace(symbol, " ")

            if splitOnSpace:
                splitString = re.split(punctAndSpaceSplit, rawString)
            else:
                splitString = re.split(punctSplit, rawString)
            found = False
            for current in splitString:
                if found:
                    break

                foundProblem = False
                for problem in forbiddenSegments:
                    if problem.strip().lower() in current.strip().lower():
                        foundProblem = True
                        break
                for problem in forbiddenWords:
                    if problem.strip().lower() == current.strip().lower():
                        foundProblem = True
                        break
                if foundProblem:
                    continue
                for compare in keywords_exact:
                    if current.strip().lower() == compare.strip().lower():
                        matchingIndex.append(i)
                        first_keywords.append(current.strip())
                        foundWithSpace.append(splitOnSpace)
                        found = True
                        break
                if not found:
                    for compare in keywords_fuzzy:
                        #anything that isn't an E number uses fuzzy matching
                        matchStrength = fuzz.token_sort_ratio(current.strip().lower(), compare.strip().lower() )
                        if matchStrength > fuzzy_cuttoff: #this was 
                            #if fuzz.partial_token_sort_ratio(current.strip().lower(), compare.strip().lower() ) > fuzzy_cuttoff: #this was a problem allows matching any part of the string
                            matchesNegative = False
                            for compare2 in negative_keywords:
                                if fuzz.token_sort_ratio(current.strip().lower(), compare2.strip().lower() ) > matchStrength:
                                    matchesNegative = True
                                    break
                            if not matchesNegative:
                                matchingIndex.append(i)
                                first_keywords.append(current.strip())
                                foundWithSpace.append(splitOnSpace)
                                #print(str(len(matchingIndex)) + ":" + str(len(first_keywords)) + ":" + str(matchingIndex[-1]) + ":" + first_keywords[-1])
                                found = True
                                break
                    
    return matchingIndex, first_keywords, foundWithSpace

# Does the same as above, but instead of reporting the closest matches, it instead excludes those and reports the matches that would be found if fuzzy_cutoff was reduced
#to Lower cuttoff instead. EG only reporting those entries that match a keyword at >80% but less than 90%.
#This is useful for testing whether reducing the cuttoff value would be useful or if it would introduce too many false positives.
# It is not used at the end when cutoff are made

def comparesIndex(df, keywords_exact, keywords_fuzzy, negative_keywords = [], ingredients_name = "Ingredienser"):
    matchingIndex = []
    for i in range(0, len(df[ingredients_name])):
        #if i == 68565:
        #    print("")
        #print(f"{i}")
        rawString = str(df[ingredients_name][i])
        for symbol in punctuation:
            rawString = rawString.replace(symbol, " ")
        splitString = re.split(punctAndSpaceSplit, rawString)
        found = False
        for current in splitString:
            if found:
                break
            
            foundProblem = False
            for problem in forbiddenSegments:
                if problem.strip().lower() in current.strip().lower():
                    foundProblem = True
                    break
            for problem in forbiddenWords:
                if problem.strip().lower() == current.strip().lower():
                    foundProblem = True
                    break

            for compare in keywords_exact:
                if re.match(enum_any_spaces, compare.strip().lower()):
                    #Enumbers don't get fuzzy matching
                    if current.strip().lower() == compare.strip().lower():
                        matchingIndex.append(i)
                        found = True
                        break
            if not found:
                for compare in keywords_fuzzy:
                    #anything that isn't an E number uses fuzzy matching
                    matchStrength = fuzz.token_sort_ratio(current.strip().lower(), compare.strip().lower() )
                    if matchStrength <= fuzzy_cuttoff:
                        if matchStrength > lower_cuttoff:
                            if foundProblem:
                                if (current.strip().lower() != "salt") and  (current.strip().lower() != "hvitløk"):
                                    print(f"Skipping {current}")
                            else:
                                for compare2 in negative_keywords:
                                    if fuzz.token_sort_ratio(current.strip().lower(), compare2.strip().lower() ) > matchStrength:
                                        matchesNegative = True
                                        break
                                if not matchesNegative:
                                    matchingIndex.append(i)
                                    found = True
                                    break
                    
    return matchingIndex


#if the ''' is commented out with a hash then the program will use the lower_cutoff parameter and create a file that will 
# show which items would be included by dropping the value of cutoff to the value of lower cutoff. 
# It will not include any values above cutoff or below lower cutoff, only those in between. 
# This is because it is not trying to find the best matches, but to show which
# uncertain matches would be included by lowering the cutoff value. If the resulting file has a lot of bad entries in it then it indicates 
# that the value should not be lowered.
#if the line below is left as ''' then the cutoff variable will be used instead and lowe_cutoff will be complete ignored.
'''
#uses lower_cutoff
nitrates_index = comparesIndex(dataFrame, Nitrates_NO, negative_keywords=Nitrites_NO)
print(f"nitrAtes done! Found {len(nitrates_index)}")
subset = dataFrame.iloc[nitrates_index]
with ExcelWriter(folder + f"/CompareFuzzy{fuzzy_cuttoff} - {lower_cuttoff}_Nitrates_NO.xlsx") as writer:
    subset.to_excel(writer)

nitrites_index = comparesIndex(dataFrame, Nitrites_NO, negative_keywords=Nitrates_NO)
print(f"nitrItes done! Found {len(nitrites_index)}")
subset = dataFrame.iloc[nitrites_index]
with ExcelWriter(folder + f"/CompareFuzzy{fuzzy_cuttoff} - {lower_cuttoff}_Nitrites_NO.xlsx") as writer:
    subset.to_excel(writer)

extracts_index = comparesIndex(dataFrame, Extracts_NO)
print(f"extracts done! Found {len(extracts_index)}")
subset = dataFrame.iloc[extracts_index]
with ExcelWriter(folder + f"/CompareFuzzy{fuzzy_cuttoff} - {lower_cuttoff}_Extracts_NO.xlsx") as writer:
    subset.to_excel(writer)

foods_index = comparesIndex(dataFrame, Foods_NO)
print(f"foods done! Found {len(foods_index)}")
subset = dataFrame.iloc[foods_index]
with ExcelWriter(folder + f"/CompareFuzzy{fuzzy_cuttoff} - {lower_cuttoff}_Foods_NO.xlsx") as writer:
    subset.to_excel(writer)

'''
# Mapping the items identified with KBS ontology (not used here as it performed badly and manual annotation was done instead)
codesMap = {}
namesToCodesFile = folder + "/KBS.FoodEx2.Nitritt.txt"
if fuzzyMatchCodes:
    with open(namesToCodesFile, 'r', encoding="utf-8") as currentFile:
        #rows = currentFile.split("\n")
        for row in currentFile:
            data = row.split("\t")
            codesMap[data[2]] = data[4]

#only uses fuzzy_cutoff
# This is the main part of the code for finding Nitrates 
nitrates_index, first_keywords, foundWithSpace = matchesAnyIndex(dataFrame, Nitrates_NO_exact, Nitrates_NO_fuzzy, negative_keywords=Nitrites_NO_all)
subset = dataFrame.iloc[nitrates_index]
subset.insert(7, "Found only with space", foundWithSpace, True)
subset.insert(7, "KeyWord", first_keywords, True)

#with a possibility of matching with KBS, that was not performed here (this part was not working well)
if fuzzyMatchCodes:
    foodCodes = []
    foodCodeScores = []
    matchStrings = []
    for cell in subset["Markedsnavn"]:
        bestMatch = "NA"
        matchedTo = "NA"
        matchScore = 0
        for key in codesMap.keys():
            score = fuzz.token_sort_ratio(cell.strip().lower(), key.strip().lower() )
            #score = fuzz.partial_token_set_ratio(cell.strip().lower(), key.strip().lower() )
            if score > matchScore:
                matchScore = score
                bestMatch = codesMap[key]
                matchedTo = key
        foodCodes.append(bestMatch)
        foodCodeScores.append(matchScore)
        matchStrings.append(matchedTo)
    subset.insert(1, "FoodCode", foodCodes, True)
    subset.insert(1, "FuzzyScore", foodCodeScores, True)
    subset.insert(1, "MatchedTo", matchStrings, True)

with ExcelWriter(folder + f"/Nitrates_NO{fileSuffix}.xlsx") as writer:
    subset.to_excel(writer)
print(f"nitrAtes done! Found {len(nitrates_index)}")


# This is the main part of the code for finding Nitrites
nitrites_index, first_keywords, foundWithSpace = matchesAnyIndex(dataFrame, Nitrites_NO_exact, Nitrites_NO_all, negative_keywords=Nitrates_NO_all)
subset = dataFrame.iloc[nitrites_index]
subset.insert(7, "Found only with space", foundWithSpace, True)
subset.insert(7, "KeyWord", first_keywords, True)

#with a possibility of matching with KBS, that was not performed here (this part was not working well)
if fuzzyMatchCodes:
    foodCodes = []
    foodCodeScores = []
    matchStrings = []
    for cell in subset["Markedsnavn"]:
        bestMatch = "NA"
        matchedTo = "NA"
        matchScore = 0
        for key in codesMap.keys():
            score = fuzz.token_sort_ratio(cell.strip().lower(), key.strip().lower() )
            #score = fuzz.partial_token_set_ratio(cell.strip().lower(), key.strip().lower() )
            if score > matchScore:
                matchScore = score
                bestMatch = codesMap[key]
                matchedTo = key
        foodCodes.append(bestMatch)
        foodCodeScores.append(matchScore)
        matchStrings.append(matchedTo)
    subset.insert(1, "FoodCode", foodCodes, True)
    subset.insert(1, "FuzzyScore", foodCodeScores, True)
    subset.insert(1, "MatchedTo", matchStrings, True)
with ExcelWriter(folder + f"/Nitrites_NO{fileSuffix}.xlsx") as writer:
    subset.to_excel(writer)
print(f"nitrItes done! Found {len(nitrites_index)}")

# This is the main part of the code for finding Extracts 
extracts_index, first_keywords, foundWithSpace = matchesAnyIndex(dataFrame, Extracts_NO_exact, Extracts_NO_fuzzy)
subset = dataFrame.iloc[extracts_index]
subset.insert(7, "Found only with space", foundWithSpace, True)
subset.insert(7, "KeyWord", first_keywords, True)

#with a possibility of matching with KBS, that was not performed here (this part was not working well)
if fuzzyMatchCodes:
    foodCodes = []
    foodCodeScores = []
    matchStrings = []
    for cell in subset["Markedsnavn"]:
        bestMatch = "NA"
        matchedTo = "NA"
        matchScore = 0
        for key in codesMap.keys():
            score = fuzz.token_sort_ratio(cell.strip().lower(), key.strip().lower() )
            #score = fuzz.partial_token_set_ratio(cell.strip().lower(), key.strip().lower() )
            if score > matchScore:
                matchScore = score
                bestMatch = codesMap[key]
                matchedTo = key
        foodCodes.append(bestMatch)
        foodCodeScores.append(matchScore)
        matchStrings.append(matchedTo)
    subset.insert(1, "FoodCode", foodCodes, True)
    subset.insert(1, "FuzzyScore", foodCodeScores, True)
    subset.insert(1, "MatchedTo", matchStrings, True)
with ExcelWriter(folder + f"/Extracts_NO{fileSuffix}.xlsx") as writer:
    subset.to_excel(writer)
print(f"extracts done! Found {len(extracts_index)}")

# This is the main part of the code for finding Foods
foods_index, first_keywords, foundWithSpace = matchesAnyIndex(dataFrame, Foods_NO_exact, Foods_NO_fuzzy)
subset = dataFrame.iloc[foods_index]
subset.insert(7, "Found only with space", foundWithSpace, True)
subset.insert(7, "KeyWord", first_keywords, True)

#with a possibility of matching with KBS, that was not performed here (this part was not working well)
if fuzzyMatchCodes:
    foodCodes = []
    foodCodeScores = []
    matchStrings = []
    for cell in subset["Markedsnavn"]:
        bestMatch = "NA"
        matchedTo = "NA"
        matchScore = 0
        for key in codesMap.keys():
            score = fuzz.token_sort_ratio(cell.strip().lower(), key.strip().lower() )
            #score = fuzz.partial_token_set_ratio(cell.strip().lower(), key.strip().lower() )
            if score > matchScore:
                matchScore = score
                bestMatch = codesMap[key]
                matchedTo = key
        foodCodes.append(bestMatch)
        foodCodeScores.append(matchScore)
        matchStrings.append(matchedTo)
    subset.insert(1, "FoodCode", foodCodes, True)
    subset.insert(1, "FuzzyScore", foodCodeScores, True)
    subset.insert(1, "MatchedTo", matchStrings, True)
with ExcelWriter(folder + f"/Foods_NO{fileSuffix}.xlsx") as writer:
    subset.to_excel(writer)
print(f"foods done! Found {len(foods_index)}")

# The results of these search can be input for VennDiagrams
