from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname
import glob
import os
import json
import csv

speech_to_text = SpeechToTextV1(
    iam_apikey='buikFmICUIRaiH8JqefBElbVxveOIHMZ-oRcAL_YVP03',
    url='https://gateway-wdc.watsonplatform.net/speech-to-text/api'
)

files = ['arctic_a0026.wav']
json_name = ['test.json']
'''
for file in files:
    with open(join(dirname(__file__), './.', file), 'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            timestamps=True,
            #keywords=['morning', 'hello', 'good','americans','america'],
            #keywords_threshold=0.5
        ).get_result()
    print(json.dumps(speech_recognition_results, indent=2))
wordsfile = open("words.csv", "w")
csvfile = csv.writer(wordsfile)
csvfile.writerow(['word', 'confidence', 'start', 'end'])
'''
## Transcribe each WAV to Watson
#for fname in glob("*.wav"):
for fname in files:
    # Download watson's response
    tname = json_name[0]

    print("Transcribing", fname)
    with open(fname, 'rb') as r:
        speech_recognition_results = speech_to_text.recognize(
            audio=r,
            content_type='audio/wav',
            timestamps=True,
            keywords=['morning', 'hello', 'good','americans','america'],
            keywords_threshold=0.7
        ).get_result()
        with open(tname, 'w') as w:
            w.write(json.dumps(speech_recognition_results, indent=2))
            print("Wrote transcript to", tname)


# Print out the raw transcript and word csv
rawfile = open("raw.txt", "w")
wordsfile = open("words.csv", "w")
csvfile = csv.writer(wordsfile)
csvfile.writerow(['word', 'confidence', 'start', 'end'])

for fname in json_name:
    with open(fname, 'r') as f:
        results = json.load(f)['results']
        for linenum, result in enumerate(results): # each result is a  line
            if result.get('alternatives'): # each result may have many alternatives
                # just pick best alternative
                lineobj = result.get('alternatives')[0]
                # rawfile.writeline(lineobj['transcript'])
                word_timestamps = lineobj['timestamps']
                if word_timestamps:
                    rawfile.write(lineobj['transcript'] + "\n")
                    word_confidences = lineobj['confidence']
                    for idx, wordts in enumerate(word_timestamps):
                        txt, tstart, tend = wordts
                        print(word_confidences)
                        confidence = round(100 * word_confidences)
                        csvfile.writerow([txt, confidence, tstart, tend])


rawfile.close()
wordsfile.close()

