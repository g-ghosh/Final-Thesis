from pydub import AudioSegment

files_path = '/home/gaurab/Audio_Extract_Test/'
file_name = 'small_audio'

startMin = 0
startSec = 2.33

endMin = 0
endSec = 2.8

# Time to miliseconds
startTime = startMin*60*1000+startSec*1000
endTime = endMin*60*1000+endSec*1000

# Opening file and extracting segment
song = AudioSegment.from_wav( files_path+file_name+'.wav' )
extract = song[startTime:endTime]

# Saving
extract.export( file_name+'-extract.wav', format="wav")
