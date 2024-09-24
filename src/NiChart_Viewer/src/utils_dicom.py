import streamlit as st
import os
from math import ceil
import nibabel as nib
import numpy as np
from nibabel.orientations import axcodes2ornt, ornt_transform
import pydicom


def read_DICOM_slices(path):

    # Load the DICOM files
    files = []

    for fname in glob.glob(path + '*', recursive=False):
        if fname[-4:] == '.dcm': # Read only dicom files inside folders.
            files.append(pydicom.dcmread(fname))

    # Skip files with no SliceLocation
    slices = []
    skipcount = 0
    for f in files:
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount = skipcount + 1

    slices = sorted(slices, key=lambda s: s.SliceLocation)

    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # Fill 3D array with the images from the files
    for i, img2d in enumerate(slices):
        img3d[:, :, i] = img2d.pixel_array

    columns = ['PatientID', 'PatientName', 'StudyDescription', 'PatientBirthDate', 'StudyDate', 'Modality', 'Manufacturer', 'InstitutionName', 'ProtocolName']
    col_dict = {col: [] for col in columns}

    try:
        for col in columns:
            col_dict[col].append(str(getattr(files[0], col)))

        df = pd.DataFrame(col_dict).T
        df.columns = ['Patient']
    except:
        df = pd.DataFrame([])

    del files, slices, columns, col_dict

    return img3d, df

def display_info(path):
    columns = ['PatientID', 'PatientName', 'StudyDescription', 'PatientBirthDate', 'StudyDate', 'Modality', 'Manufacturer', 'InstitutionName', 'ProtocolName']
    col_dict = {col: [] for col in columns}
    dicom_object = pydicom.dcmread(path + os.listdir(path)[0])

    for col in columns:
        col_dict[col].append(str(getattr(dicom_object, col)))

    df = pd.DataFrame(col_dict).T
    df.columns = ['Patient']
    return df
