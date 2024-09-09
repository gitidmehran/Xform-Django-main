import json
import traceback
from mysql.connector import Error


def insert_new(cursor, root_word_id, morpheme_data):
    try:
        cursor.execute(f"SELECT id, sheet_reference, word FROM morphemes WHERE root_word_id = '{root_word_id}'")
        morphemes = cursor.fetchall()

        def get_id():
            for _sheet_word in morpheme_data['sheet_words']:
                # CHECKING QURANIC REFERENCES START
                reference = f"{_sheet_word['weight']}:{_sheet_word['morpheme_no']}:{_sheet_word['group']}:{_sheet_word['subgroup']}:{_sheet_word['word_number']}"
                for items in morphemes:
                    if reference in items[1] and _sheet_word['word'].strip() == items[2]:
                        return items[0]

        cursor.execute('''
            INSERT INTO morpheme_details_new (root_word_id, morpheme_id, morpheme_no, weight)
            VALUES (%s, %s, %s, %s)
        ''', (root_word_id, get_id(), morpheme_data['morpheme_no'], morpheme_data['weight']))

        morpheme_id = cursor.lastrowid  # Get the last inserted ID

        # Insert into Templates, Headings, and SubHeadings
        for sheet_word in morpheme_data['sheet_words']:
            # Skip insertion if word is "-", empty, only spaces, or an integer
            word_value = str(sheet_word['word']).strip()
            template_key_ = str(sheet_word['template']).strip()
            if word_value in ["-", "", "0"] or word_value.isdigit() or template_key_ in ["-", "", "0"] or template_key_.isdigit():
                continue

            # Determine whether it's a main word or a broken plural
            is_broken_plural = sheet_word.get('isbroken', False)

            # Insert or retrieve Template ID
            template_key = sheet_word['template']
            cursor.execute("SELECT id, template_text FROM templates WHERE template_text = %s", (template_key,))
            template = cursor.fetchall()
            if not template:
                cursor.execute('''
                    INSERT INTO templates (template_text, is_broken_plural)
                    VALUES (%s, %s)
                ''', (template_key, is_broken_plural))
                # pickled_data['template_ids'][template_key] = cursor.lastrowid  # Get the last inserted ID
                template_id = cursor.lastrowid # Get the last inserted ID
            else:
                template_id = template[0][0]

            # Insert or retrieve Heading ID
            heading_key = (sheet_word['ar'], sheet_word['en'])
            cursor.execute("SELECT * FROM headings WHERE ar = %s AND en = %s", (sheet_word['ar'], sheet_word['en']))
            heading = cursor.fetchall()
            if not heading:
                cursor.execute('''
                    INSERT INTO headings (ar, en)
                    VALUES (%s, %s)
                ''', heading_key)
                # pickled_data['heading_ids'][heading_key] = cursor.lastrowid  # Get the last inserted ID
                heading_id = cursor.lastrowid  # Get the last inserted ID
            else:
                heading_id = heading[0][0]

            # Insert or retrieve SubHeading ID
            subheading_key = (sheet_word['sub_ar'], sheet_word['sub_en'])
            cursor.execute("SELECT * FROM subheadings WHERE sub_ar = %s AND sub_en = %s", (sheet_word['sub_ar'], sheet_word['sub_en']))
            SubHeading = cursor.fetchall()
            if not SubHeading:
                cursor.execute('''
                    INSERT INTO subheadings (sub_ar, sub_en)
                    VALUES (%s, %s)
                ''', subheading_key)
                # pickled_data['subheading_ids'][subheading_key] = cursor.lastrowid  # Get the last inserted ID
                subheading_id = cursor.lastrowid  # Get the last inserted ID
            else:
                subheading_id = SubHeading[0][0]

            mrf_id = None
            # CHECKING QURANIC REFERENCES START
            reference = f"{sheet_word['weight']}:{sheet_word['morpheme_no']}:{sheet_word['group']}:{sheet_word['subgroup']}:{sheet_word['word_number']}"
            for items in morphemes:
                if reference in items[1] and sheet_word['word'].strip() == items[2]:
                    mrf_id = items[0]
                    break

            # Insert into Words
            cursor.execute('''
                INSERT INTO words (morpheme_id, morpheme_detail_id, template_id, heading_id, subheading_id,
                                morpheme_no, weight, word, `group`, subgroup,
                                word_number, isbroken)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (mrf_id, morpheme_id, template_id, heading_id, subheading_id,
                sheet_word['morpheme_no'], sheet_word['weight'], sheet_word['word'],
                sheet_word['group'], sheet_word['subgroup'], sheet_word['word_number'],
                is_broken_plural))

            word_id = cursor.lastrowid  # Get the last inserted ID

            # Insert into BrokenPlurals (if it's a broken plural)
            if is_broken_plural:
                # Insert or retrieve Template ID
                broken_plurals = sheet_word.get('broken_plurals', {})

                if broken_plurals != '':
                    broken_plural_template_key = broken_plurals['template']
                    cursor.execute("SELECT * FROM broken_plural_templates WHERE template_text = %s", (broken_plural_template_key,))
                    broken_plural_template = cursor.fetchall()
                    if not broken_plural_template:
                        cursor.execute('''
                            INSERT INTO broken_plural_templates (template_text)
                            VALUES (%s)
                        ''', (broken_plural_template_key,))
                        
                        # pickled_data['broken_template_ids'][broken_plural_template_key] = cursor.lastrowid  # Get the last inserted ID
                        _broken_plural_id = cursor.lastrowid  # Get the last inserted ID
                    else:
                        _broken_plural_id = broken_plural_template[0][0]

                    # reference_string = ', '.join(broken_plurals.get('references', []))
                    reference_string = json.dumps(broken_plurals.get('references', []))
                    cursor.execute('''
                        INSERT INTO brokenplurals (base_word_id, template_id, word, reference)
                        VALUES (%s, %s, %s, %s)
                    ''', (word_id, _broken_plural_id, broken_plurals['word'], reference_string))
          
                    broken_plural_id = cursor.lastrowid

                    # Insert into WordBrokenPlural
                    cursor.execute('''
                        INSERT INTO wordbrokenplural (word_id, broken_plural_id)
                        VALUES (%s, %s)
                    ''', (word_id, broken_plural_id))

        # Return a success message
        return {'status': 'success', 'message': 'Data successfully inserted.'}

    except Error as e:
        traceback.print_exc()
        return {'status': 'error', 'message': f'MySQL Error: {str(e)}'}
    except Exception as e:
        traceback.print_exc()
        return {'status': 'error', 'message': f'An error occurred: {str(e)}'}
