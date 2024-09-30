import plotly.express as px
import os
import streamlit as st
import tkinter as tk
from tkinter import filedialog
import utils_st as utilst
import utils_nifti as utilni
import utils_dicom as utildcm
import pandas as pd
import numpy as np

VIEWS = ["axial", "sagittal", "coronal"]


result_holder = st.empty()
def progress(p, i, decoded):
    with result_holder.container():
        st.progress(p, f'Progress: Token position={i}')
        #if decoded and decoded[0]:
            #st.markdown(decoded[0])

#out = model.generate([input_text], 
                     #max_gen_len=max_seq_len, 
                     #temperature=temperature, 
                     #top_p=top_p, 
                     #callback=progress)


st.markdown(
        """
    1. Select Output: Select the folder where all results will be saved.
    2. Select Input: Choose the directory containing your raw DICOM files.
    3. Detect Series: The application will automatically identify different imaging series within the selected folder.
    4. Choose Series: Select the specific series you want to extract. You can pick multiple series if necessary.
    5. Extract Nifti Scans: Convert the selected DICOM series into Nifti format.
    6. View Nifti Scans: View extracted scans.
        """
)

# Panel for output (dataset name + out_dir)
with st.expander('Select output', expanded = True):
    # Dataset name: All results will be saved in a main folder named by the dataset name
    helpmsg = "Each dataset's results are organized in a dedicated folder named after the dataset"
    dset_name = utilst.user_input_text("Dataset name", st.session_state.dset_name, helpmsg)

    # Out folder
    helpmsg = 'Extracted Nifti images will be saved to the output folder.\n\nChoose the path by typing it into the text field or using the file browser to browse and select it'
    path_out = utilst.user_input_folder("Select folder",
                                        'btn_sel_out_dir',
                                        "Output folder",
                                        st.session_state.path_last_sel,
                                        st.session_state.path_out,
                                        helpmsg)
    if dset_name != '' and path_out != '':
        st.session_state.dset_name = dset_name
        st.session_state.path_out = path_out
        st.session_state.path_dset = os.path.join(path_out, dset_name)
        st.session_state.path_nifti = os.path.join(path_out, dset_name, 'Nifti')

        if st.session_state.path_dset != '':
            if not os.path.exists(st.session_state.path_dset):
                os.makedirs(st.session_state.path_dset)
            st.success(f'Results will be saved to: {st.session_state.path_dset}')

# Panel for detecting dicom series
if st.session_state.dset_name != '':
    with st.expander('Detect dicom series', expanded = True):
        # Input dicom image folder
        helpmsg = 'Input folder with dicom files (.dcm).\n\nChoose the path by typing it into the text field or using the file browser to browse and select it'
        path_dicom = utilst.user_input_folder("Select folder",
                                        'btn_indir_dicom',
                                        "Input dicom folder",
                                        st.session_state.path_last_sel,
                                        st.session_state.path_dicom,
                                        helpmsg)
        st.session_state.path_dicom = path_dicom

        flag_btn = os.path.exists(st.session_state.path_dicom)

        # Detect dicom series
        btn_detect = st.button("Detect Series", disabled = not flag_btn)
        if btn_detect:
            with st.spinner('Wait for it...'):
                df_dicoms, list_series = utildcm.detect_series(path_dicom)
                if len(list_series) == 0:
                    st.warning('Could not detect any dicom series!')
                else:
                    st.success(f"Detected {len(list_series)} dicom series!", icon = ":material/thumb_up:")
                st.session_state.list_series = list_series
                st.session_state.df_dicoms = df_dicoms

# Panel for selecting and extracting dicom series
if len(st.session_state.list_series) > 0:
    with st.expander('Select dicom series', expanded = True):

        # Selection of img modality
        helpmsg = 'Modality of the extracted images'
        st.session_state.sel_mod = utilst.user_input_select('Image Modality',
                                                            ['T1', 'T2', 'FL', 'DTI', 'rsfMRI'], 'T1',
                                                            helpmsg)
        # Selection of dicom series
        st.session_state.sel_series = st.multiselect("Select series:",
                                                     st.session_state.list_series,
                                                     [])
        # Create out folder for the selected modality
        if len(st.session_state.sel_series) > 0:
            if st.session_state.path_nifti != '':
                st.session_state.path_selmod = os.path.join(st.session_state.path_nifti,
                                                            st.session_state.sel_mod)
                if not os.path.exists(st.session_state.path_selmod):
                    os.makedirs(st.session_state.path_selmod)

        # Button for extraction
        flag_btn = st.session_state.df_dicoms.shape[0] > 0 and len(st.session_state.sel_series) > 0
        btn_convert = st.button("Convert Series", disabled = not flag_btn)
        if btn_convert:
            with st.spinner('Wait for it...'):
                utildcm.convert_sel_series(st.session_state.df_dicoms,
                                        st.session_state.sel_series,
                                        st.session_state.path_selmod)
                st.session_state.list_input_nifti = [f for f in os.listdir(st.session_state.path_selmod) if f.endswith('nii.gz')]
                if len(st.session_state.list_input_nifti) == 0:
                    st.warning(f'Could not extract any nifti images')
                else:
                    st.success(f'Extracted {len(st.session_state.list_input_nifti)} nifti images')

            # utilst.display_folder(st.session_state.path_selmod)

# Panel for viewing extracted nifti images
if len(st.session_state.list_input_nifti) > 0:
    with st.expander('View images', expanded = True):
    #with st.container(border=True):

        # Selection of MRID
        sel_img = st.selectbox("Select Image",
                               st.session_state.list_input_nifti,
                               key=f"selbox_images",
                               index = 0)
        st.session_state.path_sel_img = os.path.join(st.session_state.path_selmod, sel_img)

        # Create a list of checkbox options
        list_orient = st.multiselect("Select viewing planes:", VIEWS, VIEWS)

        flag_btn = os.path.exists(st.session_state.path_sel_img)

        with st.spinner('Wait for it...'):

            # Prepare final 3d matrix to display
            img = utilni.prep_image(st.session_state.path_sel_img)

            # Detect mask bounds and center in each view
            img_bounds = utilni.detect_img_bounds(img)

            # Show images
            blocks = st.columns(len(list_orient))
            for i, tmp_orient in enumerate(list_orient):
                with blocks[i]:
                    ind_view = VIEWS.index(tmp_orient)
                    utilst.show_img3D(img, ind_view, img_bounds[ind_view,:], tmp_orient)


# FIXME: this is for debugging; will be removed
with st.expander('session_state: All'):
    st.write(st.session_state.df_dicoms)
    st.write(st.session_state.sel_series)
