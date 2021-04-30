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
TimeNow("start", "trainer.py")

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
	print("")
	print(f"{filename} was successfully read into the script.")
	print(f"Stat / {filename} contains {len(mydata)} rows.")

# Filter the dataframe, and drop rows with NA in 'adjuvant_chemotherapy' and 'hormone_therapy' columns
df = mydata.dropna(subset=['adjuvant_chemotherapy', 'hormone_therapy'])
if isPrintGeneralStat:
	print(f"Stat / {filename} contains {len(df)} NA free rows related to chemo and hormon therapies.")
	print(f"Stat / Dropped {len(mydata) - len(df)} ({ '{:.2%}'.format((len(mydata) - len(df)) / len(mydata)) }) rows, because NA in adjuvant_chemotherapy or hormone_therapy columns.")

# Slice the dataframe into four subsets, based on the usage of chemotherapy and hormone therapy
filtered_rax_ch0_ho0 = df.loc[(df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 0)]
filtered_ra0_ch0_ho0 = df.loc[(df['radiation_therapy'] == 0) & (df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 0)]
filtered_ra1_ch0_ho0 = df.loc[(df['radiation_therapy'] == 1) & (df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 0)]
filtered_rax_ch0_ho1 = df.loc[(df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 1)]
filtered_ra0_ch0_ho1 = df.loc[(df['radiation_therapy'] == 0) & (df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 1)]
filtered_ra1_ch0_ho1 = df.loc[(df['radiation_therapy'] == 1) & (df['adjuvant_chemotherapy'] == 0) & (df['hormone_therapy'] == 1)]
filtered_rax_ch1_ho0 = df.loc[(df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 0)]
filtered_ra0_ch1_ho0 = df.loc[(df['radiation_therapy'] == 0) & (df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 0)]
filtered_ra1_ch1_ho0 = df.loc[(df['radiation_therapy'] == 1) & (df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 0)]
filtered_rax_ch1_ho1 = df.loc[(df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 1)]
filtered_ra0_ch1_ho1 = df.loc[(df['radiation_therapy'] == 0) & (df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 1)]
filtered_ra1_ch1_ho1 = df.loc[(df['radiation_therapy'] == 1) & (df['adjuvant_chemotherapy'] == 1) & (df['hormone_therapy'] == 1)]
filtered_rax_ch0_hox = df.loc[(df['adjuvant_chemotherapy'] == 0)]
filtered_ra0_ch0_hox = df.loc[(df['radiation_therapy'] == 0) & (df['adjuvant_chemotherapy'] == 0)]
filtered_ra1_ch0_hox = df.loc[(df['radiation_therapy'] == 1) & (df['adjuvant_chemotherapy'] == 0)]
filtered_rax_ch1_hox = df.loc[(df['adjuvant_chemotherapy'] == 1)]
filtered_ra0_ch1_hox = df.loc[(df['radiation_therapy'] == 0) & (df['adjuvant_chemotherapy'] == 1)]
filtered_ra1_ch1_hox = df.loc[(df['radiation_therapy'] == 1) & (df['adjuvant_chemotherapy'] == 1)]
filtered_rax_chx_ho0 = df.loc[(df['hormone_therapy'] == 0)]
filtered_ra0_chx_ho0 = df.loc[(df['radiation_therapy'] == 0) & (df['hormone_therapy'] == 0)]
filtered_ra1_chx_ho0 = df.loc[(df['radiation_therapy'] == 1) & (df['hormone_therapy'] == 0)]
filtered_rax_chx_ho1 = df.loc[(df['hormone_therapy'] == 1)]
filtered_ra0_chx_ho1 = df.loc[(df['radiation_therapy'] == 0) & (df['hormone_therapy'] == 1)]
filtered_ra1_chx_ho1 = df.loc[(df['radiation_therapy'] == 1) & (df['hormone_therapy'] == 1)]

# Number of rows for these therapies
rows_rax_ch0_ho0 = len(filtered_rax_ch0_ho0.index)
rows_rax_chx_ho0 = len(filtered_rax_chx_ho0.index)
rows_rax_ch0_hox = len(filtered_rax_ch0_hox.index)
rows_ra0_ch0_ho0 = len(filtered_ra0_ch0_ho0.index)
rows_ra0_chx_ho0 = len(filtered_ra0_chx_ho0.index)
rows_ra0_ch0_hox = len(filtered_ra0_ch0_hox.index)
rows_ra1_ch0_ho0 = len(filtered_ra1_ch0_ho0.index)
rows_ra1_chx_ho0 = len(filtered_ra1_chx_ho0.index)
rows_ra1_ch0_hox = len(filtered_ra1_ch0_hox.index)

rows_rax_ch0_ho1 = len(filtered_rax_ch0_ho1.index)
rows_rax_chx_ho1 = len(filtered_rax_chx_ho1.index)
rows_ra0_ch0_ho1 = len(filtered_ra0_ch0_ho1.index)
rows_ra0_chx_ho1 = len(filtered_ra0_chx_ho1.index)
rows_ra1_ch0_ho1 = len(filtered_ra1_ch0_ho1.index)
rows_ra1_chx_ho1 = len(filtered_ra1_chx_ho1.index)

rows_rax_ch1_ho0 = len(filtered_rax_ch1_ho0.index)
rows_rax_ch1_hox = len(filtered_rax_ch1_hox.index)
rows_ra0_ch1_ho0 = len(filtered_ra0_ch1_ho0.index)
rows_ra0_ch1_hox = len(filtered_ra0_ch1_hox.index)
rows_ra1_ch1_ho0 = len(filtered_ra1_ch1_ho0.index)
rows_ra1_ch1_hox = len(filtered_ra1_ch1_hox.index)

rows_rax_ch1_ho1 = len(filtered_rax_ch1_ho1.index)
rows_ra0_ch1_ho1 = len(filtered_ra0_ch1_ho1.index)
rows_ra1_ch1_ho1 = len(filtered_ra1_ch1_ho1.index)

# Print general information about row numbers created by the previous slicing
if isPrintGeneralStat:
	print("")
	print("General statistics of rows.")
	print("=" * 140)
	print("radiation_therapy value".ljust(65),
		"NOT measured".ljust(20),
		"  measured and 0".ljust(20),
		"  measured and 1")
	print("=" * 140)
	print("".ljust(65),
		"Rows".ljust(10), "Rows/All".ljust(10),
		"Rows".ljust(10), "Rows/All".ljust(10),
		"Rows".ljust(10), "Rows/All".ljust(10))
	print("=" * 140)
	print("Stat / Cases, without chemotherapy:".ljust(65),
		str(rows_rax_ch0_hox).ljust(10), '{:.2%}'.format(rows_rax_ch0_hox/len(df)).ljust(10),
		str(rows_ra0_ch0_hox).ljust(10), '{:.2%}'.format(rows_ra0_ch0_hox/len(df)).ljust(10),
		str(rows_ra1_ch0_hox).ljust(10), '{:.2%}'.format(rows_ra1_ch0_hox/len(df)).ljust(10))
	print("Stat / Cases, without hormontherapy:".ljust(65),
		str(rows_rax_chx_ho0).ljust(10), '{:.2%}'.format(rows_rax_chx_ho0/len(df)).ljust(10),
		str(rows_ra0_chx_ho0).ljust(10), '{:.2%}'.format(rows_ra0_chx_ho0/len(df)).ljust(10),
		str(rows_ra1_chx_ho0).ljust(10), '{:.2%}'.format(rows_ra1_chx_ho0/len(df)).ljust(10))
	print("Stat / Cases, without chemotherapy or hormontherapy:".ljust(65),
		str(rows_rax_ch0_ho0).ljust(10), '{:.2%}'.format(rows_rax_ch0_ho0/len(df)).ljust(10),
		str(rows_ra0_ch0_ho0).ljust(10), '{:.2%}'.format(rows_ra0_ch0_ho0/len(df)).ljust(10),
		str(rows_ra1_ch0_ho0).ljust(10), '{:.2%}'.format(rows_ra1_ch0_ho0/len(df)).ljust(10))
	print("Stat / Cases, with hormontherapy:".ljust(65),
		str(rows_rax_chx_ho1).ljust(10), '{:.2%}'.format(rows_rax_chx_ho1/len(df)).ljust(10),
		str(rows_ra0_chx_ho1).ljust(10), '{:.2%}'.format(rows_ra0_chx_ho1/len(df)).ljust(10),
		str(rows_ra1_chx_ho1).ljust(10), '{:.2%}'.format(rows_ra1_chx_ho1/len(df)).ljust(10))
	print("Stat / Cases, with hormontherapy only (and NOT adj. chemoth.):".ljust(65),
		str(rows_rax_ch0_ho1).ljust(10), '{:.2%}'.format(rows_rax_ch0_ho1/len(df)).ljust(10),
		str(rows_ra0_ch0_ho1).ljust(10), '{:.2%}'.format(rows_ra0_ch0_ho1/len(df)).ljust(10),
		str(rows_ra1_ch0_ho1).ljust(10), '{:.2%}'.format(rows_ra1_ch0_ho1/len(df)).ljust(10))
	print("Stat / Cases, with adj. chemotherapy:".ljust(65),
		str(rows_rax_ch1_hox).ljust(10), '{:.2%}'.format(rows_rax_ch1_hox/len(df)).ljust(10),
		str(rows_ra0_ch1_hox).ljust(10), '{:.2%}'.format(rows_ra0_ch1_hox/len(df)).ljust(10),
		str(rows_ra1_ch1_hox).ljust(10), '{:.2%}'.format(rows_ra1_ch1_hox/len(df)).ljust(10))
	print("Stat / Cases, with adj. chemotherapy only (and NOT hormonth.):".ljust(65),
		str(rows_rax_ch1_ho0).ljust(10), '{:.2%}'.format(rows_rax_ch1_ho0/len(df)).ljust(10),
		str(rows_ra0_ch1_ho0).ljust(10), '{:.2%}'.format(rows_ra0_ch1_ho0/len(df)).ljust(10),
		str(rows_ra1_ch1_ho0).ljust(10), '{:.2%}'.format(rows_ra1_ch1_ho0/len(df)).ljust(10))
	print("Stat / Cases, with both therapies:".ljust(65),
		str(rows_rax_ch1_ho1).ljust(10), '{:.2%}'.format(rows_rax_ch1_ho1/len(df)).ljust(10),
		str(rows_ra0_ch1_ho1).ljust(10), '{:.2%}'.format(rows_ra0_ch1_ho1/len(df)).ljust(10),
		str(rows_ra1_ch1_ho1).ljust(10), '{:.2%}'.format(rows_ra1_ch1_ho1/len(df)).ljust(10))
	print("=" * 140)
	print("")

filtered_dict_radio = {	"radio_x": {
						"chemo_0_hormo_0": filtered_rax_ch0_ho0,
						"chemo_0_hormo_1": filtered_rax_ch0_ho1,
						"chemo_1_hormo_0": filtered_rax_ch1_ho0,
						"chemo_1_hormo_1": filtered_rax_ch1_ho1,
						"chemo_0": filtered_rax_ch0_hox,
						"chemo_1": filtered_rax_ch1_hox,
						"hormon_0": filtered_rax_chx_ho0,
						"hormon_1": filtered_rax_chx_ho1 },
					"radio_0": {
						"chemo_0_hormo_0": filtered_ra0_ch0_ho0,
						"chemo_0_hormo_1": filtered_ra0_ch0_ho1,
						"chemo_1_hormo_0": filtered_ra0_ch1_ho0,
						"chemo_1_hormo_1": filtered_ra0_ch1_ho1,
						"chemo_0": filtered_ra0_ch0_hox,
						"chemo_1": filtered_ra0_ch1_hox,
						"hormon_0": filtered_ra0_chx_ho0,
						"hormon_1": filtered_ra0_chx_ho1 },
					"radio_1": {
						"chemo_0_hormo_0": filtered_ra1_ch0_ho0,
						"chemo_0_hormo_1": filtered_ra1_ch0_ho1,
						"chemo_1_hormo_0": filtered_ra1_ch1_ho0,
						"chemo_1_hormo_1": filtered_ra1_ch1_ho1,
						"chemo_0": filtered_ra1_ch0_hox,
						"chemo_1": filtered_ra1_ch1_hox,
						"hormon_0": filtered_ra1_chx_ho0,
						"hormon_1": filtered_ra1_chx_ho1 }
					}

#
# Testing General PFS - Chemotherapy / Hormontherapy relation and significance
#

# The patient's status not changed
rows_pfs0 = []
# The patient's status further progressed
rows_pfs1 = []

for filtered_dict in filtered_dict_radio.items():
	for this_df in filtered_dict[1].items():
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
grader_merged = {"grade": [["1", "2", "3"]]}
GeneralSlicer(filtered_dict_radio, grader, sub_cond_null)

#
# Testing Staging and PFS Chemotherapy / Hormontherapy relation and significance
#

# Simple
stager = {"pathologic_stage": ["I", "IA", "IB", "II", "IIA", "IIB", "III", "IIIA", "IIIB", "IIIC", "IV"]}
GeneralSlicer(filtered_dict_radio, stager, sub_cond_null)
# Combined into groups based on main identifier
stager_combined = {"pathologic_stage": [["I", "IA", "IB"], ["II", "IIA", "IIB"], ["III", "IIIA", "IIIB", "IIIC"], "IV"]}
GeneralSlicer(filtered_dict_radio, stager_combined, sub_cond_null)
# pathologic_T
pathologic_T = {"pathologic_T": ["T1", "T1b", "T1c", "T2", "T3", "T3a", "T4", "T4b", "T4d", "TX"]}
GeneralSlicer(filtered_dict_radio, pathologic_T, sub_cond_null)
# pathologic_N
pathologic_N = {"pathologic_N": ["N0", "N0 (i-)", "N0 (i+)", "N1", "N1a", "N1b", "N1mi", "N2", "N2a", "N3", "N3a", "N3b", "NX"]}
GeneralSlicer(filtered_dict_radio, pathologic_N, sub_cond_null)
# pathologic_M
pathologic_M = {"pathologic_M": ["M0", "M1"]}
GeneralSlicer(filtered_dict_radio, pathologic_M, sub_cond_null)

#
# A slicing and analysis based on the tumor size
#

# Set of tumor size range
size_range = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 200),
			  (1, 10), (11, 20), (21, 30), (31, 40), (41, 50),
			  (51, 60), (61, 70), (71, 80), (81, 90), (91, 100),
			  (101, 120), (121, 200)]

for this_range in size_range:

	name = "simple"
	sub_cond = {"col_name": "size_documented",
				"cond_value": "between_" + str(this_range[0]).zfill(3) + "_" + str(this_range[1]).zfill(3)}

	filtered_dict_by_size = {}

	for filtered_dict in filtered_dict_radio.items():
		filtered_dict_by_size[filtered_dict[0]] = {}
		for this_df in filtered_dict[1].items():
			filtered_dict_by_size[filtered_dict[0]][this_df[0]] = this_df[1][ (this_df[1]["size_documented"] >= this_range[0]) & (this_df[1]["size_documented"] <= this_range[1]) ]

	# Test tumor size (merged file is producing the whole table)
	GeneralSlicer(filtered_dict_by_size, grader_merged, sub_cond, name, "a")
	# Test tumor size line with grade level
	GeneralSlicer(filtered_dict_by_size, grader, sub_cond, name, "a")
	# Test tumor size line with combined stage level
	GeneralSlicer(filtered_dict_by_size, stager_combined, sub_cond, name, "a")

#
# Age slicing
#
# age_range = from 1 to 50, from 51 to 65, from 66 to 100
#

# Set of age range
age_range = [(1, 50), (51, 65), (66, 100),
			 (1, 35), (36, 50), (51, 70), (71, 85), (86, 100)]

for this_range in age_range:

	name = "simple"
	sub_cond = {"col_name": "age_at_diagnosis",
				"cond_value": "between_" + str(this_range[0]).zfill(3) + "_" + str(this_range[1]).zfill(3)}

	filtered_dict_by_age = {}

	for filtered_dict in filtered_dict_radio.items():
		filtered_dict_by_age[filtered_dict[0]] = {}
		for this_df in filtered_dict[1].items():
			filtered_dict_by_age[filtered_dict[0]][this_df[0]] = this_df[1][ (this_df[1]["age_at_diagnosis"] >= this_range[0]) & (this_df[1]["age_at_diagnosis"] <= this_range[1]) ]

	# Test age_at_diagnosis (merged file is producing the whole table)
	GeneralSlicer(filtered_dict_by_age, grader_merged, sub_cond, name, "a")
	# Test age_at_diagnosis line with grade level
	GeneralSlicer(filtered_dict_by_age, grader, sub_cond, name, "a")
	# Test age_at_diagnosis line with combined stage level
	GeneralSlicer(filtered_dict_by_age, stager_combined, sub_cond, name, "a")

#
# Testing Grading and PFS Chemotherapy / Hormontherapy relation and significance
#

list_of_conditon_arrays = [grader, stager_combined]

# Testing for menopausa status
menopausa_status = {"menopause_status_documented": ["PRE", "POST", "PERI", "MALE"]}
GeneralSlicer(filtered_dict_radio, menopausa_status, sub_cond_null)
SliceBySimpleConditon(filtered_dict_radio, menopausa_status, list_of_conditon_arrays)

# Testing for surgical_procedure
surgical_procedure = {"surgical_procedure": ["MASTECTOMY", "BREAST CONSERVING"]}
GeneralSlicer(filtered_dict_radio, surgical_procedure, sub_cond_null)
SliceBySimpleConditon(filtered_dict_radio, surgical_procedure, list_of_conditon_arrays)

print(f"Trainer have successfully exported statistics into {my_data_folder + '/' + statistics_filename}.")

# Print end time to the console
TimeNow("end", "trainer.py", start_time)

