# Trabajo Final de Grado (undergraduate thesis)

   _Source code for OCS-WAF: a Web Application Firewall based
   on anomaly detection using One-Class SVM classifier._

## Running tests

   Tested with Python 3.5 on Ubuntu 14.04 and Windows 7

#### Install dependencies
   ```bash
   cd tfg
   pip install -r requirements.txt
   ```
   _If there are problems on Windows with some packages,
   [Anaconda](https://www.continuum.io/downloads) can be
   used to install them_.
   _In Ubuntu using `pip` should work just fine_.

#### Download necessary data sets
   - Paste files from [CSIC 2010 HTTP data sets](http://www.isi.csic.es/dataset/)
   into `/tfg/implementation/data_sets/csic/original_files/`
   - Paste files from [CSIC Torpeda 2012 HTTP data sets](http://www.tic.itefi.csic.es/torpeda/datasets.html)
   into `/tfg/implementation/data_sets/torpeda/original_files/`

#### Run the tests
   Use the script `run.py` to run the different tests; executing
   it without additional parameters displays the usage info,
   like this `python3 run.py`.
   
   For `test2` you have to start all four options of that test in
   their listed order, starting with the destination and concluding
   with source, waiting some seconds in between to give them some
   time to initialize.

## Compiling Latex files
   Use the script `run.py` to compile the latex source files and
   generate a PDF of our undergraduate thesis (proposal, complete
   book and summary article); executing it without additional parameters
   displays the usage info, like this `python3 run.py`.
   
   For the compilation process, the utilities `pdflatex`, `makeglossaries`
   and `bibtex` need to be installed.
   
   The compiled PDFs are also available in the folder `/tfg/pdfs/`.

## Authors
   - Nico Epp
   - Ralf Funk
   - Cristian Cappo (undergraduate thesis advisor)

## See also
   Check out the [paper](https://www.researchgate.net/publication/319490376_Anomaly-based_Web_Application_Firewall_using_HTTP-specific_features_and_One-Class_SVM)
   we submitted to the ERRC 2017 conference in Santa Maria, Brazil and
   the corresponding [source code](https://github.com/nico-ralf-ii-fpuna/paper).
