# This python scrip is producing venn diagram and venn intersection (excel files)
# using the previously created files for individual items  

from pandas import read_excel, ExcelWriter
import sys
import os.path
#sys.exit(0)

#homedir = "C:/Users/maww/Desktop/"
homedir = "C:/Users/maww/Documents/Python_Scripts/VKM-P001/"


folder_in = homedir+"21.09.2024_venn/inputs"
folder_out = homedir+"21.09.2024_venn/outputs"
fileSuffix = "_combined_2109" #these need to be produced from previous python script


if not os.path.exists(folder_out):
    os.makedirs(folder_out)

for i in [2,3,4]:
    if not os.path.exists(os.path.join(folder_out, f"Venn{i}")):
        os.makedirs(os.path.join(folder_out, f"Venn{i}"))


countFileAddress = folder_out + f"/Count_venn_objects.txt"

with open(folder_in + f"/Nitrates_NO{fileSuffix}.xlsx", "rb") as newFile:
    nitrates_data = read_excel(newFile)
with open(folder_in + f"/Nitrites_NO{fileSuffix}.xlsx", "rb") as newFile:
    nitrites_data = read_excel(newFile)
with open(folder_in + f"/Extracts_NO{fileSuffix}.xlsx", "rb") as newFile:
    extracts_data = read_excel(newFile)
with open(folder_in + f"/Foods_NO{fileSuffix}.xlsx", "rb") as newFile:
    foods_data = read_excel(newFile)


nitrates_index = list(nitrates_data["Unnamed: 0"].values)
nitrites_index = list(nitrites_data["Unnamed: 0"].values)
extracts_index = list(extracts_data["Unnamed: 0"].values)
foods_index = list(foods_data["Unnamed: 0"].values)
#print(nitrates_indexes)

print(len(nitrates_index))
print(len(nitrites_index))
print(len(extracts_index))
print(len(foods_index))



venn2_nitrates = list(set(nitrates_index).difference(nitrites_index))
venn2_nitrites = list(set(nitrites_index).difference(nitrates_index))
venn2_nitrates_nitrites = list(set(nitrates_index).intersection(nitrites_index))


venn3_nitrates = list(set(nitrates_index).difference(nitrites_index).difference(foods_index))
venn3_nitrites = list(set(nitrites_index).difference(nitrates_index).difference(foods_index))
venn3_nitrates_nitrites = list(set(nitrates_index).intersection(nitrites_index).difference(foods_index))
venn3_foods = list(set(foods_index).difference(nitrates_index).difference(nitrites_index))
venn3_nitrates_foods = list(set(nitrates_index).intersection(foods_index).difference(nitrites_index))
venn3_nitrites_foods = list(set(nitrites_index).intersection(foods_index).difference(nitrates_index))
venn3_nitrates_nitrites_foods = list(set(nitrates_index).intersection(nitrites_index).intersection(foods_index))



venn4_nitrates = list(set(nitrates_index).difference(nitrites_index).difference(extracts_index).difference(foods_index))                                  #1000 #233 
venn4_nitrites = list(set(nitrites_index).difference(nitrates_index).difference(extracts_index).difference(foods_index))                                  #0100 #3680
venn4_nitrates_nitrites = list(set(nitrates_index).intersection(nitrites_index).difference(extracts_index).difference(foods_index))                       #1100 #271 
venn4_extracts = list(set(extracts_index).difference(nitrates_index).difference(nitrites_index).difference(foods_index))                                  #0010 #286 
venn4_nitrates_extracts = list(set(nitrates_index).intersection(extracts_index).difference(nitrites_index).difference(foods_index))                       #1010 #0 
venn4_nitrites_extracts = list(set(nitrites_index).intersection(extracts_index).difference(nitrates_index).difference(foods_index))                       #0110 #19 
venn4_nitrates_nitrites_extracts = list(set(nitrates_index).intersection(nitrites_index).intersection(extracts_index).difference(foods_index))            #1110 #0 
venn4_foods = list(set(foods_index).difference(nitrates_index).difference(nitrites_index).difference(extracts_index))                                     #0001 #1435
venn4_nitrates_foods = list(set(nitrates_index).intersection(foods_index).difference(nitrites_index).difference(extracts_index))                          #1001 #12 
venn4_nitrites_foods = list(set(nitrites_index).intersection(foods_index).difference(nitrates_index).difference(extracts_index))                          #0101 #147 
venn4_nitrates_nitrites_foods = list(set(nitrates_index).intersection(nitrites_index).intersection(foods_index).difference(extracts_index))               #1101 #15 
venn4_extracts_foods = list(set(extracts_index).intersection(foods_index).difference(nitrates_index).difference(nitrites_index))                          #0011 #95 
venn4_nitrates_extracts_foods = list(set(nitrates_index).intersection(extracts_index).intersection(foods_index).difference(nitrites_index))               #1011 #0 
venn4_nitrites_extracts_foods = list(set(nitrites_index).intersection(extracts_index).intersection(foods_index).difference(nitrates_index))               #0111 #3 
venn4_nitrates_nitrites_extracts_foods = list(set(nitrates_index).intersection(nitrites_index).intersection(extracts_index).intersection(foods_index))    #1111 #0 


with open(countFileAddress, "w") as countFile:
    #Printing count information
    print(f"For Venn2: nitrates only = {len(venn2_nitrates)}", file=countFile)
    print(f"For Venn2: nitrites only = {len(venn2_nitrites)}", file=countFile)
    print(f"For Venn2: nitrates and nitrites = {len(venn2_nitrates_nitrites)}", file=countFile)

    print(f"For Venn3: nitrates only = {len(venn3_nitrates)}", file=countFile)
    print(f"For Venn3: nitrites only = {len(venn3_nitrites)}", file=countFile)
    print(f"For Venn3: nitrates and nitrites = {len(venn3_nitrates_nitrites)}", file=countFile)
    print(f"For Venn3: foods = {len(venn3_foods)}", file=countFile)
    print(f"For Venn3: nitrates and food only= {len(venn3_nitrates_foods)}", file=countFile)
    print(f"For Venn3: nitrites and food only = {len(venn3_nitrites_foods)}", file=countFile)
    print(f"For Venn3: nitrates, nitrites and food = {len(venn3_nitrates_nitrites_foods)}", file=countFile)


    print(f"For Venn4: nitrates only = {len(venn4_nitrates)}", file=countFile)
    print(f"For Venn4: nitrites only = {len(venn4_nitrites)}", file=countFile)
    print(f"For Venn4: nitrates and nitrites only = {len(venn4_nitrates_nitrites)}", file=countFile)
    print(f"For Venn4: extracts only = {len(venn4_extracts)}", file=countFile)
    print(f"For Venn4: nitrates and extracts only = {len(venn4_nitrates_extracts)}", file=countFile)
    print(f"For Venn4: nitrites and extracts only = {len(venn4_nitrites_extracts)}", file=countFile)
    print(f"For Venn4: nitrates, nitrites and extracts only = {len(venn4_nitrates_nitrites_extracts)}", file=countFile)
    print(f"For Venn4: foods only = {len(venn4_foods)}", file=countFile)
    print(f"For Venn4: nitrates and foods only = {len(venn4_nitrates_foods)}", file=countFile)
    print(f"For Venn4: nitrites and foods only = {len(venn4_nitrites_foods)}", file=countFile)
    print(f"For Venn4: nitrates, nitrites and foods only = {len(venn4_nitrates_nitrites_foods)}", file=countFile)
    print(f"For Venn4: extracts and foods only = {len(venn4_extracts_foods)}", file=countFile)
    print(f"For Venn4: nitrates, extracts and foods only = {len(venn4_nitrates_extracts_foods)}", file=countFile)
    print(f"For Venn4: nitrites, extracts and foods only = {len(venn4_nitrites_extracts_foods)}", file=countFile)
    print(f"For Venn4: everything = {len(venn4_nitrates_nitrites_extracts_foods)}", file=countFile)

with open(countFileAddress, "r") as textFile:
    for line in textFile:
        print(line)


# Producing interesction for two sets (nitrates and nitrites). Excel files produced will have prefix Venn2.

if len(venn2_nitrates) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn2_nitrates)]
    with ExcelWriter(folder_out + f"/Venn2/Venn2_IntersectionOf_Nitrates_Excluding_Nitrites{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

if len(venn2_nitrites) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn2_nitrites)]
    with ExcelWriter(folder_out + f"/Venn2/Venn2_IntersectionOf_Nitrites_Excluding_Nitrates{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

if len(venn2_nitrates_nitrites) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn2_nitrates_nitrites)]
    with ExcelWriter(folder_out + f"/Venn2/Venn2_IntersectionOf_Nitrites-Nitrites_Excluding_None{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)



#three set
# Producing interesction for three sets only nitrates, nitrites and foods. Excel files produced will have prefix Venn3.


if len(venn3_nitrates) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn3_nitrates)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Nitrates_Excluding_Nitrites-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

if len(venn3_nitrites) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn3_nitrites)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Nitrites_Excluding_Nitrates-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)
        
if len(venn3_nitrates_nitrites) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn3_nitrates_nitrites)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Nitrates-Nitrites_Excluding_Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)
        
if len(venn3_foods) > 0:
    subset = foods_data[foods_data["Unnamed: 0"].isin(venn3_foods)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Foods_Excluding_Nitrates-Nitrites{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

if len(venn3_nitrates_foods) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn3_nitrates_foods)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Nitrates-Foods_Excluding_Nitrites{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

if len(venn3_nitrites_foods) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn3_nitrites_foods)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Nitrites-Foods_Excluding_Nitrates{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

if len(venn3_nitrates_nitrites_foods) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn3_nitrates_nitrites_foods)]
    with ExcelWriter(folder_out + f"/Venn3/Venn3_IntersectionOf_Nitrates-Nitrites-Foods_Excluding_None{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)

#four set
# Producing interesction for three sets only nitrates, nitrites, foods and extracts. 
# Excel files produced will have prefix Venn4.


if len(venn4_nitrates) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates_Excluding_Nitrites-Extracts-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)
    

if len(venn4_nitrites) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn4_nitrites)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrites_Excluding_Nitrates-Extracts-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_nitrites) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_nitrites)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Nitrites_Excluding_Extracts-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_extracts) > 0:
    subset = extracts_data[extracts_data["Unnamed: 0"].isin(venn4_extracts)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Extracts_Excluding_Nitrates-Nitrites-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_extracts) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_extracts)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Extracts_Excluding_Nitrites-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrites_extracts) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn4_nitrites_extracts)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrites-Extracts_Excluding_Nitrates-Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_nitrites_extracts) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_nitrites_extracts)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Nitrites-Extracts_Excluding_Foods{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_foods) > 0:
    subset = foods_data[foods_data["Unnamed: 0"].isin(venn4_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Foods_Excluding_Nitrates-Nitrites-Extracts{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_foods) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Foods_Excluding_Nitrites-Extracts{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrites_foods) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn4_nitrites_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrites-Foods_Excluding_Nitrates-Extracts{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_nitrites_foods) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_nitrites_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Nitrites-Foods_Excluding_Extracts{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_extracts_foods) > 0:
    subset = extracts_data[extracts_data["Unnamed: 0"].isin(venn4_extracts_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Extracts-Foods_Excluding_Nitrates-Nitrites{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_extracts_foods) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_extracts_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Extracts-Foods_Excluding_Nitrites{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrites_extracts_foods) > 0:
    subset = nitrites_data[nitrites_data["Unnamed: 0"].isin(venn4_nitrites_extracts_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrites-Extracts-Foods_Excluding_Nitrates{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


if len(venn4_nitrates_nitrites_extracts_foods) > 0:
    subset = nitrates_data[nitrates_data["Unnamed: 0"].isin(venn4_nitrates_nitrites_extracts_foods)]
    with ExcelWriter(folder_out + f"/Venn4/Venn4_IntersectionOf_Nitrates-Nitrites-Extracts-Foods_Excluding_None{fileSuffix}.xlsx") as writer:
        subset.to_excel(writer)


from venny4py.venny4py import *
sets2 = {
    'Nitrates': set(nitrates_index),
    'Nitrites': set(nitrites_index)}

venny4py(sets=sets2, size=8, dpi=600, out=folder_out+'/Venn2', ext='png', colors='crgb', legend_cols=4, edge_color='black', column_spacing=2, line_width=.5)

sets3 = {
    'Nitrates': set(nitrates_index),
    'Nitrites': set(nitrites_index),
    'Foods': set(foods_index)}

venny4py(sets=sets3, size=8, dpi=600, out=folder_out+'/Venn3', ext='png', colors='crgb', legend_cols=4, edge_color='black', column_spacing=2, line_width=.5)

sets4 = {
    'Nitrates': set(nitrates_index),
    'Nitrites': set(nitrites_index),
    'Extracts': set(extracts_index),
    'Foods': set(foods_index)}

venny4py(sets=sets4, size=8, dpi=600, out=folder_out+'/Venn4', ext='png', colors='crgb', legend_cols=4, edge_color='black', column_spacing=2, line_width=.5)
#plt.show()


