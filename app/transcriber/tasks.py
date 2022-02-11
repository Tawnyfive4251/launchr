from __future__ import absolute_import, unicode_literals
from uuid import uuid4

# import speech_recognition
from pydub import AudioSegment

from celery import shared_task
from django.utils import timezone

from transcriber import models
import wave 
# import deepspeech
import os
# import numpy as np
import speech_recognition as sr

@shared_task(bind=True)
def debug_task(self):
    print('Hello there!')
    print('Request: {0!r}'.format(self.request))
    return
@shared_task
def process_uploaded_file(audio_data_id):
    """
    Call all other processing methods from this method
    """

    # Get Audio data model
    audio_data = None
    audio_data = models.AudioDataModel.objects.get(id=audio_data_id)

    # Convert uploaded file into WAV format
    convert_into_wave(audio_data)

    # Extract the Transcript from WAV file
    return AI_transcription(audio_data)


def convert_into_wave(audio_data):
    """
    Converts the uploaded file into WAV, suitable for Speech Recognition
    """
    # uploaded_file_name = audio_data.uploaded_file.name
    # file_extension = uploaded_file_name.split('.')[-1].lower()
    # exported_file_name = audio = None

    # # Convert into WAV format
    # if file_extension != 'wav':
    #     audio = AudioSegment.from_file(uploaded_file_name, file_extension)
    #     # audio.set_channels(1)
    #     audio.set_frame_rate(16000)
    #     # Generate a unique name and then export as WAV
    #     exported_file_name = f'{str(uuid4())}.wav'
    #     audio.export(exported_file_name, format='wav')

    # # Already a WAV file
    # else:
    #     exported_file_name = uploaded_file_name

    # # Now save the exported file name
    # audio_data.exported_file_name = exported_file_name
    # audio_data.save()
    uploaded_file_name = audio_data.uploaded_file.name
    exported_file_name = None
    sound = AudioSegment.from_mp3(uploaded_file_name)
    sound.export("transcript.wav", format="wav")
    audio_data.exported_file_name = "transcript.wav"
def AI_transcription(wavefile):
    # return wavefile
    r = sr.Recognizer()
    try:
        with sr.AudioFile(wavefile.exported_file_name) as source:
            audio = r.record(source)
        value = r.recognize_sphinx(audio)
        print(value)
        wavefile.transcript = value
        wavefile.status = 'COM'
        wavefile.save()
        return value
    except sr.UnknownValueError:
        print("could not understand audio")
        print(e)
    except sr.RequestError as e:
        print("Speech Recognition could not understand the audio Error: {0}".format(e))



# Example from GitHub:
# def transcribe_audio(audio_data):
#     """
#     Extract transcript from WAV file
#     """

#     exported_file_name = audio_data.exported_file_name
#     audio = transcript = None

#     recognizer = speech_recognition.Recognizer()

#     with speech_recognition.AudioFile(exported_file_name) as ef:
#         audio = recognizer.record(ef)
#         transcript = recognizer.recognize_google(audio)

#     # Save the transcript in the database
#     audio_data.transcript = transcript
#     audio_data.status = 'COM'
#     audio_data.time_taken = timezone.now() - audio_data.created_at
#     print(timezone.now() - audio_data.created_at)
#     audio_data.save()

#     return

# def AI_transcription(wavefile):
#     if wavefile is None:
#         return 'File not accepted: NoneType passed.'
#     exported_file_name = wavefile.exported_file_name
#     audio = transcript = None
#     #Use DeepSpeech to transcribe the audio, which is a single channel wav file in 16khz
#     model_file_path = os.path.join('''models''', 'deepspeech-0.9.3-models.pbmm')
#     model = deepspeech.Model(model_file_path)    
#     # scorer_file_path = os.path.join('''models''', 'deepspeech-0.9.3-models.pbmm')
#     # scorer = deepspeech.enableExternalScorer(scorer_file_path)
#     lm_alpha = 0.75
#     lm_beta = 1.85
#     beam_width = 500
#     model.setScorerAlphaBeta(lm_alpha, lm_beta)
#     model.setBeamWidth(beam_width)
#     w = wave.open(exported_file_name, 'r')
#     # rate = w.getframerate()
#     buffer = w.readframes(w.getnframes())
#     d16 = np.frombuffer(buffer, dtype=np.int8)
#     transcript = model.stt(d16)
#     wavefile.transcript = transcript
#     wavefile.status = 'COM'
#     wavefile.time_taken = timezone.now() - wavefile.created_at
#     wavefile.save()
    # return


