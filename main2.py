import logging
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import extract_pages

logging.basicConfig(level=logging.INFO)

def get_connection():
    try:
        tableau_server_auth = {
            'dev-environment': {
                'server': "https://<server-name>.com/",
                'api_version': "3.19",
                'personal_access_token_name': "api_test",
                'personal_access_token_secret': "TOKEN",
                'site_name': "",
                'site_url': "site"
            }
        }
        connection = TableauServerConnection(tableau_server_auth, env='dev-environment')
        connection.sign_in()
        logging.info('Connected to Tableau server')
        return connection
    except Exception as e:
        logging.error(f'Connection error: {e}')
        return None

def get_site(conn):
    try:
        all_sites = extract_pages(conn.query_sites)
        site_list = [(site['name'], site['id']) for site in all_sites]
        return site_list
    except Exception as e:
        logging.error(f'Error fetching sites: {e}')
        return []

def get_workbook(conn):
    try:
        all_wb = extract_pages(conn.query_workbooks_for_site)
        wb_list = [(wb['name'], wb['webpageUrl'], wb['owner']['name']) for wb in all_wb]
        logging.info(f'{len(wb_list)} workbooks found')
        return wb_list
    except Exception as e:
        logging.error(f'Error fetching workbooks: {e}')
        return []

def main():
    connection = get_connection()
    if connection:
        try:
            site_info = get_site(connection)
            workbook_info = get_workbook(connection)
            # Do something with site_info and workbook_info
        finally:
            connection.sign_out()
            logging.info('Signed out from Tableau server')

if __name__ == "__main__":
    main()
