# Opcode probability graph detector
# (Debugging !!!!)
---
>ref. Mehmood, Abid, Abdul Nasir Khan, and Mourad Elhadef. "HeuCrip: A malware detection approach for internet of battlefield things." Cluster Computing (2022): 1-16

---

## Introduction

### Descripition

* This is a malware detector which use the opcode sequence as feature
    
    - Input:a binary file
    
    - output:the probability of each class which is predicted by Machine method
    
### Feature Extraction

* feature 
    - opcode sequence 
* extracted tool
    - retdec
## Requirement
---
* python3
* retdec
* python package
    - tenserflow
    - sklearn
    
## File
* FC.pd : the models are responsible for classify the malware family (saved as pd)
* MD.pd : the models are responsible for classify the malware or benignware (saved as pd)
* TestingBin : the file that can test this detector
* main.py : the detector
* utils.py : for parsing args
* top_100_feature.npy : save the top 100 occurences of opcode name 

## Usage
* path of retdec decompiler: `-r <path>`, `--retdec-path <path>` 
* input binary: `-i <path>`, `--input-path <path>`
* output (record): `-o <path>`, `--output-path <path>`
* Malware Detection / Family Classification
    * do nothing if you wanna do malware detection(binary clf)  
    * add `-c` if you wanna do family classification 
* e.g.
    `python main.py -r home/retdec-install/bin/retdec_decompiler  TestingBin/malware/00a2bd396600e892da75c686be60d5d13e5a34824afd76c02e8cf7257d2cf5c5 -o myDetector_FC_records.csv -c`
    * using trained rf family classifier(`-c`), predict '00a2bd396600e892da75c686be60d5d13e5a34824afd76c02e8cf7257d2cf5c5' and write the result to 'myDetector_FC_records.csv'
    * add `-W ignore` if you keep getting bothered by warning msg
    
* output file format

  |    Filename  | Benignware | Malware |
  | :----------: | :------: | :-------: |
  | 00ffe391     |   0.97   |   0.03    |
  |     00f391fe      |  0.967   |  165.51   |
  |     1fe00f39      |  -1   |    |
  * it will record the prob of each class
  * -1 means fail

### Accuracy
* classification
    * 0.840
* Detect
    * 0.879