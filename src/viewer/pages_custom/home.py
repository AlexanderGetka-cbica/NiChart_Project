import os

import pandas as pd
import streamlit as st

# Initiate Session State Values
if "instantiated" not in st.session_state:

    # App type ('desktop' or 'cloud')
    st.session_state.app_type = "cloud"
    st.session_state.app_type = "desktop"
    
    st.session_state.app_config = {
        'cloud': {
            'msg_infile': 'Upload'
        },
        'desktop': {
            'msg_infile': 'Select'
        }
    }

    # Flag to keep state for panels
    st.session_state.flags_plotsmri = {
        'panel_wdir_open': False,
        'panel_ddir_open': False,
        'dset': False
    }

    # Dictionary with plot info
    st.session_state.plots = pd.DataFrame(
        columns=["pid", "xvar", "yvar", "hvar", "hvals", "trend", "lowess_s", "centtype"]
    )
    st.session_state.plot_index = 1
    st.session_state.plot_active = ""

    # Study name
    st.session_state.dset = ""

    # Flags for various i/o
    st.session_state.icon_thumb = {
        False: ':material/thumb_down:',
        True: ':material/thumb_up:'
    }

    # Flags for various i/o
    st.session_state.flags = {
        'dset': False,        
        'dir_out': False,
        'dir_dicom': False,
        'dicom_series': False,
        'dir_nifti': False,
        'dir_t1': False,
        'dir_dlmuse': False,
        'csv_dlmuse': False,
        'csv_demog': False,
        'csv_dlmuse+demog': False,
        'dir_download': False,
        'csv_mlscores': False,
        'csv_plot': False,
    }

    # Predefined paths for different tasks in the final results
    # The path structure allows nested folders with two levels
    # This should be good enough to keep results organized
    st.session_state.dict_paths = {
        "lists": ["", "Lists"],
        "dicom": ["", "Dicoms"],
        "nifti": ["", "Nifti"],
        "T1": ["Nifti", "T1"],
        "T2": ["Nifti", "T2"],
        "FL": ["Nifti", "FL"],
        "DTI": ["Nifti", "DTI"],
        "fMRI": ["Nifti", "fMRI"],
        "dlmuse": ["", "DLMUSE"],
        "mlscores": ["", "MLScores"],
        "plots": ["", "Plots"],
        "download": ["", "Download"],
    }

    # Paths to input/output files/folders
    st.session_state.paths = {
        "root": "",
        "init": "",
        "last_in_dir": "",
        "target_dir": "",
        "target_file": "",
        "dset": "",
        "dir_out": "",
        "lists": "",
        "dicom": "",
        "nifti": "",
        "user_dicom": "",
        "T1": "",
        "user_T1": "",
        "T2": "",
        "FL": "",
        "DTI": "",
        "fMRI": "",
        "dlmuse": "",
        "mlscores": "",
        "download": "",
        "plots": "",
        "sel_img": "",
        "sel_seg": "",
        "csv_demog": "",
        "csv_dlmuse": "",
        "csv_plot": "",
        "csv_roidict": "",
        "csv_mlscores": "",
    }

    # Flags to hide/show panels
    st.session_state.panel_visible = {
        'working_dir': False,
        'plot_in_data': False
    }

    # Flags to keep updates in user input/output
    st.session_state.is_updated = {
        "csv_plot": False,
    }
        
    # Paths for output
    st.session_state.paths["root"] = os.path.dirname(os.path.dirname(os.getcwd()))
    st.session_state.paths["init"] = st.session_state.paths["root"]

    #########################################
    # FIXME : set to test folder outside repo
    st.session_state.paths["init"] = os.path.join(
        os.path.dirname(st.session_state.paths["root"]), "TestData"
    )

    st.session_state.paths["last_in_dir"] = st.session_state.paths["init"]

    # FIXME: This sets the default out path to a folder inside the root folder for now
    st.session_state.paths["dir_out"] = os.path.join(
        st.session_state.paths["root"],
        "output_folder"
    )
    if not os.path.exists(st.session_state.paths["dir_out"]):
        os.makedirs(st.session_state.paths["dir_out"])
        
    #########################################

    # Image modalities
    st.session_state.list_mods = ["T1", "T2", "FL", "DTI", "fMRI"]

    # Dictionaries
    res_dir = os.path.join(st.session_state.paths["root"], "resources")
    st.session_state.dicts = {
        "muse_derived": os.path.join(res_dir, "MUSE", "list_MUSE_mapping_derived.csv"),
        "muse_all": os.path.join(res_dir, "MUSE", "list_MUSE_all.csv"),
        # "muse_sel": os.path.join(res_dir, "MUSE", "list_MUSE_primary.csv"),
        "muse_sel": os.path.join(res_dir, "MUSE", "list_MUSE_all.csv"),
    }
    st.session_state.dict_categories = os.path.join(
        res_dir,
        'dictionaries',
        'var_categories',
        'dict_var_categories.json'
    )

    # Current roi dictionary
    st.session_state.roi_dict = None
    st.session_state.roi_dict_rev = None

    # Input image vars
    st.session_state.list_input_nifti = []

    # Dicom vars
    st.session_state.list_series = []
    st.session_state.num_dicom_scans = []
    st.session_state.df_dicoms = pd.DataFrame()
    st.session_state.sel_series = []
    st.session_state.sel_mod = "T1"

    # Default number of plots in a row
    st.session_state.plotvars = {
        'max_plots_per_row': 5,
        'plots_per_row': 2,
    }
    st.session_state.max_plots_per_row = 5      ## FIXME will be redundant
    st.session_state.plots_per_row = 2          ## FIXME will be redundant

    st.session_state.plot_init_height = 500
    st.session_state.plot_height_coeff = 100
    st.session_state.plot_active = ""

    # Image suffixes
    st.session_state.suff_t1img = "_T1.nii.gz"
    st.session_state.suff_seg = "_T1_DLMUSE.nii.gz"

    st.session_state.df_plot = pd.DataFrame()

    # Variables for page plot_smri
    st.session_state.page_plotsmri = {
        'df' : pd.DataFrame(),
        'xvar' : None,
        'yvar' : None,
        'hvar' : None,
        'trend_types' : ['None', 'Linear', 'Smooth LOWESS Curve'],
        'trend' : 'None',
        'centile_types' : ['None', 'CN-All', 'CN-M', 'CN-F'],
        'centile' : 'None'
    }

    st.session_state.trend_types = ["", "Linear", "Smooth LOWESS Curve"]
    st.session_state.cent_types = ["", "CN-All", "CN-F", "CN-M"]

    st.session_state.plot_xvar = ""
    st.session_state.plot_yvar = ""
    st.session_state.plot_hvar = ""
    st.session_state.plot_hvals = []
    st.session_state.plot_trend = ""
    st.session_state.lowess_s = 0.5
    st.session_state.plot_centtype = ""

    # MRID selected by user
    st.session_state.sel_mrid = ""
    st.session_state.sel_roi = ""

    # Variable selected by user
    st.session_state.sel_var = ""

    # Variables selected by userroi_dict
    st.session_state.plot_sel_vars = []

    # Debugging variables
    st.session_state.debug_show_state = False
    st.session_state.debug_show_paths = False
    st.session_state.debug_show_flags = False

    # Viewing variables


    st.session_state.instantiated = True

st.sidebar.image("../resources/nichart1.png")

st.write("# Welcome to NiChart Project!")

st.sidebar.info(
    """
                    Note: This website is based on materials from the [NiChart Project](https://neuroimagingchart.com/).
                    The content and the logo of NiChart are intellectual property of [CBICA](https://www.med.upenn.edu/cbica/).
                    Make sure that you read the [licence](https://github.com/CBICA/NiChart_Project/blob/main/LICENSE).
                    """
)

with st.sidebar.expander("Acknowledgments"):
    st.markdown(
        """
                The CBICA Dev team
                """
    )

st.sidebar.success("Select a task above")

with st.sidebar.expander('Flags'):

    if st.checkbox("Show paths?", value=True):
        st.session_state.debug_show_paths = True
    else:
        st.session_state.debug_show_paths = False

    if st.checkbox("Show flags?", value=True):
        st.session_state.debug_show_flags = True
    else:
        st.session_state.debug_show_flags = False

    if st.checkbox("Show all session state vars?", value=True):
        st.session_state.debug_show_state = True
    else:
        st.session_state.debug_show_state = False

    if st.checkbox("Switch to cloud?"):
        st.session_state.app_type = 'cloud'
    else:
        st.session_state.app_type = 'desktop'

st.markdown(
    """
    NiChart is an open-source framework built specifically for
    deriving Machine Learning based indices from MRI data.

    **👈 Select a task from the sidebar** to process, analyze and visualize your data!

    ### Want to learn more?
    - Check out [NiChart Web page](https://neuroimagingchart.com)
    - Visit [NiChart GitHub](https://github.com/CBICA/NiChart_Project)
    - Jump into our [documentation](https://github.com/CBICA/NiChart_Project)
    - Ask a question in our [community
        forums](https://github.com/CBICA/NiChart_Project)
        """
)

st.markdown(
    """
            You can try NiChart manually via our github
            ```bash
            git clone https://github.com/CBICA/NiChart_Project
            git submodule update --init --recursive --remote
            pip install -r requirements.txt
            ```

            And to run the workflows, just run:
            ```bash
            python3 run.py --dir_input input folder --dir_output output_folder --studies 1 --version my_version --cores 4 --conda 0
            ```

            You can always find more options at our documentation
            """
)

if st.session_state.debug_show_state:
    with st.expander("DEBUG: Session state - all variables"):
        st.write(st.session_state)

if st.session_state.debug_show_paths:
    with st.expander("DEBUG: Session state - paths"):
        st.write(st.session_state.paths)

if st.session_state.debug_show_flags:
    with st.expander("DEBUG: Session state - flags"):
        st.write(st.session_state.flags)
