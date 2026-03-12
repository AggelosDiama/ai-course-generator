import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
        
        html {
            scroll-behavior: smooth;
        }
                
        /* Sidebar Metric Styling */
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
            color: #3211d4 !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        
        /* Progress Bar Color */
        .stProgress > div > div > div > div {
            background-color: #3211d4 !important;
        }

        /* Roadmap Link Styling */
        .roadmap-link {
            text-decoration: none !important;
            color: #475569 !important;
            display: block;
            padding: 4px 8px;
            border-radius: 4px;
            transition: 0.2s;
        }
        
        .roadmap-link:hover {
            background-color: #3211d415 !important;
            color: #3211d4 !important;
        }

        .roadmap-module {
            font-weight: bold;
            margin-top: 10px;
        }

        /* Offset for scrolling so the title isn't tucked under the top margin */
        h2, h3 {
            scroll-margin-top: 2rem;
        }
                
        html { scroll-behavior: smooth; }
        .stApp { background-color: #f6f6f8; font-family: 'Lexend', sans-serif; }
        
        /* Container styling */
        .st-key-container {
            background-color: white; border-radius: 16px !important; border: 1px solid #f1f5f9 !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important; padding: 2rem !important;
        }
                
        [data-testid="stSidebar"] hr {
        margin-top: 0.5rem !important;
        margin-bottom: 2rem !important;
        padding-top: 0px !important;
        padding-bottom: 10px !important;
        }
        
        /* Also reduce space between container elements in sidebar */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }

        /* Buttons */
        .st-key-primary-btn button {
            background-color: #3211d4 !important; color: white !important; font-weight: 600 !important;
            height: 3.5em !important; border-radius: 12px !important; border: none !important;
        }

        /* Roadmap Sidebar Links */
        .roadmap-link {
            text-decoration: none !important;
            color: #475569 !important;
            display: block;
            padding: 8px 12px;
            margin: 2px 0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        .roadmap-link:hover {
            background-color: rgba(50, 17, 212, 0.08) !important;
            color: #3211d4 !important;
            padding-left: 18px;
        }
        .roadmap-module { font-weight: 600; margin-top: 10px; color: #1e293b !important; }
        </style>
    """, unsafe_allow_html=True)