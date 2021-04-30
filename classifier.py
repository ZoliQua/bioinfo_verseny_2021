#
# Semmelweis Bioinformatika verseny pályázat 2021
#
# Készítette: Dr. Dul Zoltán, PhD
# 				a Semmelweis EMK MSc képzésének másodéves hallgatója
#

from trainer_functions import *
from trainer_variables import *

# Print start time to the console
start_time = time.time()
TimeNow("start", "classifier.py")

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

	if iter_item[1]["radiotherapy"] != "x":
		this_row["radiation_therapy"] = [iter_item[1]["radiotherapy"]]

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
		if iter_item[1]["sub_condition_value"].count("_") > 0:
			sub_items = iter_item[1]["sub_condition_value"].split("_")
			this_row[iter_item[1]["sub_condition"]] = [int(sub_items[1]), int(sub_items[2])]
		else:
			this_row[iter_item[1]["sub_condition"]] = [iter_item[1]["sub_condition_value"]]

	positive_list.append(this_row)

# Load the data into pandas dataframe
source_data = pd.read_csv(filename)

list_of_sign = []
new_column_1 = []
new_column_2 = []
new_column_3 = []
new_column_4 = []
new_column_5a = []
new_column_5b = []
new_column_6 = []

source_data.fillna("NA")

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
				satisfied_indexes.append(condition["index"])

		# if iter_item[0] in list_of_sign:
		# 	break

	years_05 = False
	years_10 = False

	if iter_item[1]["OS_time_months"] >= 60:
		new_column_5a.append(1)
		years_05 = True
		if iter_item[1]["OS_time_months"] >= 120:
			new_column_5b.append(1)
			years_10 = True
		else:
			new_column_5b.append(0)
	else:
		new_column_5a.append(0)
		new_column_5b.append(0)

	this_class = []

	if iter_item[1]["hormone_therapy"] == float('0'):
		this_class.append("NOT_hormon")
	if iter_item[1]["hormone_therapy"] == float('1'):
		this_class.append("hormon")
	if iter_item[1]["adjuvant_chemotherapy"] == float('0'):
		this_class.append("NOT_chemo")
	if iter_item[1]["adjuvant_chemotherapy"] == float('1'):
		this_class.append("chemo")

	if years_10:
		this_class.append("with_05_years_OS")
	elif years_05:
		this_class.append("with_10_years_OS")


	if iter_item[0] in list_of_sign:
		new_column_1.append(1)
		new_column_2.append(satisfied_indexes)
		new_column_3.append(chemo)
		new_column_4.append(hormon)
		if iter_item[1]["PFS_event"] == 0:
			this_class.insert(0, "significantly_effective_not_progressing")
		else:
			this_class.insert(0, "significantly_effective_progressing")

		new_column_6.append(", ".join(this_class))

	else:
		new_column_1.append(0)
		new_column_2.append(0)
		new_column_3.append(0)
		new_column_4.append(0)
		if len(this_class) > 0:
			new_column_6.append(", ".join(this_class))
		else:
			new_column_6.append("NOT_Classified")

# Print the number of significant patients
print(f"Classifier have found {len(list_of_sign)} ({'{:.2%}'.format((len(list_of_sign)/len(source_data)))}) significantly effectively treated patients out of {len(source_data)}.")

# Adding significance indicating columns to the export file
source_data["significance"] = new_column_1
source_data["significance_reason"] = new_column_2
source_data["significance_adjuvant_chemotherapy"] = new_column_3
source_data["significance_hormone_therapy"] = new_column_4
source_data["os_survival_05"] = new_column_5a
source_data["os_survival_10"] = new_column_5b
source_data["classification"] = new_column_6

classic = source_data.groupby(["classification"] ).size()
print(classic)

source_data_ch1_ho0 = source_data[(source_data["significance_adjuvant_chemotherapy"] == 1) & (source_data["significance_hormone_therapy"] == 0)]
source_data_ch0_ho1 = source_data[(source_data["significance_adjuvant_chemotherapy"] == 0) & (source_data["significance_hormone_therapy"] == 1)]
source_data_ch1_ho1 = source_data[(source_data["significance_adjuvant_chemotherapy"] == 1) & (source_data["significance_hormone_therapy"] == 1)]

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

# Print end time to the console
TimeNow("end", "classifier.py", start_time)
