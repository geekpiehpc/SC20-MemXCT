# Compile Script 
`run.sh` is provided for tuning parameters. `test_scale_3.sh` and `test_scale_4.sh` is to test the NF from 1 to 32 within inner cycle and outer cycle of the dataset of `ADS1` and `ADS2`, which produces the graph in the paper. `test_scale_strong.sh` is to produce the strong scaling graph. We suppose the datasets are decompressed into `$HOME/datasets` and the script produce the log at `./logs/` folder for you to see the best result from the tuned parameter.

## Datasets

There are 6 datasets, called `ADS1`, `ADS2`, `ADS3`, `ADS4`, `RDS1` and `RDS2`. 

## Environment

Our evaluation environment is 2 node epyc rome with 100Gbps infiniband connected.

Here take spack for package management for instance.

```bash
git clone https://github.com/spack/spack/
source $PWD/spack/share/spack/setup-env.sh
spack install intel-parallel-studio@cluster-2019.5
spack load intel-parallel-studio@cluster-2019.5
```