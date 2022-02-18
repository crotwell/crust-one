# crust-one
Read Crust1.0 model in python.

https://igppweb.ucsd.edu/~gabi/crust1.html

Crust1.0 data files are at:
http://igppweb.ucsd.edu/~gabi/crust1/crust1.0.tar.gz

Now also with Crust2.0 data for comparison.


# build/release
```
conda create -n crust-one python=3.9
conda activate crust-one
python3 -m pip install --upgrade build
python3 -m build
pip install dist/crustone-0.0.4-py3-none-any.whl --force-reinstall
```

# dev autobuild
```
python3 -m pip install -e .
```

# maybe one day conda package:
```
conda install conda-build
```
