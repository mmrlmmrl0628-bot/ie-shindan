# 場面の開始時刻に合わせてナレーションを並べ、動画に合成する。 python3 mux.py frames_dir out.mp4
import json, subprocess, sys
fr, out = sys.argv[1], sys.argv[2]
starts = json.load(open('starts.json'))
cmd = ['ffmpeg','-y','-loglevel','error','-framerate','24','-i',f'{fr}/%05d.jpg']
for i in range(len(starts)): cmd += ['-i', f'audio/s{i+1:02d}.mp3']
flt = ';'.join(f'[{i+1}:a]adelay={int((t+0.3)*1000)}|{int((t+0.3)*1000)}[a{i}]' for i, t in enumerate(starts))
flt += ';' + ''.join(f'[a{i}]' for i in range(len(starts))) + f'amix=inputs={len(starts)}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]'
cmd += ['-filter_complex', flt, '-map','0:v','-map','[aout]','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart', out]
subprocess.check_call(cmd)
