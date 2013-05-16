from multiparticles import multiparticle_fix # should be automatic
from nbaryon import N
from plusminus import pm
from plusminus import lepton
from Kbar import kbar
from pions import pipi
from muons import mumu
from phi import phi
from omega import omega
from rho import rho
from kst import kst
from brakets import brakets

fixlist = [multiparticle_fix, brakets, kbar, phi, rho, omega, kst] 
multiplexers = [lepton, pm, N, pipi]
