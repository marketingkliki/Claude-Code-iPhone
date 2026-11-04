import json, wave, numpy as np
SR=48000; DUR=35.6; rng=np.random.default_rng(7)
W=json.load(open('words.json')); T=lambda i,j: W[i]['w'][j][1]
out=np.zeros(int(SR*DUR))
def add(t,x,g):
    i=int(t*SR); n=min(len(x),len(out)-i); out[i:i+n]+=x[:n]*g
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def whoosh(l=.45):
    n=int(SR*l); x=rng.standard_normal(n); y=np.zeros(n); c=np.linspace(.02,.25,n)**1.5
    for k in range(1,n): y[k]=y[k-1]+c[k]*(x[k]-y[k-1])
    return y*np.sin(np.pi*np.arange(n)/n)**2
def pop(f0=900,f1=320,l=.09):
    n=int(SR*l); f=np.linspace(f0,f1,n); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.002,.03)
def impact():
    n=int(SR*.5); f=np.linspace(110,40,n); b=np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.003,.16)
    nz=rng.standard_normal(n)*env(n,.001,.02)*.5; return b+nz
def tick(): n=int(SR*.05); return np.sin(2*np.pi*2300*np.arange(n)/SR)*env(n,.001,.012)
def chime():
    n=int(SR*1.6); t=np.arange(n)/SR; return (np.sin(2*np.pi*880*t)+.6*np.sin(2*np.pi*1320*t)+.3*np.sin(2*np.pi*1760*t))*env(n,.005,.45)
for t in [1.75,4.55,9.8,12.3,T(7,0),13.95,15.55,19.25,22.2,28.45]: add(t,whoosh(),.22)
for t in [T(9,4) if False else 9.38,T(8,0),T(14,2)]: add(t+.04,impact(),.55)
for t in [T(0,3),T(2,0),T(5,0),T(6,0),T(12,1),T(12,3),T(15,0),T(15,1),T(15,2),T(16,1),T(17,1)-.05,32.6]: add(t,pop(),.28)
for t in [T(8,3)+.1,T(10,0),T(10,2),T(16,4),19.4,19.6]: add(t,tick(),.22)
add(33.05,chime(),.16)
out=np.clip(out,-1,1); pcm=(out*32767).astype(np.int16)
with wave.open('sfx.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('sfx ok')
