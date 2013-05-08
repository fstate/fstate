from multiparticles import multiparticle_fix # should be automatic
from nbaryon import N
from plusminus import pm
from Kbar import kbar
from pions import pipi
from muons import mumu
from phi import phi
from omega import omega

fixlist = [multiparticle_fix, kbar, phi, mumu, omega] 
multiplexers = [pm, N, pipi]
