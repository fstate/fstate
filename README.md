fstate
======

Final state search engine based on decay.dec of LHCb

To run from scratch:

```
cd parrticleparser
python parse_particle.py
cd ../decaydecparser
python parser.py
cd ../createdatabase
python make_fstates.py  #(here you may use pypy as well. parameters of compiled db are in config.py)
cd ../web
python server.py
```
