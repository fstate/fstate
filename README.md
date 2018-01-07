fstate
======

Final state search engine based on decay.dec of LHCb

To run from scratch run mongo server first:
```
mongod
```
Than in new terminal:
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

Web-deployement
------
To run the app on Debian 9 server, you need to run it from docker image. If you run from scratch, uncomments ilnes to build DB in docker-entrypoint.sh before.
```
docker-compose up
```
And to run nginx (to listen port 80):
```
cp nginx.conf /etc/nginx/
service nginx start
```
