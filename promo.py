### streamlit version == 0.89

# Import Apps to call them later
import promo_1
# import promo_2
# import promo_3
# import promo_x
import promo_x_copy
# Import other libraries
import streamlit as st
import hydralit_components as hc
import pandas as pd
from sqlalchemy import create_engine

def connection():
        #UPLOADING TO MYSQL DB
        client_cert = 'C:\\Users\\o.georgievskiy\\client-cert.pem'
        client_key = 'C:\\Users\\o.georgievskiy\\client-key.pem'
        server_ca = 'C:\\Users\\o.georgievskiy\\server-ca.pem'
        #Connection attributes
        db_data = 'mysql+mysqlconnector://' + 'root' + ':' + 'sA2gw3Fpkpe9sn35' + '@' + '34.89.188.155' + ':3306/' + 'promotions' + '?charset=utf8mb4' #pip install mysqlclient 
        connect_args={
                "ssl_ca":server_ca,
                "ssl_cert": client_cert,
                "ssl_key": client_key
            }
        #Create Connection
        engine = create_engine(db_data, connect_args = connect_args)

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def load_dwh():
    client_cert = 'C:\\Users\\o.georgievskiy\\client-cert.pem'
    client_key = 'C:\\Users\\o.georgievskiy\\client-key.pem'
    server_ca = 'C:\\Users\\o.georgievskiy\\server-ca.pem'
    #Connection attributes
    db_data = 'mysql+mysqlconnector://' + 'root' + ':' + 'sA2gw3Fpkpe9sn35' + '@' + '34.89.188.155' + ':3306/' + 'promotions' + '?charset=utf8mb4' #pip install mysqlclient 
    connect_args={
            "ssl_ca":server_ca,
            "ssl_cert": client_cert,
            "ssl_key": client_key
        }
    #Create Connection
    engine = create_engine(db_data, connect_args = connect_args)
    #Read tables
    with engine.begin() as db_connection:
        ### One Option to extract is via sqlalchemy
        # metadata = sq.MetaData()
        # database = sq.Table('promodb', metadata, autoload=True, autoload_with=engine)  
        # selection = sq.select([database.columns.partner_name]) 
        # db_partner = db_connection.execute(selection).fetchall()
        querypar = "SELECT * from dim_partner"
        querypro = "SELECT * from dim_product"
        querysrp = "SELECT * from fact_basesrp"
        querydb = "SELECT * from promodb"
        dim_partner_ = pd.read_sql(querypar,db_connection)
        dim_product_ = pd.read_sql(querypro,db_connection)
        fact_basesrp_ = pd.read_sql(querysrp,db_connection)
        promodb_ = pd.read_sql(querydb,db_connection)
        return dim_partner_,dim_product_,fact_basesrp_,promodb_

def main():

    #region     hide_streamlit_style = """
    # 	<style>
    # 	/* This is to hide hamburger menu completely */ 3
    # 	#MainMenu {visibility: hidden;}
    # 	/* This is to hide Streamlit footer */
    # 	footer {visibility: hidden;}
    # 	/*
    # 	If you did not hide the hamburger menu completely,
    # 	you can use the following styles to control which items on the menu to hide.
    # 	*/
    # 	ul[data-testid=main-menu-list] > li:nth-of-type(4), /* Documentation */
    # 	ul[data-testid=main-menu-list] > li:nth-of-type(5), /* Ask a question */
    # 	ul[data-testid=main-menu-list] > li:nth-of-type(6), /* Report a bug */
    # 	ul[data-testid=main-menu-list] > li:nth-of-type(7), /* Streamlit for Teams */
    # 	ul[data-testid=main-menu-list] > div:nth-of-type(2) /* 2nd divider */
    # 		{display: none;}
    # 	</style>
    # """
    #     st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    #endregion
        
    st.set_page_config(
        page_title = "Promo Tracker DB",
        page_icon = "🧊",
        layout="wide",
        initial_sidebar_state = "collapsed")
    hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
    st.markdown(hide_footer_style, unsafe_allow_html=True)

    dim_partner, dim_product,fact_basesrp, promodb = load_dwh()


    #First screen with App/Page selection
    PAGES = {
    #"Log": promo_0,
    "New Promo": promo_1,
    "New Promo X": promo_x_copy,
    # "Promo Overview": promo_2,
    # "Promo DB": promo_3
    }

    st.info('Hello! This is an app to handle and view Promos!')
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", options = list(PAGES.keys()))
    page = PAGES[selection]


    st.sidebar1 = st.sidebar.empty()
    st.sidebar2 = st.sidebar.empty()
    st.sidebar3 = st.sidebar.empty()
    st.sidebar4 = st.sidebar.empty()
    st.sidebar5 = st.sidebar.empty()
    st.sidebar6 = st.sidebar.empty()

    pams = (
        "Raquel",  #Microsoft
        "Lorenzo", #EPIC
        "Simone",
        "Kenji")   #PSN, Nintendo)
    st.sidebar.selectbox("Added by", options = pams,key= 'sb_user')
    sb_user = st.session_state.sb_user
    
    sb_partner = st.sidebar2.selectbox("Partner", options = list(dim_partner.name),key = 'sb_partner')

        # ['dwh_id_dlproduct',
        #  'product_id',
        #  'dwh_id_dlpartner',
        #  'dwh_id_product',
        #  'product_name',
        #  'title_id',
        #  'title_name',
        #  'content_type',
        #  'platform',
        #  'product_release_date',
        #  'publisher',
        #  'ips_project_code',
        #  'ips_project_title',
        #  'ips_project_label']

    #FIND how to use numerical values insteead of applying new column 
    #dim_product.join(dim_partner["name"]).rename(columns = {"name":"partner_name"})

    #FIND and add Partner Name based on its id of another df
    dim_product["partner_name"] = dim_product.apply(lambda x: dim_partner[(dim_partner.dwh_id_dlpartner == x.dwh_id_dlpartner)].values[0][1], axis=1)
    
    sb_ts = st.sidebar3.selectbox("Franchise", options = list(dim_product.ips_project_title[(dim_product.partner_name.isin([sb_partner]))].unique()),key = 'sb_ts', index = 1)
    sb_new = st.sidebar4.checkbox("Add New Title", key = 'sb_new', value = False)
    copy_promo = st.sidebar5.checkbox("Copy Promo Campaign", key = 'copy_promo', value = False)

    if page == promo_1:
        df = page.app(promodb,dim_partner, dim_product,fact_basesrp)
        csv = convert_df(df)
        st.download_button(
         label="Download data as CSV",
         data=csv,
         file_name='large_df.csv',
         mime='text/csv',
     )
    elif page == promo_x_copy:
        df = page.app(promodb,dim_partner, dim_product,fact_basesrp)
    
    return print(type(df))
# OTHER PAGES
    # elif page == promo_2: 
    #     page.app(data_df_promo,dfs_dwh)
    # elif page == promo_3:
    #     page.app(data_df_promo,dfs_dwh)

#FUNCTIONS
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def quer(columns,values):
    qry = ""
    s = 0
    for x, v in zip(columns,values):
        if s != len(columns)-1:
            qry = qry + x + ' == ' + '"'+str(v)+'"' +' & '
        else:
            qry = qry + x + ' == ' +'"'+ str(v)+'"'
        s+=1
    return (qry)

if __name__ == '__main__':
    main()
