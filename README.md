# Railway_Announcement

1. pip install pyaudio 
   1.1  if you get an error then you search "unofficial python binaries" 
	then select your python version and install it
   1.2  open the powershell window using shift + rightclick, then run it.

2. pip install pydub
   2.1  download ffmpeg from official site, select windows builds select your os  
   2.2  extract the files
   2.3  then select all the files inside the folder
   2.4  copy the files and create the folder "ffmpeg" in C:\Program Files and paste the 
        files in that folder
                      "THIS IS ONE TIME PROCESS"
   2.5  rightclick on thisPC (Windows 10) or Computer then click on properties 
   2.4  on left side click on advanced system settings then select Environment Variable	
   2.6  then click on edit of user variable 
   2.7  click on new and the paste the location C:\Program Files\ffmpeg\bin ,click OK 

3. pip install gTTS (google text to speech)
4. pip install pyodbc	
   4.1  If You found an ERROR datasource not found 
        then run this code:
	" import pyodbc
	  print(pyodbc.dataSources()) "
