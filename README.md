# DataPipeline-download
downloading files from AWS DataPipeline system

System requirements:
  - Python3
  - Flask (pip install flask)

Instructions to download data files
- Run run.py (this restarts the ec2 instance and restores the rds db snapshot)
    - Enter the date for which you want to restore the db snapshot
    - Follow the instructions on the terminal and wait until the system setup is complete
    - Make sure that the db snapshot is restored before moving to next step
- Go to web folder - cd web
    - Run hello.py
    - Open [localhost:5000](localhost:5000) on your local browser and follow on the instructions on the webpage
    - Note: edf data files will be downloaded in s3_download folder of current directory, while behavioral data will be downloaded in s3_download/behavioral_data
    - After the downloads are completed, get back to the main directory and run stop.py (this stops the ec2 instance as well as deletes the db instance and saves a db snapshot)

Instructions to combine chunk files to a edf file
- All the downloaded edf data files are have .chn extension
- Each chunk consists data of maximum 60 minutes and most of the times we have to combine 2 chunk files to get information regarding particular task.
- To combine those files, run edfwriter.py passing in the directory of the folder where edf data files are stored as well as the destination along with name of the final edf file you want to write as
