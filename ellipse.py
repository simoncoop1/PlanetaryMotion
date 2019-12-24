import math
import numpy as np
from curses import wrapper
import locale
import time
from time import sleep

locale.setlocale(locale.LC_ALL, '')

##given a eccentricity ec, eccentic anomoly eca, period prd
## calculate the time as a fraction of period
def ecaTime(ec,eca,prd):
    return (((eca-(ec*math.sin(eca)))*prd)/(2*math.pi))


## eccentricity
def ecntcty(a,b):
    return (1-((float(b)/a)**2))**0.5

## foci
def fci(a,b):
    return (a**2 - b**2)**0.5

##create a table with eccentric anomoly,  time, x, t
def init(a,b):


    foci = fci(a,b)

    if foci == (((a**2) - (b**2))**0.5):
        print "good"

    ec = ecntcty(a,b)
    
    print "ecentricity " + str(ec)
    print "foci " + str(foci) 

    ##ecentric anomoly

    prd = 1

    ##how much the eccentric anomoly is split
    dv = 80

    i = (math.pi*2)/dv

    das = ()

    da = (i,)
    da = da + ( (((da[0]-(ec*math.sin(da[0])))*prd)/(2*math.pi)) , )

    das = das + (da,)

    for x in range(2,dv+1):
        da = (i*x,)
        da = da + ( ecaTime(ec, da[0],prd) , )
        das = das + (da,)

    return das


##find an initial value for numeric method
## data to work on a
## toggle for alternate in case of diverging
## target time
def numericInit(a,toggle,tt):

    ## newton rasphson method
    ## target time tt
    ## initial value x
    ## prd period
    ## eccentric anomoly eca
    ## ecentricity e
    if(toggle == True):
        ##get alternative init
        raise ValueError('get a converging init') 

    bst = ()

    for l in a:
        if l[1]<tt:
            bst = l
        else:
            break
    

    return bst[0]

##generate times from 0 to 1
## eg if for have a period of 10 seconds and we wanted 30 value per second for 30fps
## then we need 300 values between 0 and 1
## vps values we want per second
## rtp real time period (seconds)
def GenTm(rtp, vps):
    tms = ()

    i = 1 / float(rtp * vps)

    for x in range(1,(rtp*vps)+1):
        tms = tms + (i*x,)

    return tms

    

def numericSolve(x,tt,prd,ec):
    ## x - (fx/f'x)
    fx = ecaTime(ec,x,prd) - tt
    fx1 = (math.pi*(1-(ec*math.cos(x))))/2
    s1 = x -(fx/fx1)
    ##print "first solve " + str(s1)

    ##is it diverging or converging
    if(abs((ecaTime(ec,s1,prd) - tt)) > abs(fx)):
        x = numericInit(None,False)
        raise ValueError('problem, diverging') 

    ##assume converging

    ##accuracy = 10 digits (not required)
    
    cont = True
    while cont == True:
        fx = ecaTime(ec,s1,prd) - tt
        fx1 = (math.pi*(1-(ec*math.cos(s1))))/2
        sl0 =s1
        s1 = s1 -(fx/fx1)
        ##print "first solve " + str(s1) + ", " + str(ecaTime(ec,s1,prd) - tt)
        if s1 == sl0:
            cont = False

    ## the optimised value
    return s1

def drawellipse(stdscr):
    
    stdscr.clear()

    stdscr.addstr(0, 0, 'this is a string {},{}'.format(stdscr.getmaxyx()[0],stdscr.getmaxyx()[1]))

    a = 40

    b = 12

    ##if y = 0
    y = 12
    x = 40
    yco = int(stdscr.getmaxyx()[0]-(stdscr.getmaxyx()[0]/float(2)))+y
    xco = int(stdscr.getmaxyx()[1]-(stdscr.getmaxyx()[1]/float(2)))+x
    ou = ""
   
    for k in range(1,25+1):
        t = ((2*math.pi)/float(25))*k
        x = int(a*math.cos(t))
        y = int(b*math.sin(t))

        ##ou = ou + " " +str(x) + "," + str(40-x)
        ##stdscr.addstr(0,0,ou)
        
        

        try:##addstrj param are y then x order
            stdscr.addstr(12-y,40-x, u'\u2585'.encode('UTF-8'))
        except:
            print "caught it " + str(x+40) + str(x+40)
        
    stdscr.refresh()    
    stdscr.getkey()

    return

def playellipse(stdscr,bt):
    #raise ValueError('no') 

    stdscr.clear()

    stdscr.addstr(12,40-int(fci(40,12)),u'\u2585'.encode('UTF-8'))
    stdscr.addstr(0,0, 'ok yes')

    orbits = 10

    for x in range(orbits):

        now1=time.time()
        interval = 1/float(15)


        for r in bt:
            time2=time.time()
            sleepm = interval - (time2-now1)
            ##stdscr.addstr(12-r[3],40-r[2], "sleep " + str(sleepm))
            ##stdscr.refresh()
            sleep(sleepm)
            now1=time.time()
            stdscr.addstr(12-r[3],40-r[2], u'\u2585'.encode('UTF-8'))
            stdscr.refresh()
    
    

    stdscr.refresh()    
    stdscr.getkey()
    


##

a = 40
b = 12

at = init(a,b )
bt = ()
#print(np.matrix(at))
#numericSolve(0.63,0.02,1,ecntcty(2,1))

 

for tt in GenTm(10, 15):
    p = numericInit(at,False,tt)
    s1 = numericSolve(p,tt,1,ecntcty(a,b))
    k = (s1,tt,int(a*math.cos(s1)),int(b*math.sin(s1)))
    bt= bt + (k, )

print(np.matrix(bt))

##wrapper(drawellipse)
wrapper(playellipse,bt)


