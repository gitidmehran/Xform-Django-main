from collections import OrderedDict
from .missing import has_missing_hyphens_or_two_segment_value
def get_headers( data_frame, file_name ):

    # data = re.split(r'\r?\n', data_frame.to_csv(index=False))
    data_frame.replace('\n', '', regex=True, inplace=True)
    
    data = data_frame.to_csv(index=False).split('\n')
    print('======get_headers Data start============')
    print(data)
    
    print('======get_headers Data end==============')
    references = data[1].split(',')
    print('======references Data start============')
    print(references)
    print('======references Data end==============')
    print('======file_name start==================')
    print(file_name)
    print('======file_name end====================')
    if has_missing_hyphens_or_two_segment_value( references, file_name ): 
        return False
    ar_headers = data[2].split(',')
    print('======ar_headers start============')
    print(ar_headers)
    print('======ar_headers end==============')
    en_headers = data[3].split(',')
    print('======en_headers start============')
    print(en_headers)
    print('======en_headers end==============')
    sub_ar_headers = data[4].split(',')
    print('======sub_ar_headers start============')
    print(sub_ar_headers)
    print('======sub_ar_headers end==============')
    sub_en_headers = data[5].split(',')
    print('======sub_en_headers start============')
    print(sub_en_headers)
    print('======sub_en_headers end==============')
    check = data[6].split(',')
    ar_level_3 = data[8].split(',')
    en_level_3 = data[9].split(',')
    sub_ar = ''
    sub_en = ''
    temp = OrderedDict()
    for i, ref in enumerate(references):
        if not ref == '-':
            ar = ar_headers[i] if not ar_headers[i] == '-' else ar
            en = en_headers[i] if not en_headers[i] == '-' else en
            c = check[i] if not check[i] == '-' else c

            sub_ar = sub_ar_headers[i] if not sub_ar_headers[i] == '-' else sub_ar  # Assign ar when hyphen occurs
            sub_en = sub_en_headers[i] if not sub_en_headers[i] == '-' else sub_en  # Assign en when hyphen occurs

            if c.strip() == 'Broken':
                sub_ar = ar_level_3[i] if not ar_level_3[i] == '-' else sub_ar
                sub_en = en_level_3[i] if not en_level_3[i] == '-' else sub_en
                # sub_en = sub_en_headers[i] if not sub_en_headers[i] == '-' else sub_en
            temp.update({
                ref: [ar.strip(), en.strip(), sub_ar.strip(), sub_en.strip(), False if not c.strip() == 'Broken' else True]
            })

    
    # values_to_remove = ['-']

    # new_list = [x.strip() for x in data if x not in values_to_remove]

    return temp