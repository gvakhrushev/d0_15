#!/usr/bin/env python3
"""Short candidate Golden powers, each accepted by exact complex balls.

Optional existing gmpy2 changes speed only. Candidate mpmath is untrusted.
Every actual integer power is enclosed at the selected target precision.
"""
from pathlib import Path
from hashlib import sha256
import sys,json,gzip
sys.dont_write_bytecode=True
import two_bit_source_targets as t
for d in (t.loc.B/'round75/.deps',t.loc.B/'round42/.deps'):sys.path.insert(0,str(d))
try:import gmpy2 as gm
except ImportError:gm=None
import mpmath as mp


class Dyadic(t.Dyadic):
    def __init__(self,bits):
        super().__init__(bits)
        if gm:self.scale=gm.mpz(self.scale)
    def sqrt(self,a):
        if not gm:return super().sqrt(a)
        assert a[0]>=0
        lo=gm.isqrt(a[0]*self.scale);x=a[1]*self.scale;hi=gm.isqrt(x)
        return lo,hi+(hi*hi<x)


class Certifier:
    def __init__(self,controls,bits=3456,precision=8192):
        assert precision>=2*bits+512
        self.controls,self.bits,self.precision=controls,bits,precision
        self.iv=Dyadic(precision);self.S=self.iv.scale;self.c=t.cf.constants(self.iv)
        a,p=self.c['sqrtp'],self.c['p']
        self.powers=[(a[0],p[0],a[1]-a[0]+p[1]-p[0])]
        for _ in range(bits+128):self.powers.append(self.ballmul(self.powers[-1],self.powers[-1]))
        self.records={};self.unique={}
        with mp.workprec(3*bits+256):
            x=(1<<controls)*mp.acos(mp.sqrt((mp.sqrt(5)-1)/2))/(2*mp.pi)
            p0,p1,q0,q1,steps=0,1,1,0,0
            while True:
                z=int(mp.floor(x));pn=z*p1+p0;qn=z*q1+q0;steps+=1
                if qn.bit_length()>=bits+36:break
                p0,p1,q0,q1=p1,pn,q1,qn;x=1/(x-z)
        assert qn.bit_length()<bits+100
        self.pn,self.qn,self.steps,self.inv=pn,qn,steps,pow(pn,-1,qn)

    def ballmul(self,x,y):
        c,s,r=x;C,T,R=y;S=self.S
        return ((c*C-s*T)>>self.precision,(c*T+s*C)>>self.precision,
                r+R+((r*R+S-1)>>self.precision)+2)

    def power(self,n):
        assert type(n) is int and n>0 and n.bit_length()<=len(self.powers)
        x=(self.S,0,0);j=0
        while n:
            if n&1:x=self.ballmul(x,self.powers[j])
            n>>=1;j+=1
        c,s,r=x;return (c-r,c+r),(s-r,s+r)

    @staticmethod
    def digest(c,s):return sha256('|'.join(hex(int(x)) for x in (*c,*s)).encode()).hexdigest()

    def certify(self,c,s):
        c=(max(-self.S,c[0]),min(self.S,c[1]));s=(max(-self.S,s[0]),min(self.S,s[1]))
        assert c[0]<=c[1] and s[0]<=s[1]
        key=self.digest(c,s)
        if key in self.unique:return self.unique[key]
        with mp.workprec(3*self.bits+256):
            cm=mp.mpf(int(c[0]+c[1]))/(2*int(self.S));sm=mp.mpf(int(s[0]+s[1]))/(2*int(self.S))
            turn=(mp.atan2(sm,cm)/(2*mp.pi))%1
            target=int(mp.nint(self.qn*turn))%self.qn;k=(target*self.inv)%self.qn
            if not k:k=self.qn
        nc,ns=self.power(k*(1<<self.controls))
        err=max(abs(nc[0]-c[1]),abs(nc[1]-c[0]))+max(abs(ns[0]-s[1]),abs(ns[1]-s[0]))
        assert err<=self.S>>self.bits,('uncertified angle',len(self.records))
        name='angle_'+str(len(self.records));self.unique[key]=name
        self.records[name]={'k':str(k),'k_binary_length':k.bit_length(),
          'native_exponent_multiplier':1<<self.controls,'target_sha256':key,
          'operator_error_L1_numerator_hex':hex(int(err)),'certified_error_bits':self.bits}
        return name

    def controlled_x(self):
        iv=self.iv;aid=self.certify(iv.rational(0),iv.rational(1));entry=self.records[aid]
        nc,ns=self.power(int(entry['k'])*(1<<(self.controls+1)))
        err=max(abs(nc[0]+self.S),abs(nc[1]+self.S))+max(abs(ns[0]),abs(ns[1]))
        combined=err+int(entry['operator_error_L1_numerator_hex'],16)
        assert combined<=self.S>>self.bits
        return {'rotation_angle_id':aid,'phase_native_exponent_multiplier':1<<(self.controls+1),
          'X_error_L1_numerator_hex':hex(int(combined)),'certified_X_error_bits':self.bits}

    def metadata(self):
        return {'precision_bits':self.precision,'per_macro_error_le':'2^-'+str(self.bits),
          'controls':self.controls,'candidate_grid_not_proof':{'numerator':str(self.pn),
            'denominator':str(self.qn),'steps':self.steps},'angles':self.records}


def save_gzip(path,obj):
    with Path(path).open('wb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as out:out.write(json.dumps(obj,separators=(',',':')).encode())
