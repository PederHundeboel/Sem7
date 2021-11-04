FROM conda/miniconda3

WORKDIR /code

# copy the dependencies file to the working directory
COPY conda_dependencies.txt .
COPY pip_dependencies.txt .

# install dependencies
RUN conda update -n base -c defaults conda
RUN conda install --file conda_dependencies.txt
RUN pip install -r pip_dependencies.txt

COPY src/ .

# command to run on container start
CMD [ "python", "./downloader.py" ] 
