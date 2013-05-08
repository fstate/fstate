cd stage1/
cp empty.txt valid.txt
python decay-cleaner.py > valid.txt
cd ../stage2
python make_fstates.py

