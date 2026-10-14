import json, glob, os, traceback
os.makedirs('fetch/out/transcripts', exist_ok=True)
try:
    from faster_whisper import WhisperModel
    m = WhisperModel('medium', device='cpu', compute_type='int8')
    for f in glob.glob('fetch/audio/*.mp3'):
        segs, _ = m.transcribe(f, language='fr', word_timestamps=True)
        out = [{'s': s.start, 'e': s.end, 't': s.text, 'w': [[w.start, w.end, w.word] for w in s.words]} for s in segs]
        json.dump(out, open('fetch/out/transcripts/' + os.path.basename(f) + '.json', 'w'), ensure_ascii=False, indent=1)
except Exception:
    open('fetch/out/transcripts/error.txt', 'w').write(traceback.format_exc())
