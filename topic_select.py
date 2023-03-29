import csv
from topics_listall import topics

# John Wang
# make sure you have topics_listall.py, merged_data.csv
# make sure you have topic_label.csv(or any topic csv you have labeled, related topics marked as "o" at first column)

with open('./topic_label.csv', 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

targets = [int(row[1]) for row in data if row[0] == 'o'] # select from labeled topics


arr = topics
# targets = [2, 5] # select from specific topics

all_positions = [index for index, value in enumerate(arr) if value in targets]

# for pos in all_positions:
#     print(pos)

with open('merged_data.csv', 'r', encoding='utf-8-sig') as merged_file:
    merged_data = list(csv.reader(merged_file))

# save the filtered result in a new csv
with open('filtered_data.csv', 'w', encoding='utf-8-sig', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    
    for pos in all_positions:
        row_number = pos + 1
        csv_writer.writerow(merged_data[row_number])