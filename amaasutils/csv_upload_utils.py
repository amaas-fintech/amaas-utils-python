import csv
from datetime import date, datetime
from dateutil.parser import parse
from decimal import Decimal


#lists to dicide which a particular class belong to
ASSET = ['Asset', 'Automobile', 'BondFutureOption', 'BondFuture', 'BondOption', 'Bond', 'ContractForDifference', 'Currency', 'CustomAsset', 
         'Derivative', 'EnergyFuture', 'EquityFuture', 'Equity', 'ExchangeTradedFund', 'ForeignExchange', 'Fund', 'FutureOption', 'Future'
         'ForeignExchangeOption', 'IndexFuture', 'Index', 'InterestRateFuture', 'ListedContractForDifference', 'ListedDerivative'
         'OptionMixin', 'RealAsset', 'RealEstate', 'Sukuk', 'SyntheticFromBook', 'SyntheticMultiLeg', 'Synthetic', 'Warrant', 'Wine']
PARTY = ['Broker', 'Company', 'Exchange', 'Fund', 'GovernmentAgency', 'Individual', 'Organisation', 'Party', 'SubFund']
BOOK = ['Book']
CORPORATE_ACTION = ['CorporateAction', 'Dividend', 'Notification', 'Split']
MARKET_DATA = ['EODPrice', 'FXRate', 'Quote']
TRANSACTION = ['Transaction']
ASSET_MANAGER = ['AssetManager', 'Relationship']
#children_class dictionary director for different classes
#chiildren fields names that signal children fields
CHILDREN_SIGNAL = {'references', 'addresses', 'emails', 'comments', 'charges', 'codes', 'parties'}
#parameters datatypes:
INTEGER_PARAMS = {'internal_id', 'client_id', 'asset_manager_id', 'version',
                  'default_book_owner_id', 'related_id', 'quantity',
                  'valid_to_id', 'charge_value', 'price', 'gross_settlement',
                  'net_settlement', }
STRING_PARAMS = {'asset_id', 'asset_status', 'asset_class', 'asset_type', 'asset_issuer_id',
                 'country_id', 'venue_id', 'currency', 'display_name', 'description',
                 'created_by', 'updated_by', 'reference_type', 'reference_value',
                 'link_type', 'linked_asset_id', 'comment_type', 'comment_value',
                 'party_id', 'party_status', 'party_class', 'party_type', 'base_currency',
                 'legal_name', 'url', 'address_type', 'line_one', 'line_two',
                 'city', 'region', 'postal_code', 'comment_type', 'comment_value',
                 'email_primary', 'email_type', 'email', 'linked_party_id',
                 'asset_manager_type', 'asset_manager_status', 'dafault_timezone',
                 'account_type', 'relationship_id', 'relationship_type',
                 'relationship_status', 'book_id', 'book_status', 'book_type',
                 'business_unit', 'timezone', 'owner_id', 'corporate_action_id',
                 'corporate_action_type', 'corporate_action_status',
                 'message', 'accounting_type', 'item_id', 'item_status',
                 'item_category', 'details', 'charge_type', 'transaction_id',
                 'code_type', 'code_value', 'linked_transaction_id',
                 'reason', 'transaction_status', 'asset_book_id', 'counterparty_book_id',
                 'transaction_action', 'transaction_type', 'transaction_currency',
                 'settlement_currency'}
BOOLEAN_PARAMS = {'fungible', 'roll_price', 'active', 'address_primary', 'elective',
                  'net_affecting', 'lifecycle'}
DATE_PARAMS = {'issue_date', 'maturity_date', 'declared_date', 'record_date', 'settlement_date',
               'posting_date', 'posting_type', 'transaction_date', 'settlement_date'}
DATETIME_PARAMS = {'created_time', 'updated_time', 'default_book_close_time', 'close_time',
                   'valid_from', 'valid_to', 'execution_time'}
JSON_PARAMS = {'additional', 'client_additional'}

def formatted_string_to_links(links_input, clazz):
    """
    Example formatted string ::
    '{link_1:[{linked_asset_id:12345},{linked_asset_id:54321,active:true}],link_2:[{linked_asset_id:12365}]}'
    string of "true" will be converted to True string of "false" will be converted to False (Python Boolean)
    """
    links_dict = dict()
    key = ''
    if links_input!= '' and (links_input).split('{', 1)[1] != '':
        links_input = links_input.split('{', 1)[1]
        key=links_input.split(':',1)[0]
        links_input = links_input.split(':',1)[1]
    link_set = set()
    value = links_input.split(']',1)[0][1:]
    if (len(links_input.split('}',1)) != 1):
        links_input = links_input.split(']',1)[1]
    while(key!=''):
        params_dict = dict()
        temp = value.split('}', 1)[0]
        value = value.split('}', 1)[1]
        while (temp[0] in [',', '{']):
            temp = temp[1:]
        temp_list = temp.split(',')
        for field in temp_list:
            params_dict.update(process_field(field))
        link_set.add(clazz(**params_dict))
        params_dict = dict()
        while(value!= '' and value[0:2] == ',{'):
            temp = value.split('}', 1)[0]
            value = value.split('}', 1)[1]
            while (temp[0] in [',', '{']):
                temp = temp[1:]
            temp_list = temp.split(',')
            for field in temp_list:
                params_dict.update(process_field(field))
            link_set.add(clazz(**params_dict))
            params_dict = dict()
        links_dict[key] = link_set
        if (links_input[0] == ','):
            links_input = links_input[1:]
        else:
            break
        link_set = []
        key = links_input.split(':', 1)[0]
        value = links_input.split(':', 1)[1].split(']', 1)[0][1:]
        links_input = links_input.split(':', 1)[1].split(']', 1)[1]        
    return links_dict

def formatted_string_to_others(typi_input, clazz):
    """
    Example formatted string that is passed in from above::
    '{address_1:{line_one:12345,city:Singapore,country_id:SGD,address_primary:123,line_two:6789,active:true}}',
    '{comment_1:{comment_value:1,active:true},comment_2:{comment_value:2,active:false}}',
    '{email_1:{email:1@1.com,email_primary:true,active:true},email_2:{email:2@2.com,email_primary:false}}',
    '{reference_1:{reference_value:1,active:true},reference_2:{reference_value:2}}'
    '{charge_1:{charge_value:10,currency:SGD,active:true},charge_2:{charge_value:1,currency:SGD}}'
    '{code_1:{code_value:1,active:true},code_2:{code_value:2}}'
    '{comment_1:{comment_value:1,active:true},comment_2:{comment_value:2}}'
    '{party_1:{party_id:1,active:true},party_2:{party_id:2,active:false}}'
    string of "true" will be converted to True, string of "false" will be converted to False (Python Boolean)
    """
    typi_dict = dict()
    while (typi_input != '}' and typi_input != ''):
        params_dict = dict()
        temp = typi_input.split('}', 1)[0]
        while (temp[0] in [',', '{']):
            temp = temp[1:]
        key = temp.split(':', 1)[0]
        temp = temp.split(':', 1)[1]
        while (temp[0] in [',', '{']):
            temp = temp[1:]
        temp_list = temp.split(',')
        for field in temp_list:
            params_dict.update(process_field(field))
        typi_dict[key] = clazz(**params_dict)
        if len(typi_input.split('}', 1))==2:
            typi_input = typi_input.split('}', 1)[1]
        else:
            typi_input = ''
    return typi_dict

def process_header(header_str):
    """helper method - assuming the children fields headers are seperated by dot"""
    if not children_signal(header_str):
        return header_str
    naive_split = header_str.split('.')
    return naive_split

def process_value(value_str):
    """
    naive version of processing the values: leave the work for constructors
    process the value to check exotic value inputs
    true or false should be converted to python boolean values
    empty strings should be converted to None because it is undefined
    """
    #check for boolean
    if value_str == 'true' or value_str == 'True':
        return True
    elif value_str == 'false' or value_str == 'False':
        return False
    #check for None (undefined types)
    elif value_str == '':
        return None
    else:
        return value_str

def process_value_with_header(header_str, value_str):
    """
    This function processes the value field of each key,value pair
    By datatype implied by the key, from the class DB construction
    """
    if header_str in INTEGER_PARAMS:
        return int(value_str)
    elif header_str in BOOLEAN_PARAMS:
        if value_str == 'true' or value_str == 'True':
            return True
        else:
            return False
    elif header_str in DATE_PARAMS:
        return parse(value_str).date()
    elif header_str in DATETIME_PARAMS:
        return datetime.strptime(value_str)
    else:
        return value_str

def process_field(field_str):
    """This function deals with particular fields that contain key value pairs seperated by ':'"""
    params_update_dict = dict()
    field_key = field_str.split(':')[0]
    field_value = field_str.split(':')[1]
    params_update_dict[field_key] = process_value_with_header(field_key, field_value)
    return params_update_dict

def children_signal(header_str):
    """Check whether the string is signalling the field is a children feild"""
    if '.' in header_str:
        return True
    return False

def group_raw_to_formatted_string_dict(raw_dict):
    """
    This method can convert the children fields value by grouping them 
    And convert to formatted string internally decided
    """
    cooked_dict = dict()
    last_header_first = last_header_second = None
    last_header_third = last_header_fourth = None
    for header, value in raw_dict.items():
        header = process_header(header)
        if isinstance(header, list):
            if len(header) == 4:
                if not cooked_dict.get('links', None):
                    cooked_dict['links']='{'
                cooking_value = cooked_dict['links']
                if header[1] in cooking_value:
                    cooking_str = cooking_value.split(header[1])[1].split(']', 1)[0]
                    if header[2] == last_header_third:
                        cooked_str = header[1]+cooking_str[0:-1]+','+header[3]+':'+value+'}]'
                    else:
                        addon_str = ',{'+header[3]+':'+value+'}'
                        cooked_str = header[1]+cooking_str+addon_str+']'
                    cooked_dict['links'] = cooking_value.split(header[1])[0]+cooked_str+cooking_value.split(header[1])[1].split(']', 1)[1]
                else:
                    addon_str = header[1]+':'+'[{'+header[3]+':'+value+'}]'
                    if cooking_value == '{':
                        cooked_dict['links'] = cooking_value+addon_str+'}'
                    else:
                        cooked_dict['links'] = cooking_value[0:-1]+addon_str+'}'
                last_header_first = header[0]
                last_header_second = header[1]
                last_header_third = header[2]
                last_header_fourth = header[3]
            else:
                if not cooked_dict.get(header[0], None):
                    cooked_dict[header[0]] = '{'
                cooking_value = cooked_dict[header[0]]
                if header[1] in cooking_value:
                    cooking_str = cooking_value.split(header[1])[1].split('}', 1)[0]
                    cooked_str = header[1]+cooking_str+','+header[2]+':'+value+'}'
                    cooked_dict[header[0]] = cooking_value.split(header[1])[0]+cooked_str+cooking_value.split(header[1])[1].split('}', 1)[1]
                else:
                    addon_str = header[1]+':{'+header[2]+':'+value+'}'
                    if len(addon_str) != 0:
                        addon_str = ','+addon_str
                    if cooking_value == '{':
                        cooked_dict[header[0]] = cooking_value+addon_str+'}'
                    else:
                        cooked_dict[header[0]] = cooking_value[0:-1]+addon_str+'}'
                last_header_first = header[0]
                last_header_second = header[1]
                last_header_third = header[2]
                last_header_fourth = None
        else:
            cooked_dict[header] = value
    return cooked_dict
