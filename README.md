# ccm_war
convergent cross mapping based on the ACLED data of the Russia-Ukraine War

This project is based on the acled data of the russia ukraine war this is a streamlit data 
The ccm model of skccm is used on the event_type and admin1 of the ACLED data :
so it shows the ccm relation like Battles@Belgorod vs Battles@Kherson and so on the code general shows the relation of first 100 
you can change it by changing this line .head() value --{ top_labels = df['event_label'].value_counts().head(100).index.tolist() }


For installation of packages use :
          pip install streamlit pandas numpy seaborn matplotlib pyEDM


Use streamlit gb.py to run the file 
the csv file is 200mb so i uploaded the zip file unzip and upload the file after running the python file. you have to upload directly in the streamlit page.
