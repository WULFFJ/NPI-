import requests
import json
import pandas as pd

from flatten_json import flatten

#So you can see the full Pandas columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

#NPI URL
url=r"https://npiregistry.cms.hhs.gov/api/?"

#I listed taxonomies, states and zip codes in a csv file.  This will import them
statedocs=pd.read_csv(r"C:\Users\blah\Desktop\zip2.csv",dtype=str,sep=",")

This is a list of columns from the NPI database available.  Feel free to choose which you want.
column_names=['enumeration_type','number','last_updated_epoch','created_epoch','basic_first_name','basic_last_name','basic_middle_name','basic_credential','basic_sole_proprietor','basic_gender','basic_enumeration_date','basic_last_updated','basic_status','basic_name','other_names','addresses_0_country_code','addresses_0_country_name','addresses_0_address_purpose','addresses_0_address_type','addresses_0_address_1','addresses_0_address_2','addresses_0_city','addresses_0_state','addresses_0_postal_code','addresses_0_telephone_number','addresses_0_fax_number','addresses_1_country_code','addresses_1_country_name','addresses_1_address_purpose','addresses_1_address_type','addresses_1_address_1','addresses_1_address_2','addresses_1_city','addresses_1_state','addresses_1_postal_code','addresses_1_telephone_number','addresses_1_fax_number','taxonomies_0_code','taxonomies_0_desc','taxonomies_0_primary','taxonomies_0_state','taxonomies_0_license','taxonomies_1_code','taxonomies_1_desc','taxonomies_1_primary','taxonomies_1_state','taxonomies_1_license','other_names_0_code','other_names_0_type','other_names_0_last_name','other_names_0_first_name','other_names_0_middle_name','other_names_0_credential','identifiers','basic_name_prefix','taxonomies_2_code','taxonomies_2_desc','taxonomies_2_primary','taxonomies_2_state','taxonomies_2_license','taxonomies_3_code','taxonomies_3_desc','taxonomies_3_primary','taxonomies_3_state','taxonomies_3_license','taxonomies_4_code','taxonomies_4_desc','taxonomies_4_primary','taxonomies_4_state','taxonomies_4_license','basic_certification_date','basic_name_suffix','practiceLocations_0_address_type','practiceLocations_0_address_1','practiceLocations_0_address_2','practiceLocations_0_city','practiceLocations_0_state','practiceLocations_0_postal_code','practiceLocations_0_country_code','practiceLocations_0_country_name','practiceLocations_0_fax_number','practiceLocations_0_telephone_number','practiceLocations_0_update_date','practiceLocations_1_address_type','practiceLocations_1_address_1','practiceLocations_1_address_2','practiceLocations_1_city','practiceLocations_1_state','practiceLocations_1_postal_code','practiceLocations_1_country_code','practiceLocations_1_country_name','practiceLocations_1_fax_number','practiceLocations_1_telephone_number','practiceLocations_1_update_date','basic_organization_name','basic_organizational_subpart','basic_parent_organization_ein','basic_parent_organization_legal_business_name','basic_authorized_official_credential','basic_authorized_official_first_name','basic_authorized_official_last_name','basic_authorized_official_middle_name','basic_authorized_official_telephone_number','basic_authorized_official_title_or_position','basic_authorized_official_name_prefix','other_names_0_organization_name','taxonomies_5_code','taxonomies_5_desc','taxonomies_5_primary','taxonomies_5_state','taxonomies_5_license','taxonomies_6_code','taxonomies_6_desc','taxonomies_6_primary','taxonomies_6_state','taxonomies_6_license','taxonomies_7_code','taxonomies_7_desc','taxonomies_7_primary','taxonomies_7_state','taxonomies_7_license','practiceLocations_2_address_type','practiceLocations_2_address_1','practiceLocations_2_address_2','practiceLocations_2_city','practiceLocations_2_state','practiceLocations_2_postal_code','practiceLocations_2_country_code','practiceLocations_2_country_name','practiceLocations_2_telephone_number','practiceLocations_2_update_date']

#Set the DataFrame
ASC=pd.DataFrame(columns=column_names)

#This for loop allows you to loop through three columns at once to narroow your search.
for state,cod,tax in zip(statedocs['state_id'],statedocs['code'], statedocs['taxonomy']):   
        body=('enumeration_type=NPI-1&'
            'address_purpose=PRIMARY&'
            f'taxonomy_description={tax}&'
            f'state={state}&'
            'country_code=US&'
            f'postal_code={cod}&'
            'limit=200&'
            'version=2.1')

        reqs=requests.get(url,body)
        req=reqs.json()
        print(req)
        
        try:
            reqct=req['result_count']
        except:
            continue
            
        i = 0
        print(req['results'])
        while i < reqct:
            record = flatten(req['results'][i])
            print(record)
            data = pd.DataFrame.from_dict(record,orient='index').T

            i+=1
            ASC=ASC.append(data,ignore_index=False)
            del data

#Last we save to csv
ASC.to_csv(r"C:\blah\jwulff\Desktop\INOHDOCS1.csv")
