import csv

# John Wang
# Make sure you have topic_keywordsall.csv

with open('./topic_keywordsall.csv', 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

for row in data:
    row.insert(0, '')

english_keywords = ['kill', 'killed', 'dead', 'death', 'bullet', 'shoot', 'shot', 'stab', 'stabbed', 'blunt', 'r.i.p.', 'homicide', 'gun', 'violence', 'rip', 'rest in peace', 'murder', 'murdered', 'police', 'crime', 'rob','steal']

spanish_keywords = ['matar', 'asesinado', 'muerto', 'muerte','bala', 'disparar', 'apuñalar', 'contundente', 'rip', 'homicidio', 'arma', 'violencia ', 'rasgar', 'descanse en paz', 'asesinato', 'policía', 'crimen', 'robar']

# filter
for row in data[1:]:
    if 'leyder' in row[2] and 'cárdenas' in row[2]:
        row[0] = 'x' #mark
    elif any(keyword in row[2] for keyword in english_keywords):
        row[0] = 'o'
    elif any(keyword in row[2] for keyword in spanish_keywords):
        row[0] = 'o'
    else:
        row[0] = ''


with open('topic_label.csv', 'w', newline='', encoding='utf-8-sig') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)