#!/bin/bash

#SBATCH --job-name=lab1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=62GB
#SBATCH --time=00:30:00
#SBATCH --res=morari 
#SBATCH --partition=c26
#SBATCH --exclusive
#SBATCH --output=out.%j

#Uncomment to execute C code
#module load intel/17.0.1
#./lab1

#Uncomment to execute python code
#module purge
#module load numpy/intel/1.13.1
#python ./lab1.py

#Uncomment to execute pytorch code
module load pytorch/python3.6/0.3.0_4
python ./lab1.pytorch 4
python ./lab1.pytorch 5
python ./lab1.pytorch 6
python ./lab1.pytorch 7
python ./lab1.pytorch 8
python ./lab1.pytorch 9
python ./lab1.pytorch 10
python ./lab1.pytorch 11
python ./lab1.pytorch 12
python ./lab1.pytorch 13
python ./lab1.pytorch 14
python ./lab1.pytorch 15
python ./lab1.pytorch 16
python ./lab1.pytorch 17
python ./lab1.pytorch 18
python ./lab1.pytorch 19
python ./lab1.pytorch 20
python ./lab1.pytorch 21
python ./lab1.pytorch 22

