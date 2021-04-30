#
# Semmelweis Bioinformatika verseny pályázat 2021
#
# Készítette: Dr. Dul Zoltán, PhD
# 				a Semmelweis EMK MSc képzésének másodéves hallgatója
#

from trainer_functions import *
from trainer_variables import *

###########################
####### GENERAL DEF #######
###########################

# To Print General statistics
isPrintGeneralStat = True
# To Print PFS statistics
isPrintPFSStat = False
# To Print Any ChiSq test
isPrintChiSq = False

# Load the train data into pandas dataframe
filename = my_data_folder + "/" + my_data_filename
mydata = pd.read_csv(filename)
if isPrintGeneralStat:
	print(f"{filename} was successfully read into the script.")
	print(f"Stat / {filename} contains {len(mydata)} rows.")

# Filter the dataframe, and drop rows with NA in 'adjuvant_chemotherapy' and 'hormone_therapy' columns
df = mydata.dropna(subset=['adjuvant_chemotherapy', 'hormone_therapy'])

# Slice the dataframe into four subsets, based on the usage of chemotherapy and hormone therapy
filtered_ch0_ho0 = df.loc[(df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 0)]
filtered_ch0_ho1 = df.loc[(df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 1)]
filtered_ch1_ho0 = df.loc[(df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 0)]
filtered_ch1_ho1 = df.loc[(df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 1)]
filtered_ch0 = df.loc[(df['adjuvant_chemotherapy'] == 0)]
filtered_ch1 = df.loc[(df['adjuvant_chemotherapy'] == 1)]
filtered_ho0 = df.loc[(df['hormone_therapy'] == 0)]
filtered_ho1 = df.loc[(df['hormone_therapy'] == 1)]

# Number of rows for these therapies
rows_ch0_ho0 = len(filtered_ch0_ho0.index)
rows_ch0_ho1 = len(filtered_ch0_ho1.index)
rows_ch1_ho0 = len(filtered_ch1_ho0.index)
rows_ch1_ho1 = len(filtered_ch1_ho1.index)

# Print general information about row numbers created by the previous slicing
if isPrintGeneralStat:
	print("Stat / row numbers, without chemo or hormontherapy:", rows_ch0_ho0)
	print("Stat / row numbers, with hormontherapy only:", rows_ch0_ho1)
	print("Stat / row numbers, with adj. chemotherapy only:", rows_ch1_ho0)
	print("Stat / row numbers, with both therapy:", rows_ch1_ho1)
	print("")

filtered_dict = {	"chemo_0_hormo_0": filtered_ch0_ho0,
					"chemo_0_hormo_1": filtered_ch0_ho1,
					"chemo_1_hormo_0": filtered_ch1_ho0,
					"chemo_1_hormo_1": filtered_ch1_ho1,
					"chemo_0": filtered_ch0,
					"chemo_1": filtered_ch1,
					"hormon_0": filtered_ho0,
					"hormon_1": filtered_ho1 }

#
# Testing General PFS - Chemotherapy / Hormontherapy relation and significance
#

# The patient's status not changed
rows_pfs0 = []
# The patient's status further progressed
rows_pfs1 = []

for this_df in filtered_dict.items():
	filtered_pfs0 = this_df[1].loc[this_df[1]['PFS_event'] == 0]
	filtered_pfs1 = this_df[1].loc[this_df[1]['PFS_event'] == 1]
	if isPrintPFSStat:
		print(f"{this_df[0]} =>\t\tPFS_0:\t{len(filtered_pfs0.index)}\t\tPFS_1:\t{len(filtered_pfs1.index)}\t\t"
		      f"SUM:\t{len(this_df[1].index)}\t\tAverage PFS time (mean): {'{:.4f}'.format(filtered_pfs0['PFS_time_months'].mean())} ")
	rows_pfs0.append(len(filtered_pfs0.index))
	rows_pfs1.append(len(filtered_pfs1.index))

# ChiSq test for Chemotherapy
kemo = [[rows_pfs0[0] + rows_pfs0[1], rows_pfs1[0] + rows_pfs1[1]], [rows_pfs0[2] + rows_pfs0[3], rows_pfs1[2] + rows_pfs1[3]]]
if isPrintChiSq:
	PrintChiSq(kemo, "Adj. Chemotherapy", "pfs", "kemo")

# ChiSq test for Adj. Hormontherapy
hormon = [[rows_pfs0[0] + rows_pfs0[2], rows_pfs1[0] + rows_pfs1[2]], [rows_pfs0[1] + rows_pfs0[3], rows_pfs1[1] + rows_pfs1[3]]]
if isPrintChiSq:
	PrintChiSq(hormon, "Hormontherapy", "pfs", "horm")

# Check file status

if os.path.exists(my_data_folder + '/' + statistics_filename):
  os.remove(my_data_folder + '/' + statistics_filename)

#
# Testing Grading and PFS Chemotherapy / Hormontherapy relation and significance
#

sub_cond_null = {"col_name": "", "cond_value": ""}
grader = {"grade": [1, 2, 3]}
GeneralSlicer(filtered_dict, grader, sub_cond_null)

#
# Testing Staging and PFS Chemotherapy / Hormontherapy relation and significance
#

# Simple
stager = {"pathologic_stage": ["I", "IA", "IB", "II", "IIA", "IIB", "III", "IIIA", "IIIB", "IIIC", "IV"]}
GeneralSlicer(filtered_dict, stager, sub_cond_null)
# Combined into groups based on main identifier
stager = {"pathologic_stage": [["I", "IA", "IB"], ["II", "IIA", "IIB"], ["III", "IIIA", "IIIB", "IIIC"], "IV"]}
GeneralSlicer(filtered_dict, stager, sub_cond_null)

#
# A slicing and analysis based on the tumor size
#

# Set of tumor size range
size_range = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 200)]

for this_range in size_range:

	name = "simple"
	sub_cond = {"col_name": "size_documented",
				"cond_value": "between_" + str(this_range[0]).zfill(3) + "_" + str(this_range[1]).zfill(3)}
	filtered_dict_by_age = {}

	for this_df in filtered_dict.items():
		filtered_dict_by_age[this_df[0]] = this_df[1][ (this_df[1]["size_documented"] >= this_range[0]) & (this_df[1]["size_documented"] <= this_range[1]) ]

	GeneralSlicer(filtered_dict_by_age, grader, sub_cond, name, "a")

#
# Age slicing
#
# age_range = from 1 to 50, from 51 to 65, from 66 to 100
#

# Set of age range
age_range = [(1, 50), (51, 65), (66, 100)]

for this_range in age_range:

	name = "simple"
	sub_cond = {"col_name": "age_at_diagnosis",
				"cond_value": "between_" + str(this_range[0]).zfill(3) + "_" + str(this_range[1]).zfill(3)}

	filtered_dict_by_age = {}

	for this_df in filtered_dict.items():
		filtered_dict_by_age[this_df[0]] = this_df[1][ (this_df[1]["age_at_diagnosis"] >= this_range[0]) & (this_df[1]["age_at_diagnosis"] <= this_range[1]) ]

	GeneralSlicer(filtered_dict_by_age, grader, sub_cond, name, "a")

print(f"Trainer have successfully exported statistics into {my_data_folder + '/' + statistics_filename}.")
