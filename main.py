from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import extract_pages


def get_connection():
    # set credentials to log in to your Tableau Server / Tableau Online. I'm using a personal token
    tableau_server_auth = {
            'dev-environment': {
                    'server': "https://<server-name>.com/",  # update for your server
                    'api_version': "3.19",                         # update for your version of the API
                    'personal_access_token_name': "api_test",      # update with your personal access token's name
                    'personal_access_token_secret': "TOKEN",  # update with your personal access token's secret
                    'site_name': "",                               # set it to '' if accessing your default site (this can be left empty)
                    'site_url': "site_name"            # set it to '' if accessing your default site (write just the name, no url)
            }
    }

    # log in to the server. If the connection was successful, we get 200 code
    try:
        connection = TableauServerConnection(tableau_server_auth, env='dev-environment')
        connection.sign_in()
        print('connected')
    except:
        print('connetion error')
    return connection

def get_site(conn=get_connection()):
    try:    
        all_sites = extract_pages(conn.query_sites)
        site_list = [(site['name'], site['id']) for site in all_sites]
        #print(site_list[:2])
        return site_list
    except:
        print('not able to download sites')
    finally:
        conn.sign_out()
        print('sign out')

def get_workbook(conn=get_connection()):
    try:    
        all_wb = extract_pages(conn.query_workbooks_for_site)
        #all_sites = extract_pages(conn.query_sites, starting_page=1, page_size=200, limit=500)
        wb_list = [(
            wb['name'], 
            wb['webpageUrl'], 
            wb['owner']['name']) 
            for wb in all_wb
            ]
        #print(wb_list[:1]) #the result of this is in the output_example.py file
        print(len(wb_list))
        return wb_list
    except:
        print('not able to download workbooks')
    finally:
        conn.sign_out()
        print('sign out')
