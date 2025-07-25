import os
import sys
import PyPDF2
import difflib

def print_help():
    print('/? - print help')
    print('file1 - out text in [file1].txt ')
    print('file1 file2- out text in file2 ')
    print('-screen file1 - print text on screen')
    print('-compare file1 file2 - out in file compare.txt the difference')
    print('-compare_print file1 file2 - print screen the difference')

def screen_text(params):
    print(params[2])
    print(read_text_file(params[2]))

def save_file(output_file, text_file):
    with open(output_file, 'w', encoding='utf-8') as file_out:
        file_out.write(text_file)

def output_filename(params):
    if len(params) >= 3:
        output_file = params[2]
    else:
        basename, extensions = os.path.splitext(params[1])
        output_file = basename + '.txt'

    return output_file

def read_text_file(file):
    text_all = ''
    with open(file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            text_all += text + ('\n'*2)

    return text_all

def print_compare(params, screen):
    text1 = read_text_file(params[2]).strip().splitlines()
    text2 = read_text_file(params[3]).strip().splitlines()
    text_compare = ''
    for line in difflib.unified_diff(text1, text2, fromfile='file1', tofile='file2', lineterm='', n=0):
        for prefix in ('---', '+++', '@@'):
            if line.startswith(prefix):
                break
        else:
            text_compare += line + '\n'
    if screen:
        print(text_compare)
    else:
        save_file('compare.txt', text_compare)

def work_file(params):
    only_screen = False
    only_help = False
    only_compare = False
    only_compare_print = False
    for param in params:
        if param == '-screen':
            only_screen = True
            break
        elif param == '/?':
            only_help = True
            break
        elif param == '-compare':
            only_compare = True
            break
        elif param == '-compare_print':
            only_compare_print = True
            break

    if only_screen:
        screen_text(params)
    elif only_help:
        print_help()
    elif only_compare:
        print_compare(params, False)
    elif only_compare_print:
        print_compare(params, True)
    else:
        text_all = read_text_file(params[1])
        output_file = output_filename(params)
        save_file(output_file, text_all)


if __name__ == "__main__":

    cmd_params = sys.argv

    if len(cmd_params) == 1:
        print('/? for help')
        sys.exit()
    elif len(cmd_params) > 1:
        work_file(cmd_params)
