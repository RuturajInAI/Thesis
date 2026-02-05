Weld Seam HMI (Streamlit)

What this app does
- Upload a weld list as CSV
- Edit and review welds
- Focus on a part to implicitly prioritize weld review
- View part connectivity graph
- Validate and export CSV or JSON

How to run
1) Install dependencies
   pip install -r requirements.txt

2) Start Streamlit
   streamlit run app.py

CSV minimum columns
- Weld Index
- Part A
- Part B

Optional columns
- Weld Type, Weld Side, Weld Size, Weld Length, Weld Reference
- Source, Confidence, Status, Notes
