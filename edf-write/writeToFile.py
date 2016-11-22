from __future__ import print_function
import numpy as np

def write(numSignals, dataArray, header, remainingHeaderInfo, edf_file):

    numSamples = header[-1][0] # number of samples in data record - assuming each data record has same number of samples

    # reshaping the data array in terms of each signal in data array
    reshaped_data = np.reshape(dataArray, ((len(dataArray[0])*numSignals)/numSamples, numSamples))
        
    # initializing variables
    headBytes = 256+(numSignals*256) # number of bytes in edf header --> first 256 bytes of header are independent of signals, whereas later each signal has 256 bytes of header information
    numRecs = remainingHeaderInfo[0]
    recDur = remainingHeaderInfo[1]
    
    print("number of bytes in header record: ", headBytes)
    print("number of data records: ", numRecs)
    print("duration of a data record, in seconds: ", recDur)

    # write to a new EDF file
    with open(edf_file, 'wb') as f:
        f.write((str('0').ljust(8)).encode()) # initial 8 spaces
        f.write((str('').ljust(160)).encode()) # local patient + recording identification -> (80+80)
        f.write((str('01.01.01').ljust(8)).encode()) # start date de-identified (8)
        f.write((str('12.12.12').ljust(8)).encode()) # start time de-identified (8) 
        f.write((str(headBytes).ljust(8)).encode('utf-8')) #number of bytes on header record
        f.write((str('').ljust(44)).encode()) #reserved spaces
        f.write((str(numRecs).ljust(8)).encode('utf-8')) #number of data records
        f.write((str(recDur).ljust(8)).encode('utf-8')) #duration of a data record
        f.write((str(numSignals).ljust(4)).encode('utf-8')) #number of signals in data record

        # label for each signal
        for i in range(len(header[0])):
            strr = str(header[0][i])
            f.write((strr.ljust(16)).encode())
        
        # transducer type left as blank space
        f.write((str('').ljust(numSignals*80)).encode())
        
        # function to add headers with common features
        def addMulitpleHeaders(headerElements):
            for i in range(len(headerElements)):
                strr = str(headerElements[i])
                f.write((strr.ljust(8)).encode())
        
        # loop to add headers with common features
        # (i.e. physical dimension, physical minimum, physical maximum, digital minimum, digital maximum)
        for j in range(1,6):
            addMulitpleHeaders(header[j])

        # prefiltering left as blank space
        f.write((str('').ljust(numSignals*80)).encode())

        # number of samples in each data record 
        addMulitpleHeaders(header[6])
        
        # reserved spaces
        f.write((str('').ljust(numSignals*32)).encode())

        # looping through the array of data record arrays
        for i in range(numRecs):
            for j in range(numSignals):
        
                f.write(reshaped_data[(j*numRecs)+i].tobytes())
            print("wrote data records: ", i+1)
        
        f.close()
        print("edf writing complete!")
