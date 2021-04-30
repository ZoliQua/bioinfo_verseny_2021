#
# Semmelweis Bioinformatika verseny pályázat 2021
#
# Készítette: Dr. Dul Zoltán, PhD
# 				a Semmelweis EMK MSc képzésének másodéves hallgatója
#

from trainer_functions import *
from trainer_variables import *

# Set filenames
filename = my_data_folder + "/" + my_data_filename
filename_ch0_ho1 = my_data_folder + "/" + export_filename_ch0_ho1
filename_ch1_ho0 = my_data_folder + "/" + export_filename_ch1_ho0
filename_ch1_ho1 = my_data_folder + "/" + export_filename_ch1_ho1
filename_stat = my_data_folder + "/" + statistics_filename
filename_export = my_data_folder + "/" + export_filename

# Load statistics of train data into pandas dataframe
stat = pd.read_csv(filename_stat)
stat_significant = stat.loc[stat['significance'] == 1]

# Collect significantly positive conditions to positive_list array
positive_list = []

for iter_item in stat_significant.iterrows():

	this_row = {}
	this_row["index"] = iter_item[0]

	if iter_item[1]["type"][0:5] == "chemo":
		this_row["adjuvant_chemotherapy"] = [1]
	elif iter_item[1]["type"][0:5] == "hormo":
		this_row["hormone_therapy"] = [1]

	if (len(iter_item[1]["type"]) > 8):
		if iter_item[1]["type"][8:13] == "chemo":
			this_row["adjuvant_chemotherapy"] = [1]
		elif iter_item[1]["type"][8:13] == "hormo":
			this_row["hormone_therapy"] = [1]

	if iter_item[1]["condition_value"].count("_") > 0:
		sub_items = iter_item[1]["condition_value"].split("_")
	else:
		sub_items = [iter_item[1]["condition_value"]]

	this_row[iter_item[1]["main_condition"]] = sub_items

	if type(iter_item[1]["sub_condition"]) == str:
		sub_items = iter_item[1]["sub_condition_value"].split("_")
		this_row[iter_item[1]["sub_condition"]] = [int(sub_items[1]), int(sub_items[2])]

	positive_list.append(this_row)

# Load the data into pandas dataframe
source_data = pd.read_csv(filename)

list_of_sign = []
new_column_1 = []
new_column_2 = []
new_column_3 = []
new_column_4 = []

# Iterate data and check if the data row is satisfies any of the positvie list conditions
for iter_item in source_data.iterrows():

	satisfied_indexes = []
	chemo = 0
	hormon = 0

	for condition in positive_list:

		not_satisfied_conditions = len(condition)-1

		for cell_name in condition:

			if cell_name == "index":
				continue

			# Filter conditions with one element like: hormone_therapy [1]
			if len(condition[cell_name]) == 1:
				if iter_item[1][cell_name] == condition[cell_name][0]:
					not_satisfied_conditions -= 1
					if cell_name == 'adjuvant_chemotherapy':
						chemo = 1
					if cell_name == 'hormone_therapy':
						hormon = 1

			# Filter conditions with two elements like: age_at_diagnosis or pathologic_stat (combined)
			if len(condition[cell_name]) >= 2:
				# Filter conditions with two elements like: age_at_diagnosis [66, 100] for between
				if type(condition[cell_name][0]) == int and type(condition[cell_name][1]) == int:
					if iter_item[1][cell_name] >= condition[cell_name][0] and iter_item[1][cell_name] <= condition[cell_name][1]:
						not_satisfied_conditions -= 1
				else:
					# Filter conditions like : pathologic_stat (combined)
					for value in condition[cell_name]:
						if iter_item[1][cell_name] == value:
							not_satisfied_conditions -= 1
							break

			if not_satisfied_conditions == 0 and iter_item[0] not in list_of_sign:
				list_of_sign.append(iter_item[0])

			if not_satisfied_conditions == 0:
				satisfied_indexes.append(condition)

		# if iter_item[0] in list_of_sign:
		# 	break

	if iter_item[0] in list_of_sign:
		new_column_1.append(1)
		new_column_2.append(satisfied_indexes)
		new_column_3.append(chemo)
		new_column_4.append(hormon)

	else:
		new_column_1.append(0)
		new_column_2.append(0)
		new_column_3.append(0)
		new_column_4.append(0)

# Print the number of significant patients
print(f"Classifier have found {len(list_of_sign)} significantly effectively treated patients out of {len(source_data)}.")

# Adding significance indicating columns to the export file
source_data["significance"] = new_column_1
source_data["significance_reason"] = new_column_2
source_data["adjuvant_chemotherapy_sign"] = new_column_3
source_data["hormone_therapy_sign"] = new_column_4

source_data_ch1_ho0 = source_data[(source_data["adjuvant_chemotherapy_sign"] == 1) & (source_data["hormone_therapy_sign"] == 0)]
source_data_ch0_ho1 = source_data[(source_data["adjuvant_chemotherapy_sign"] == 0) & (source_data["hormone_therapy_sign"] == 1)]
source_data_ch1_ho1 = source_data[(source_data["adjuvant_chemotherapy_sign"] == 1) & (source_data["hormone_therapy_sign"] == 1)]

# Export results into a csv file
source_data.to_csv(filename_export, index=False)
source_data_ch1_ho0.to_csv(filename_ch1_ho0, index=False)
source_data_ch0_ho1.to_csv(filename_ch0_ho1, index=False)
source_data_ch1_ho1.to_csv(filename_ch1_ho1, index=False)

# Print summary for the console
print(f"Classifier have exported all patients results into {filename_export}.")
print(f"Classifier have found {len(source_data_ch1_ho0)} where only adj. chemotherpy was significantly effective.")
print(f"Classifier exported it into {filename_ch1_ho0}.")
print(f"Classifier have found {len(source_data_ch0_ho1)} where only hormontherapy was significantly effective.")
print(f"Classifier exported it into {filename_ch0_ho1}.")
print(f"Classifier have found {len(source_data_ch1_ho1)} where both therapies were significantly effective.")
print(f"Classifier exported it into {filename_ch1_ho1}.")

