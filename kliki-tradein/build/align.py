"""Estimate word times: speech islands from silencedetect + syllable-weighted split snapped to RMS onsets."""
import json, re, subprocess, sys
import numpy as np

VO = sys.argv[1]
OUT = sys.argv[2]
ISL = [(0.0,1.489),(1.895,3.323),(3.730,4.167),(4.800,7.446),(7.925,9.835),(10.205,11.544),
       (11.765,12.624),(12.784,13.924),(14.085,15.397),(15.693,17.087),(17.429,18.964),(19.379,20.050),
       (20.440,21.967),(22.237,23.228),(23.419,24.841),(25.160,28.458),(28.685,30.092),(30.258,32.257)]
TXT = ["Phone lama dah perlahan,","tapi duit nak upgrade","tak cukup?",
       "Jangan tunggu sampai phone tu langsung tak berguna.","Masa tu nilainya makin jatuh.",
       "Bawa phone lama ke KLIKI,","tolak nilainya,","upgrade ke phone lain.","Dibayar hari yang sama.",
       "Retak pun boleh dinilai,","asalkan phone masih boleh hidup.","Tak cukup lagi?",
       "Boleh ansuran dengan SPayLater.","Beli phone di KLIKI,","pindah data percuma.",
       "Gambar, contact, WhatsApp, semua ikut ke phone baru.","WhatsApp gambar phone lama anda,",
       "dapatkan anggaran harga trade-in dulu."]
SYL = {"phone":1,"upgrade":2,"kliki":2,"whatsapp":2,"contact":2,"spaylater":4,"trade-in":2}

sr = 16000
raw = subprocess.run(["ffmpeg","-v","error","-i",VO,"-ac","1","-ar",str(sr),"-f","s16le","-"],capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32)/32768
hop = int(0.01*sr); win = int(0.02*sr)
env = np.array([np.sqrt(np.mean(x[i:i+win]**2)+1e-12) for i in range(0,len(x)-win,hop)])
db = 20*np.log10(env)
rise = np.diff(db, prepend=db[0])

def syl(w):
    k = re.sub(r"[^a-z\-]","",w.lower())
    if k in SYL: return SYL[k]
    return max(1, len(re.findall(r"[aeiou]+", k)))

out = []
for i,((a,b),line) in enumerate(zip(ISL,TXT)):
    words = line.split()
    s = np.array([syl(w) for w in words], float)
    starts = a + (b-a)*np.concatenate([[0],np.cumsum(s)[:-1]])/s.sum()
    snapped = []
    for j,t in enumerate(starts):
        if j == 0: snapped.append(a); continue
        lo, hi = int((t-0.09)/0.01), int((t+0.09)/0.01)
        seg = rise[lo:hi]
        tt = (lo+int(np.argmax(seg)))*0.01 if len(seg) and seg.max() > 3 else t
        tt = max(tt, snapped[-1]+0.08)
        snapped.append(round(float(tt),2))
    out.append({"i":i,"a":a,"b":b,"line":line,"w":[[w,round(float(t),2)] for w,t in zip(words,snapped)]})
    print(f"{a:6.2f}-{b:6.2f}  " + "  ".join(f"{w}@{t:.2f}" for w,t in zip(words,snapped)))
json.dump(out, open(OUT,"w"), ensure_ascii=False, indent=1)
