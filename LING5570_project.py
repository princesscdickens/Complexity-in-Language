# Language Complexity and Infrastructure

# Hypothesis: Language complexity is correlated with isolation (poor infrastructure)
# How can one define complexity in language?
# --> multiple means of encoding? (obligatory?)

# I'm going to map out the geographic distribution of 'complex' languages
# I define complex as multiple means of encoding

# language.csv taken from WALS corpus
# 2679 languages
# 192 potential features
# I will focus on morpho-syntactic features
# I will exclude languages for which there exists little data.

'''
1. Read in '/Users/pdickens/Dropbox/LING 5570 Diachronic Ling/wals_language/language.csv'
2. Create list of features and decide which features contribute to complexity
(perhaps with a simpler table)
3. For those features, if the present language has multple means of encoding them, 
add 1 point for complexity for each 'extra' feature 
--> This can be a dictionary: {name_lang: 
									{complexity_score: count, latitude: number, longitude: number}}
4. Write this dictionary to a .txt file
5. Search for infrastructure data and compare results.
'''

import csv

file_path = 'ExtractedFeatures.csv'
feature_names = []
all_values = []

with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    language_count = 0
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            feature_names = row
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            language_count += 1
            current_values = row
            all_values.append((language_count,current_values)) #2-tuple (language#, list of values as strings)
        line_count += 1
        

    print('Processed:', line_count, 'lines')
    print('Feature names 0-5: ', feature_names[0:5])
    print('Values[0]: ', all_values[0])
    #print('Values[1]: ', all_values[1])
    #print('Values[2]: ', all_values[2])
    #print('Values[3]: ', all_values[3])
    print('Values[8]: ', all_values[8])
# Values[8]:  (9, ['Abkhaz', '43.08333333', '41', 'Northwest Caucasian', '1 Exclusively concatenative', 
# '5 No case', '1 monoexponential TAM', '1 Head marking', '1 Head marking', '1 Head-marking', 
# '2 Non-zero marking', '1 No case marking', '3 Three', '3 Not syncretic', '0'])

'''
Column names are: 
Name, latitude, longitude, family, 
Morphology
20A Fusion of Selected Inflectional Formatives, 
21A Exponence of Selected Inflectional Formatives, 
21B Exponence of Tense-Aspect-Mood Inflection, 
22A Inflectional Synthesis of the Verb
23A Locus of Marking in the Clause, 
24A Locus of Marking in Possessive Noun Phrases, 
25A Locus of Marking: Whole-language Typology, *
25B Zero Marking of A and P Arguments
27A Reduplication,
28A Case Syncretism, 
29A Syncretism in Verbal Person/Number Marking,
30A Number of Genders, (Nominal Categories)
34A Occurrence of Nominal Plurality
39A Inclusive/Exclusive Distinction in Independent Pronouns
40A Inclusive/Exclusive Distinction in Verbal Inflection
41A Distance Contrasts in Demonstratives
42A Pronominal and Adnominal Demonstratives
44A Gender Distinctions in Independent Personal Pronouns
45A Politeness Distinctions in Pronouns
47A Intensifiers and Reflexive Pronouns
48A Person Marking on Adpositions
51A Position of Case Affixes
52A Comitatives and Instrumentals
54A Distributive Numerals
55A Numeral classifiers
58A Obligatory Possessive Inflection (Nominal Syntax)
59A Possessive Classification
61A Adjectives without Nouns
63A Noun Phrase Conjunction
65A Perfective/Imperfective Aspect (Verbal Categories)
66A The Past Tense
67 The Future Tense
68A The Perfect 
69A Positive of Tense-Aspect Affixes
70A The Morphologicla Imperative
72A Imperative-Hortative Systems
73A The Optative
76A Overlap between Situational and Epistemic Modal Marking
77A Semantic Distinctions of Evidentiality
79A Suppletion According to Tense and Aspect
NumBlanks
'''

# Only keep languages for which there is sufficient data
filteredLangs = []

for item in all_values:
    numBlanks = item[1][-1]
    #print('Lang: ', item[1][0], ', numBlanks:', numBlanks)
    if int(numBlanks) < 5: #if there's fewer than 5 blanks (10%)--> actually 36/39 (92%), or if there's 8 or fewer features missing (20%), 
        filteredLangs.append((item[1], {'score':0})) #2-tuple ([feature_list], {score:0})

#print('all_values[-1][1][0:-1]: ', all_values[-1][1][0:-1]) #This is the bottom line
print('Number langs saved:', len(filteredLangs)) #121

for item in filteredLangs:
    # ------ Morphology ------
    if 'Exclusively' in item[0][4]: #20A Fusion of Selected Inflectional Formatives
        item[1]['score'] += 1
    else:
        item[1]['score'] += 2

    if 'Monoexponential' in item[0][5]: #21A Exponence of Selected Inflectional Formatives
        item[1]['score'] += 1
    elif '+' in item[0][5]:
        item[1]['score'] += 2

    if 'Monoexponential' in item[0][6]: #21B Exponence of Tense-Aspect-Mood Inflection
        item[1]['score'] += 1
    elif '+' in item[0][6]:
        item[1]['score'] += 2

    if '3' in item[0][6] or '4' in item[0][6]:
        item[1]['score'] += 1

    #22A Inflectionla Synthesis of the verb
    if item[0][7] == '2 2-3 categories per word' or item[0][7] == '3 4-5 categories per word':
        item[1]['score'] += 1
    elif item[0][7] == '4 6-7 categories per word' or item[0][7] == '5 8-9 categories per word':
        item[1]['score'] += 2
    elif item[0][7] == '6 10-11 categories per word' or item[0][7] == '7 12-13 categories per word':
        item[1]['score'] += 3

    if '3' in item[0][8]: #23A Locus of Marking in the Clause
        item[1]['score'] += 2
    elif '1' in item[0][8] or '2' in item[0][8] or '5' in item[0][8]:
        item[1]['score'] += 1

    if '3' in item[0][9]: #24A Locus of Marking in Possessive Noun Phrases
        item[1]['score'] += 2
    elif '1' in item[0][9] or '2' in item[0][9] or '5' in item[0][9]:
        item[1]['score'] += 1

    #25A Locus of Marking: Whole-language Typology 
    if '3' in item[0][10]: 
        item[1]['score'] += 2
    elif '1' in item[0][10] or '2' in item[0][10] or '5' in item[0][10]:
        item[1]['score'] += 1

    #27A Reduplication
    if '1' in item[0][11] or '2' in item[0][11]: 
        item[1]['score'] += 1

    #28A Case Syncretism 
    if '2' in item[0][12] or '3' in item[0][12] or '4' in item[0][12]: 
        item[1]['score'] += 1

    #29A Syncretism in Verbal Person/Number Marking
    if '2' in item[0][13] or '3' in item[0][13]: 
        item[1]['score'] += 1

    # ------ Nominal Categories ------
    #30A Number of Genders 
    if '1' in item[0][14]:
        item[1]['score'] += 1
    elif '2' in item[0][14] or '3' in item[0][14]: 
        item[1]['score'] += 2
    elif '4' in item[0][14]: 
        item[1]['score'] += 3

    #34A Occurrence of Nominal Plurality
    if '6' in item[0][15]: #obligatory, ALL nouns
        item[1]['score'] += 1
    elif '3' in item[0][15] or '4' in item[0][15] or '5' in item[0][15]: #optional or only in human nouns
        item[1]['score'] += 2
    elif '2' in item[0][15]: #both optional and only in human nouns
        item[1]['score'] += 3

    #39A Inclusive/Exclusive Distinction in Independent Pronouns
    if '3' in item[0][16]: 
        item[1]['score'] += 1
    elif '4' in item[0][16]: 
        item[1]['score'] += 2
    elif '5' in item[0][16]: 
        item[1]['score'] += 3

    #40A Inclusive/Exclusive Distinction in Verbal Inflection
    if '3' in item[0][17]: 
        item[1]['score'] += 1
    elif '4' in item[0][17]: 
        item[1]['score'] += 2
    elif '5' in item[0][17]: 
        item[1]['score'] += 3

    #41A Distance Contrasts in Demonstratives
    if '2' in item[0][18]: 
        item[1]['score'] += 1
    elif '3' in item[0][18]: 
        item[1]['score'] += 2
    elif '4' in item[0][18] or '5' in item[0][18]: 
        item[1]['score'] += 3

    #42A Pronominal and Adnominal Demonstratives
    if '2' in item[0][19]: #different stems
        item[1]['score'] += 1
    elif '3' in item[0][19]: #inflection
        item[1]['score'] += 2

    #44A Gender Distinctions in Independent Personal Pronouns
    if '1' in item[0][20] or '2' in item[0][20]: # +1 for person or plurality distinctions
        item[1]['score'] += 2
    elif '3' in item[0][20] or '4' in item[0][20] or '5' in item[0][20]: # 1 person
        item[1]['score'] += 1

    #45A Politeness Distinctions in Pronouns
    if '1' in item[0][21] or '2' in item[0][21] or '4' in item[0][21]:
        item[1]['score'] += 1
    elif '3' in item[0][21]:
        item[1]['score'] += 2

    #47A Intensifiers and Reflexive Pronouns
    if '2' in item[0][22]:
        item[1]['score'] += 1

    #48A Person Marking on Adpositions
    if '2' in item[0][23]: 
        item[1]['score'] += 1
    elif '3' in item[0][23]: 
        item[1]['score'] += 2
    elif '4' in item[0][23]: 
        item[1]['score'] += 3

    #51A Position of Case Affixes
    if '5' in item[0][24]: 
        item[1]['score'] += 2
    elif '1' in item[0][24] or '2' in item[0][24] or '3' in item[0][24] or '4' in item[0][24] or '6' in item[0][24] or '7' in item[0][24] or '8' in item[0][24]: 
        item[1]['score'] += 1

    #52A Comitatives and Instrumentals
    if '1' in item[0][25]: 
        item[1]['score'] += 1
    elif '2' in item[0][25]: 
        item[1]['score'] += 2
    elif '3' in item[0][25]: 
        item[1]['score'] += 3

    #54A Distributive Numerals
    if '7' in item[0][26]: 
        item[1]['score'] += 2
    elif '2' in item[0][26] or '3' in item[0][26] or '4' in item[0][26] or '5' in item[0][26] or '6' in item[0][26]: 
        item[1]['score'] += 1

    #55A Numeral classifiers
    if '3' in item[0][27]: 
        item[1]['score'] += 1
    elif '2' in item[0][27]: 
        item[1]['score'] += 2

    #----------- Nominal Syntax -------------

    #58A Obligatory Possessive Inflection
    if '1' in item[0][28]: 
        item[1]['score'] += 1

    #59A Possessive Classification
    if '2' in item[0][29]: 
        item[1]['score'] += 1
    elif '3' in item[0][29]: 
        item[1]['score'] += 2
    elif '4' in item[0][29]: 
        item[1]['score'] += 3

    #61A Adjectives without Nouns
    if '2' in item[0][30]: 
        item[1]['score'] += 1
    elif '3' in item[0][30] or '4' in item[0][30] or '5' in item[0][30] or '6' in item[0][30]: 
        item[1]['score'] += 2
    elif '7' in item[0][30]: 
        item[1]['score'] += 3

    #63A Noun Phrase Conjunction
    if '1' in item[0][31]: 
        item[1]['score'] += 1

    #----------- Verbal Categories -------------

    #65A Perfective/Imperfective Aspect
    if '1' in item[0][32]: 
        item[1]['score'] += 1

    #66A The Past Tense
    if '1' in item[0][33]: 
        item[1]['score'] += 1
    elif '2' in item[0][33]: 
        item[1]['score'] += 2
    elif '4' in item[0][33]: 
        item[1]['score'] += 3

    #67 The Future Tense
    if '1' in item[0][34]: 
        item[1]['score'] += 1

    #68A The Perfect 
    if '1' in item[0][35] or '2' in item[0][35] or '3' in item[0][35]: 
        item[1]['score'] += 1

    #69A Positive of Tense-Aspect Affixes
    if '1' in item[0][36] or '2' in item[0][36] or '3' in item[0][36]: 
        item[1]['score'] += 1
    elif '4' in item[0][36]: 
        item[1]['score'] += 2

    #70A The Morphologicla Imperative
    if '4' in item[0][37]: 
        item[1]['score'] += 1
    elif '2' in item[0][37] or '3' in item[0][37]: 
        item[1]['score'] += 2
    elif '1' in item[0][37]: 
        item[1]['score'] += 3

    #72A Imperative-Hortative Systems
    if '1' in item[0][38] or '2' in item[0][38]: 
        item[1]['score'] += 1
    elif '3' in item[0][38]: 
        item[1]['score'] += 2

    #73A The Optative
    if '1' in item[0][39]: 
        item[1]['score'] += 1

    #76A Overlap between Situational and Epistemic Modal Marking
    if '1' in item[0][40]: 
        item[1]['score'] += 2
    elif '2' in item[0][40]: 
        item[1]['score'] += 1

    #77A Semantic Distinctions of Evidentiality
    if '2' in item[0][41]: 
        item[1]['score'] += 1
    elif '3' in item[0][41]: 
        item[1]['score'] += 2

    #79A Suppletion According to Tense and Aspect
    if '1' in item[0][42] or '2' in item[0][41]: 
        item[1]['score'] += 1
    elif '3' in item[0][42]: 
        item[1]['score'] += 2


print('Status:', filteredLangs[0][0][0], '-', filteredLangs[0][1])
print('Status:', filteredLangs[1][0][0], '-', filteredLangs[1][1])

fileObject = open('complexity_score_90.txt', 'a')
# (['Acoma', '34.91666667', '-107.5833333', 'Keresan',...], {'score': 6})
headers = 'Language\t' + 'Latitude\t' + 'Longitude\t' + 'Family\t' + 'Complexity Score\n'
fileObject.write(headers)

for item in filteredLangs:
    # name lat long family score
    fileObject.write(item[0][0] + '\t' + item[0][1] + '\t' + item[0][2] + '\t' + item[0][3] + '\t' + str(item[1]['score']) + '\n')

fileObject.close()

