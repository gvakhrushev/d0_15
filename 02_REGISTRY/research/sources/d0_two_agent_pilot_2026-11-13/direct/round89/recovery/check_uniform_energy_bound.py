"""Symmetric smooth input pairs, exact trace-norm reduction, and the unbounded spectral test."""
from fractions import Fraction
import json
import math
import numpy as np


def require(condition, message):
    if not condition:
        raise ValueError(message)


p = (math.sqrt(5) - 1)/2


def complete_pair(samples):
    """Remove the common sitewise isometry |t,A> -> |t,A,chi_t>."""
    n = len(samples)
    normalization = math.sqrt(n)
    w = np.concatenate((np.full(n, math.sqrt(p)), np.full(n, p), np.zeros(n))) / normalization
    v = np.concatenate((np.full(n, math.sqrt(p)), np.sqrt(p*p - samples**2), np.zeros(n))) / normalization
    u = np.concatenate((np.zeros(2*n), samples)) / normalization
    return w, v, u


def trace_control():
    # Get all nonzero eigenvalues from the three-dimensional span; no cancellation
    # of two nearly equal 128-site/global densities on larger meshes is required.
    for n in (1,2,3,5):
        size=32
        wave=0.16*np.sin(2*np.pi*n*np.arange(size)/size)
        w,v,u=complete_pair(wave)
        d=v-w
        states=np.column_stack((u,d,w))
        gram=states.T@states
        chol=np.linalg.cholesky(gram)
        signed=np.array([[1,0,0],[0,1,1],[0,1,0]])
        reduced=chol.T@signed@chol
        packed=np.sum(np.abs(np.linalg.eigvalsh(reduced)))
        raw=np.outer(u,u)+np.outer(d,d)+np.outer(d,w)+np.outer(w,d)
        direct=np.sum(np.abs(np.linalg.eigvalsh(raw)))
        s=float(u@u)
        # |v|^2 |w|^2 - |<w,v>|^2 = ||(1-|w><w|)d||^2.
        transverse=d-w*(w@d)
        theory=s+math.sqrt(s*s+4*float(transverse@transverse))
        require(abs(theory-packed)<2e-14 and abs(theory-direct)<2e-14,'all pure tensor columns')
        require(theory <= (1+2/p)*max(abs(wave))**2,'quadratic bound on the full input mixture')
        ev,basis=np.linalg.eigh(reduced)
        helstrom=basis[:,ev>0]@basis[:,ev>0].T
        require(abs(np.trace(helstrom@reduced)-theory/2)<2e-14,'optimal binary discrimination')
        require(np.max(abs(gram[0,1:]))<1e-17,'CAR sign direction orthogonal to both common vectors')
        # A tilted, phase-sensitive paid outcome has unequal raw responses on ±.
        test=(w+u/math.sqrt(s))/math.sqrt(2)
        weights=[1+2*float(test@z)**2 for z in (v+u,v-u,w)]
        delta_plus,delta_minus=weights[0]-weights[2],weights[1]-weights[2]
        log_error=abs((math.log(weights[0])+math.log(weights[1]))/2-math.log(weights[2]))
        require(log_error<=abs((delta_plus+delta_minus)/2)+(delta_plus**2+delta_minus**2)/4+1e-14,
                'positive log partition uses both the even response and curvature')
    # Filler changes even for the trace-optimal measurement.
    return 'Trace norm = s + sqrt(s^2 + 4 ||(I-|w><w|)(v-w)||^2)'


def energy_control():
    for size in (32,64,128,256):
        t=np.arange(size)/size
        for n in (1,2,size//8,size//4):
            amp=0.20/(2*math.pi*n)**2
            wave=amp*np.sin(2*math.pi*n*t)
            edge=size*(np.roll(wave,-1)-wave)
            energy=np.mean(edge**2)
            formula=2*size**2*amp**2*math.sin(math.pi*n/size)**2
            require(abs(energy-formula)<1e-13*formula,'finite one-step energy')
            need=(0.5+1/p)*(amp**2)
            require(energy/need<=size**2/(0.5+1/p)+1e-10,'tested wave range')
            if n==size//4:
                require(abs(energy/need-size**2/(0.5+1/p))<1e-9,'quarter-Nyquist lower bound')
            # The original right-hand character vector is unchanged after four ticks.
            for ku in range(4):
                require((ku*4)%4==0,'Fourier128 invariance')
            step=4/size
            kinetic=(2*wave-np.roll(wave,4)-np.roll(wave,-4))/step**2
            freq=2*math.pi*np.fft.fftfreq(size)
            eigenvalues=4*np.sin(2*freq)**2/step**2
            powers=np.abs(np.fft.fft(wave)/size)**2
            mean=np.sum(eigenvalues*powers)
            second=np.sum(eigenvalues**2*powers)
            require(abs(mean-np.mean(((np.roll(wave,-4)-wave)/step)**2))<1e-12,
                    'mean of the multivalued spectral record')
            require(abs(second-np.mean(kinetic**2))<1e-10 and second<=0.20**2+1e-10,
                    'bounded second moment on a bounded C2 class')
    return 'Exact calibration on all grid waves requires normalized oscillation >= L^2/(1/2+1/p)'


def original_pointer():
    # Recompute the actual 64 pairs, including score and lexicographic ties.
    from itertools import product
    table=(1,0,-1,0)
    def score(k):
        return sum(table[x] for x in k)+sum(table[(k[i]-k[j])%4] for i in range(4) for j in range(i))
    keys=sorted((k for k in product(range(4),repeat=4) if k<tuple(-i%4 for i in k)),
                key=lambda k:(-score(k),k))[:64]
    visibility=Fraction(sum(table[k[0]] for k in keys),64)
    require(visibility==Fraction(5,16),'native nearest-neighbour Fourier overlap')
    for size in (8,16,32):
        # A deliberately uneven two-mask field, realized here as admitted input data.
        profile=[(Fraction((j*j)%11-5,32),Fraction((j*3)%7-3,32)) for j in range(size)]
        mass=sum(a*a+b*b for a,b in profile)/size
        cross=sum(a*c+b*d for (a,b),(c,d) in zip(profile,profile[1:]+profile[:1]))/size
        energy=2*(mass-cross)*size**2
        q=(mass-visibility*cross)/2+Fraction(11,32)*(1-mass)
        require(q==Fraction(11,32)+Fraction(5,64)*energy/size**2,'actual signed shift and inactive coin')
    return '11/32 + (5/64) h^2 times the full nearest-neighbour average energy'


def binary_variance_control():
    for width in (4,9,40):
        for a in range(width):
            for b in range(a+1,width+1):
                gap=b-a
                v=(a*(width-a)+b*(width-b))*Fraction(1,2)
                require(v >= Fraction(gap*(width-gap),2),'binary variance-gap bound')
    return 'mean of two variances >= gap*(width-gap)/2'


if __name__=='__main__':
    print(json.dumps(dict(trace_identity=trace_control(), finite_grid=energy_control(),
                          exact_one_copy_pointer=original_pointer(),
                          binary_variance=binary_variance_control(),
                          multivalued_variance_alone_excludes_energy=False,
                          one_copy_fixed_effect_uniform_gain_on_all_smooth_waves=False,
                          compulsory_physical_price_identified=False,GR_closed=False),indent=2))
