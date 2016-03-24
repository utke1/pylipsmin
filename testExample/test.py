import adolc
import lipsmin
import numpy

def gpffin_init(n):
    x=numpy.zero(n)
    for i in xrange(n):
        x[i]=i+-24.5;
    return x

def goffin(ax, n):
    tmp1 = ax[0];
    for j in xrange(1,n):
        tmp1 = fmax(tmp1,ax[j]);
    tmp1 = n*tmp1;
    for i in xrange(n):
        tmp1-=ax[i];
    return tmp1;
    

def func(tag):
    n=50
    x=goffin_init(n)
    tag=1
    adolc.trace_on(tag)
    ax = adolc.independent(adolc.adouble(x))
    ay = goffin(ax,n)
    adolc.dependent(ay)
    trace_off()
    y=ay.val
    return y


def main():
    tag=1
    y=func(tag)
    f=open("test.out","rw")
    y=lipsmin.LiPsMin(f,tag,5.0,x)
    f.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
