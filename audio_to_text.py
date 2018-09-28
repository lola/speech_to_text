import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates clients
client = speech.SpeechClient()
storage_client = storage.Client()

#variables
source_bucket_name = '911-calls'
source_bucket = storage_client.bucket(source_bucket_name)
bucket_prefix = 'audio-recordings-wav'


#create a csv file
with open('data.csv', 'a') as csvfile:
    		csvfile.write('audio_gcs_uri, transcript' + '\n')


# for each audio file ....
for file in (list(source_bucket.list_blobs(prefix=bucket_prefix))):
	audio_gcs_uri = "gs://" + source_bucket_name + "/" + file.name

	audio = types.RecognitionAudio(uri=audio_gcs_uri)
	print(audio)

	config = types.RecognitionConfig(
		encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
		# use_enhanced=True, # for phone audio
		# model='phone_call', # model must be specified for enhanced model
		language_code='en-US')


	operation = client.long_running_recognize(config, audio)


	print('Waiting for operation to complete...')
	response = operation.result(timeout=3600)
    
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
	transcript = ''
	for result in response.results:

		transcript+=str(result.alternatives[0].transcript)

	print(transcript)
	with open('data.csv', 'a') as csvfile:
  		csvfile.write(audio_gcs_uri + ',' + transcript + '\n')

 






    	