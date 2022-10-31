import logging
import os, glob
import music21, mido
import wave
import soundfile as sf

import cfg
import json_utils

log_file = os.path.join(cfg.DATASET_DIR,"Errors.txt")
logging.basicConfig(filename=log_file, filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
print_log = logger.info

JSON_FILES = glob.glob(os.path.join(cfg.DATASET_DIR, "*.json"))
WAV_FILES = glob.glob(os.path.join(cfg.DATASET_DIR, "*.wav"))
MIDI_FILES = glob.glob(os.path.join(cfg.DATASET_DIR, "*.mid"))

print_log("###############################################################################################################")
print_log("compare json & wav file")
# fields to be checked
# play_time, samplingRate, bitDepth, channel
for JSON_FILE in JSON_FILES:
    # load json & wav files on memory
    WAV_FILE = JSON_FILE.replace(".json", ".wav")
    if WAV_FILE in WAV_FILES:
        try:
            with sf.SoundFile(WAV_FILE) as sf_reader:
                framerate=sf_reader.samplerate
                duration_wav = sf_reader.frames/framerate
                nchannels=sf_reader.channels
                subtype = sf_reader.subtype
                bitDepth_wav = 24 if subtype=="PCM_24" else 16 if subtype=="PCM_16" else 32
        except Exception as e:
            # 1 : pcm
            # 3 : ieee float
            # 65534 : extensible
            print(e)
            continue
    else:
        print(f"{WAV_FILE} not found!")
        continue

    JSON = json_utils.loadjson(JSON_FILE)
    try: # json의 파라미터 가져오기
        channel_json = 1 if JSON["music_source_info"]["channel"]=="M" else 2 if JSON["music_source_info"]["channel"]=="S" else -1
        sampling_rate_json = JSON["music_source_info"]["samplingRate"]
        duration_json = JSON["music_source_info"]["play_time"]
        bitDepth_json = JSON["music_source_info"]["bitDepth"]
    except KeyError as k:
        print(f"{JSON_FILE} don't have key {k}")
        continue

    log_written = False
    # compare json & wav
    if nchannels != channel_json:
        print_log(f"{WAV_FILE} has {nchannels} channel vs. {JSON_FILE} has {channel_json} channel")
        log_written = True
    if (duration_wav - duration_json) > cfg.DURATION_TOLERANCE: # 1초 이상 차이나면 다른 것으로 판단
        print_log(f"{WAV_FILE} has {duration_wav} play_time vs. {JSON_FILE} has {duration_json} play_time")
        log_written = True
    if framerate != sampling_rate_json:
        print_log(f"{WAV_FILE} has {framerate} sampling rate vs. {JSON_FILE} has {sampling_rate_json} sampling rate")
        log_written = True
    if bitDepth_wav != bitDepth_json:
        print_log(f"{WAV_FILE} has {bitDepth_wav} bitDepth vs. {JSON_FILE} has {bitDepth_json} bitDepth")
        log_written = True
    if log_written:
        print_log("---------------------------------------------------------------------------------------------------------------")



print_log("###############################################################################################################")
print_log("compare json & midi file")
for JSON_FILE in JSON_FILES:
    # load json & wav files on memory
    MIDI_FILE = JSON_FILE.replace(".json", ".mid")
    if MIDI_FILE in MIDI_FILES:
        midi = mido.MidiFile(MIDI_FILE)
        for msg in midi:
            if msg.type=='set_tempo':
                tempo_midi = mido.tempo2bpm(msg.tempo)
                break
    else:
        print(f"{MIDI_FILE} not found!")
        continue

    JSON = json_utils.loadjson(JSON_FILE)
    try:
        tempo_json = JSON["annotation_data_info"]["tempo"][0]["annotation_code"]
    except KeyError as k:
        print(f"{JSON_FILE} don't have key {k}")
        continue
    except IndexError as i:
        print(f"{JSON_FILE}'s tempo field is empty")
        continue

    log_written = False
    # compare json & wav
    try:
        if (tempo_midi - tempo_json) > cfg.BPM_TOLERANCE:
            print_log(f"{MIDI_FILE} bpm {tempo_midi} vs. {JSON_FILE} bpm {tempo_json}")
            log_written = True
        if log_written:
            print_log("---------------------------------------------------------------------------------------------------------------")
    except TypeError as t:
        print(JSON_FILE, f"has None value in ['annotation_data_info']['tempo'][0]['annotation_code'] field")
        continue
