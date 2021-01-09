FROM  continuumio/miniconda3
LABEL Author, Dr. Timothy H. Click

ENV APP_HOME /amgen
WORKDIR $APP_HOME
COPY . $APP_HOME

#---------------- Prepare the envirennment
RUN conda update --name base conda &&\
    conda env create --file environment.yaml
SHELL ["conda", "run", "--name", "ambgen", "/bin/bash", "-c"]

ENTRYPOINT ["conda", "run", "--name", "ambgen", "python", "src/ambgen/cli.py"]
