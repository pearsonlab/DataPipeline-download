from __future__ import print_function
import numpy as np
import glob
import json
import argparse
import writeToFile

# initializing list for each relevant header information
channel_files = []
channel_name_list = []
phyDimension_list = []
phyMinimum_list = []
phyMaximum_list = []
digMinimum_list = []
digMaximum_list = []
sampsPerRecord_list = []

def main(chunk_folder, edf_file):

	# read all the files in the folder
	files = sorted(glob.glob(chunk_folder+"*.chn"))
	num_channels = int(len(files)/2) # number of channels to be included in the edf file

	# pass the files to process (retreive header and data) assuming that only 2 chunk files for each signals are used to create a new edf file
	for i in range(0,len(files),2):
		process_files(files[i], files[i+1], num_channels, edf_file)

# read the information from the files
def process_files(filepath1, filepath2, num_channels, edf_file):
	filelist = [filepath1, filepath2]

	# check to see if both chunk files for same signal are in the same filelist
	print(filelist)
	
	with open(filepath2, 'rb') as open_data:
		data = open_data.read()
		y = str(data, 'utf-8', 'ignore')
		readline = y.splitlines()[0]
		text = json.loads(readline)
		sigName = text["sigLabel"]
		phyDim = text["phyDimension"]
		phyMax = text["phyMaximum"]
		phyMin = text["phyMinimum"]
		digMax = text["digMaximum"]
		digMin = text["digMinimum"]
		numSamps = text["sampsPerRecord"]
		recsRemaining = int(text["recsRemaining"])
		recsPerChunk = int(text["recsPerChunk"])
		recDur = float(text["recDur"])
		chunkDuration = float(text["chunkDuration"])

	# add header information to lists
	channel_name_list.append(sigName)
	phyDimension_list.append(phyDim)
	phyMaximum_list.append(phyMax)
	phyMinimum_list.append(phyMin)
	digMaximum_list.append(digMax)
	digMinimum_list.append(digMin)
	sampsPerRecord_list.append(numSamps)

	# number of data records
	if(recsRemaining >= recsPerChunk):
		numRecs = int((chunkDuration/recDur)*2)
	else:
		numRecs = recsRemaining+recsPerChunk
	
	# header information related to data record
	recInfoList = [numRecs, recDur]

	# include all the lists for header information in one big list
	header_output = [channel_name_list, phyDimension_list, phyMinimum_list, phyMaximum_list, digMinimum_list, digMaximum_list, sampsPerRecord_list]

	# reading the data (content) of each file pair
	file_data = read_data(filelist)
	channel_files.append(combining_chunks(file_data))

	# pass the file information and data if and only if all the files are read
	if(len(channel_files) == num_channels):
		arrange_data(num_channels, channel_files, header_output, recInfoList, edf_file)


# read the main data (content) for each chunk files
def read_data(filepath_list):
	data_array_list = []
	for i in range(len(filepath_list)):

		with open(filepath_list[i], 'rb') as open_data:
			open_data.readline()
			data_array= np.fromfile((open_data), dtype='<i2').astype('int16')# astype('int64')

		data_array_list.insert(i, np.reshape(data_array,(1,len(data_array))))

	return(data_array_list)

# combining data array for two chunk files
def combining_chunks(data_array_list):
	concate = np.concatenate(data_array_list, axis=1)
	return(concate)

# arrange main content data (numpy array)
def arrange_data(num_channels, data_num_list, header, recHeader, edf_file):

	# updating the data array list as a stack of array to write as edf
	updated_list = []
	for i in range(len(data_num_list)):
		updated_list.insert(i, np.array(data_num_list[i]))

	data_num = tuple(updated_list)
	final_array = np.vstack(data_num)

	print("converting to edf - passing number of channels, data array and header information to writeFile")
	writeToFile.write(num_channels, final_array, header, recHeader, edf_file)

# main
if __name__ == '__main__':
	# setting up parse options
    parser = argparse.ArgumentParser(description='Combine 2 chunk files for each signals to form a edf file. ' +
                                                  'Must specify location for folder with chunk files and the final edf file name and destination',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('chunkFolderLocation', help='Location of folder with chunk files to convert, eg:(directory)')
    parser.add_argument('edfFileLocation', help='File name and location for final edf file , eg:(directory/filename.edf)')
    args = parser.parse_args()

    chunk_folder = args.chunkFolderLocation
    edf_file = args.edfFileLocation

    # checking if all the arguments are given
    if not chunk_folder and not edf_file:
    	sys.exit('Must provide input folder location for chunk files and an output file location.')
    elif not chunk_folder:
    	sys.exit('Must provide input chunk folder location.')
    elif not edf_file:
    	sys.exit('Must provide output edf file location.')
    else:
        main(chunk_folder, edf_file)
