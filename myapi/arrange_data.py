import pandas as pd
from .broken_plural_by_group_name import arrange_broken
from .extract_headers import get_headers
from .message_box import show_popup_message

def arrange_data( file ):
    try:
        excel_file = file # "Word-Xforms-samawa-V-1.29.xlsx"
        file_name = excel_file.split('/')[-1]
        data_frame = pd.read_excel(excel_file, sheet_name='Main').fillna('-')
        data_frame = data_frame.iloc[:, 4:-3]
        # headers = data_frame[3:12].to_csv(index=False).split('\r\n')[6]

        headers = get_headers(data_frame[3:12], file_name)

        if not headers:
            print(f'There are missing hyphens or two-segment values. See "log_files/{file_name}_check in database" for details.')
            return False
        data_frame_result = pd.read_excel(excel_file, sheet_name='Result').fillna('-')
        # print('======data_frame_result start============')
        # print(data_frame_result)
        # print('======data_frame_result end==============')
        # print(data_frame_result)
        # Drop the first column
        data_frame_result = data_frame_result.drop( data_frame_result.iloc[:, 5:] , axis=1)
       
        # Assuming you have a DataFrame named "dataframe" and you want to rename columns
        data_frame_result.rename(columns={'Unnamed: 0': 'reference','Unnamed: 1': 'root_word_id', 'Unnamed: 2': 'root_word', 'Unnamed: 3': 'word', 'Unnamed: 4': 'word_ids'}, inplace=True)

        # word_numbers
        word_numbers = data_frame[3:4].to_csv(header=False).replace(",-", "")

        d = word_numbers.strip()
        word_number_lines = d.split(',')

        word_number_lines.pop(0)

        broken_plurals = arrange_broken( data_frame[3:12] )
        print('======broken_plurals start============')
        print(broken_plurals)
        print('======broken_plurals end==============')
        form1  = data_frame.iloc[13:28].values
        print('======form1 start============')
        print(form1)
        print('======form1 end==============')
        form2  = data_frame.iloc[31:46].values # plus 3 - rows, plus 15 - rows
        print('======form2 start============')
        print(form2)
        print('======form2 end==============')
        form3  = data_frame.iloc[49:64].values # plus 3 - rows, plus 15 - rows
        print('======form2 start============')
        print(form3)
        print('======form2 end==============')
        form4  = data_frame.iloc[67:82].values # plus 3 - rows, plus 15 - rows
        print('======form4 start============')
        print(form4)
        print('======form4 end==============')
        form5  = data_frame.iloc[85:100].values # plus 3 - rows, plus 15 - rows
        print('======form5 start============')
        print(form5)
        print('======form5 end==============')
        form6  = data_frame.iloc[103:118].values # plus 3 - rows, plus 15 - rows
        print('======form6 start============')
        print(form6)
        print('======form6 end==============')
        form7  = data_frame.iloc[121:136].values # plus 3 - rows, plus 15 - rows
        print('======form7 start============')
        print(form7)
        print('======form7 end==============')
        form8  = data_frame.iloc[139:154].values # plus 3 - rows, plus 15 - rows
        print('======form8 start============')
        print(form8)
        print('======form8 end==============')
        form9  = data_frame.iloc[157:172].values # plus 3 - rows, plus 15 - rows
        print('======form9 start============')
        print(form9)
        print('======form9 end==============')
        form10 = data_frame.iloc[175:190].values # plus 3 - rows, plus 15 - rows
        print('======form10 start============')
        print(form10)
        print('======form10 end==============')
        broken_plural = data_frame.iloc[12:13].values
        forms = [[*broken_plural, *form1], form2, form3, form4, form5, form6, form7, form8, form9, form10]

        return [ forms, broken_plurals, headers, word_numbers, word_number_lines, data_frame_result[31:] ]
    except:
        return False