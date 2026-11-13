# Original generated track: 36.4 s, 110 bpm, C-G-Am-F. No samples, no third-party material.
import numpy as np, wave, sys
sr=44100; bpm=110; beat=60/bpm; bar=4*beat; dur=36.4
N=int(sr*dur); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(buf,t0,sig,g=1.0):
    i=int(t0*sr)
    if i>=N: return
    n=min(len(sig),N-i); buf[i:i+n]+=sig[:n]*g
def env(n,a=0.005,d=0.3):
    t=np.arange(n)/sr; return np.minimum(t/a,1)*np.exp(-t/d)
def f(m): return 440*2**((m-69)/12)
def pluck(m,length=0.5,d=0.18):
    n=int(sr*length); t=np.arange(n)/sr; fr=f(m)
    s=np.sin(2*np.pi*fr*t)+0.35*np.sin(2*np.pi*2*fr*t)*np.exp(-t/0.08)+0.15*np.sin(2*np.pi*3*fr*t)*np.exp(-t/0.05)
    return s*env(n,0.003,d)
def pad(ms,length):
    n=int(sr*length); t=np.arange(n)/sr; s=np.zeros(n)
    for m in ms:
        for det in (-0.06,0.06):
            s+=np.sin(2*np.pi*f(m+det)*t)+0.25*np.sin(2*np.pi*2*f(m+det)*t)
    e=np.minimum(t/0.4,1)*np.minimum((length-t)/0.4,1)
    return s*e/len(ms)
def bass(m,length):
    n=int(sr*length); t=np.arange(n)/sr; fr=f(m)
    s=np.sin(2*np.pi*fr*t)+0.3*np.sin(2*np.pi*2*fr*t)
    return np.tanh(1.5*s)*env(n,0.004,0.22)
def kick():
    n=int(sr*0.28); t=np.arange(n)/sr
    ph=2*np.pi*(48*t+ (110/ (1/0.03))*(1-np.exp(-t/0.03)))
    return np.sin(ph)*np.exp(-t/0.11)
def clap():
    n=int(sr*0.18); t=np.arange(n)/sr; x=rng.standard_normal(n)
    x=np.diff(x,prepend=0)  # brighten
    e=np.exp(-t/0.05)+0.6*np.exp(-np.abs(t-0.012)/0.004)
    return x*e*0.5
def hat(d=0.025):
    n=int(sr*0.08); t=np.arange(n)/sr; x=rng.standard_normal(n); x=np.diff(np.diff(x,prepend=0),prepend=0)
    return x*np.exp(-t/d)*0.25
chords=[(48,[60,64,67]),(43,[59,62,67]),(45,[60,64,69]),(41,[60,65,69])]  # C G Am F
nbars=int(np.ceil(dur/bar))
for b in range(nbars):
    t0=b*bar; root,tri=chords[b%4]
    full = b>=2; lift = b>=6
    p=pad(tri,bar); add(L,t0,p,0.10); add(R,t0,p,0.10)
    arp=[tri[0],tri[1],tri[2],tri[1]+12,tri[2],tri[1],tri[0]+12,tri[2]]
    for k in range(8):
        s=pluck(arp[k]+(12 if lift and k%2 else 0)); pan=0.35 if k%2 else 0.65
        add(L,t0+k*beat/2,s,0.22*pan*2); add(R,t0+k*beat/2,s,0.22*(1-pan)*2)
    if full:
        for k in range(4):
            add(L,t0+k*beat,kick(),0.9); add(R,t0+k*beat,kick(),0.9)
            bs=bass(root if k!=3 else root+7,beat/2)
            add(L,t0+k*beat+beat/2,bs,0.42); add(R,t0+k*beat+beat/2,bs,0.42)
        for k in (1,3):
            c=clap(); add(L,t0+k*beat,c,0.5); add(R,t0+k*beat,c,0.5)
        for k in range(8):
            h=hat(0.05 if k%2 else 0.02); add(L,t0+k*beat/2,h,0.5 if k%2 else 0.3); add(R,t0+k*beat/2,h,0.4 if k%2 else 0.35)
mix=np.stack([L,R],1)
t=np.arange(N)/sr
fade=np.minimum(t/0.05,1)*np.minimum((dur-t)/2.5,1)
mix*=fade[:,None]; mix=np.tanh(mix*1.1); mix/=np.abs(mix).max()/0.89
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((mix*32767).astype('<i2').tobytes()); w.close()
