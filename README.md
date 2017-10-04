# Trabajo Final de Grado (undergraduate thesis)

_Code for the Web Application Firewall we present in our undergraduate thesis._

This is a simple implementation of a Web Application Firewall (WAF) based on Anomaly Detection using One Class SVM.


## Getting Started

Tested with Python 3.5 on Ubuntu 14.04 and Windows 7

#### Install dependencies
```bash
cd paper
pip install -r requirements.txt
```
_If there are problems on Windows with some packages, [Anaconda](https://www.continuum.io/downloads) 
can be used to install them_.
_In Ubuntu using `pip` should just work fine_.

#### Download necessary data sets
- Paste files from [CSIC 2010 HTTP data sets](http://www.isi.csic.es/dataset/) into `/waf/data_sets/csic/original_files/`
- Paste files from [CSIC Torpeda 2012 HTTP data sets](http://www.tic.itefi.csic.es/torpeda/datasets.html) into `/waf/data_sets/torpeda/original_files/`

#### Run the code
   Use the `run.py` file to run the different tests.
   For example, `python3 run.py test1`. To see which tests are available, run the file 
   without additional commands or parameters like this `python3 run.py`.
   To test the proxy implementation you have to start all the tests beginning with `test2` in 
   their listed order (alphabetical order), starting with the data server and concluding with 
   source, waiting some seconds between the executions to give them some time to initialize.

## Latex source code
   The folder `thesis/latex` contains the latex source code of our undergraduate thesis.
   It includes a script to compile the code and generate a PDF file, using the utilities `pdflatex` and `bibtex`.

## Authors
- Nico Epp
- Ralf Funk
- Cristian Cappo (undergraduate thesis advisor)

## See also
   Check out the [paper](https://www.researchgate.net/publication/319490376_Anomaly-based_Web_Application_Firewall_using_HTTP-specific_features_and_One-Class_SVM)
   we submitted to the ERRC 2017 conference in Santa Maria, Brazil
   and the corresponding [code](https://github.com/nico-ralf-ii-fpuna/paper).
