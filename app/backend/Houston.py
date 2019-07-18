import flask
import numpy as np
import tensorflow as tf
from keras.models import load_model
import itertools
from app.backend.Hermes_Main import Sequence

def Launcher(email_address, sequence):
    query = Sequence(email_address, sequence)

    query.Transcribe()

    query.Translate()

    query.Protein_Layer()

    query.Structure_Layer()

    DNA, RNN, protein, protein_length, Hermes_final_solution = query.Final_Hermes()

    return DNA, RNN, protein, protein_length, Hermes_final_solution