## Creating a virtual environment
1. Create virtual environment with conda
conda create --name aima     # if python is lower than 3.7 on machine, specify " python=3.7" at the end

2. Activate it
   
source activate aima

4. When done, one can deactivate it too

conda deactivate

## Follow steps from aima-python github site
**Credits**: original [instructions](https://github.com/aimacode/aima-python)
1. To download the repository:
   
git clone https://github.com/aimacode/aima-python.git

2. Install dependencies

cd aima-python

pip install -r requirements.txt

3. Fetch the datasets 

git submodule init

git submodule update

4. Run  test suite

pip install pytest

py.test

