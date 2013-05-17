from multiparticles import multiparticle_fix # should be automatic
from wave import wave
from wave import wave2
from nbaryon import N
from plusminus import pm
from plusminus import lepton
from plusminus import gamma
from Kbar import kbar
from pions import pipi
from muons import mumu
from phi import phi
from omega import omega
from rho import rho
from kst import kst
from brakets import brakets
from brakets import including
from cascade import cascade1
from cascade import cascade2
from cascade import cascade3
from cascade import cascade4
from pipi import pipi
from threebody import tbody
from space import space
from sigma import sigma
from sigma import sigmahimass
from nbaryon import pipii
from nbaryon import nporn
from nbaryon import Delta

fixlist = [pipii, nporn, pipi, space, sigma, multiparticle_fix, brakets, kbar, phi, omega, kst, cascade1, cascade2, cascade3, cascade4, rho, including, wave, wave2, tbody] 
multiplexers = [sigmahimass, lepton, pm, N, pipi, gamma, Delta]

