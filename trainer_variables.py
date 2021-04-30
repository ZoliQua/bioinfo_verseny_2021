#
# Semmelweis Bioinformatika verseny pályázat 2021
#
# Készítette: Dr. Dul Zoltán, PhD
# 				a Semmelweis EMK MSc képzésének másodéves hallgatója
#

# PLEASE SET HERE THE VARIABLES TO RUN THE SCRIPT WITH CUSTOM DATA

# Name of the folder where source data is located
my_data_folder = "data"
# Name of the file to be analyzed
my_data_filename = "train.csv"
# Name of the file for statistics (saved into the my_data_folder folder)
statistics_filename = "train_statistics.csv"
# Name of files for analyzed export (saved into the my_data_folder folder)
# Export file - for all rows os the data incl. analysis
export_filename = "train_export.csv"
# Export file - for filtered rows, where only hormontherpy was significantly better
export_filename_ch0_ho1 = "train_export_chemo_0_hormon_1.csv"
# Export file - for filtered rows, where only adj. chemotherapy was significantly better
export_filename_ch1_ho0 = "train_export_chemo_1_hormon_0.csv"
# Export file - for filtered rows, where both therapies were significantly better
export_filename_ch1_ho1 = "train_export_chemo_1_hormon_1.csv"
