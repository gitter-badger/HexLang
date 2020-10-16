import re
import sys
import os
import argparse
import colorama
from colorama import init
from argparse import ArgumentParser

STD_FILE_ENDING = '.hex'
VERSION = '0.0.1'
NAME = 'HEX LANG'
AUTHOR = 'Alexander Abraham'
LICENSE = 'MIT license'
class Utils:
    def read_from_file(self, code_file):
        try:
            return open(code_file, 'r').readlines()
        except Exception as error:
            print(str(error))
            exit()
    def return_base(self, code_file):
        items_list = code_file.split(STD_FILE_ENDING)
        base_name = items_list[0]
        return base_name
    def return_cpp_name(self, code_file):
        self.return_base_name(code_file) + '.cpp'
    def return_bin_name(self, code_file):
        self.return_base_name(code_file) + '.bin'
    def check_env(self):
        try:
            os.system('g++')
        except Exception as error:
            print(colorama.Fore.RED + str(error) + colorama.Back.RESET)
            sys.exit()
class Lexer:
    def __init__(self,string):
        self.string = string
    def program_tokens(self):
        tokens = {
        'OUT':r'stdout',
        'VARABLE_DECLARATOR':r'var',
        'IDENTIFIER':r'\b(?!(?:func|var|return|while|for|[0-9]+)\b)\w+',
        'EQUALS':r'\=',
        'FLOAT':r'[0-9]+\.[0-9]+',
        'STRING':r'"(.*)"',
        'SEMICOLON':r';',
        }
        return tokens
    def lex(self):
        line_list = self.string.split('\n')
        token_dict = ()
        token_list = []
        lexed_tokens = self.program_tokens()
        for line in line_list:
            for x in lexed_tokens:
                regex = lexed_tokens[x]
                line.strip('\n')
                token = re.findall(regex, line)
                remainder_obj = re.compile(regex)
                remainder = remainder_obj.sub('',line)
                if remainder != None and token != None:
                    token_list = token_list + token
                else:
                    print('Syntax error on line: ',line)
        for i in token_list:
            for x in lexed_tokens:
                if re.match(lexed_tokens[x],i):
                    token_dict = token_dict + ((x,i,),)
                else:
                    pass
        return token_dict
    def visual(self):
        print(self.lex())
        for i in self.lex():
            print(str(i[0]) + ' : ' + str(i[1]))

class AST:
    def __init__(self, string):
        self.string = string
        self.patterns = {
        'VARIABLE_NUMBER':'VARABLE_DECLARATOR IDENTIFIER EQUALS FLOAT SEMICOLON',
        'VARIABLE_STRING':'VARABLE_DECLARATOR IDENTIFIER EQUALS STRING SEMICOLON'
        }
        self.lexed = Lexer(self.string).lex()
    def ast(self):
        ast_statements = []
        intermediate_stack = []
        secret_stack = []
        for i in self.lexed:
            intermediate_stack.append(i[0])
            secret_stack.append(i)
            joined = ' '.join(intermediate_stack)
            for pat in self.patterns:
                if self.patterns[pat] == joined:
                    new_dict = {}
                    new_dict[pat] = secret_stack
                    ast_statements.append(new_dict)
                    intermediate_stack = []
                    secret_stack = []
                    del new_dict
                    break
                else:
                    pass
        return ast_statements
    def linter(self):
        if type(self.ast()) is list and self.ast() is not None:
            return 0
        else:
            return 1
    def visual(self):
        print('\n')
        print('root')
        print('  |  ')
        for i in self.ast():
            print(i)
            print('  |  ')
        print('EOF')
        print('\n')
    def raw_visual(self):
        print(self.ast())
class IR:
    def __init__(self,string):
        self.string = string
        self.ast = AST(self.string).ast()
        self.ir_statements = [
        'VARABLE_DECLARATOR',
        'EQUALS',
        'SEMICOLON'
        ]
    def ir(self):
        ir = []
        for stat in self.ast:
            for key in stat:
                new_dict = {}
                new_list = []
                for token in stat[key]:
                    if token[0] not in self.ir_statements:
                        new_list.append(token)
                    else:
                        pass
                new_dict[key] = new_list
                ir.append(new_dict)
                del new_dict
                del new_list
        return ir
    def visual(self):
        for y in self.ir():
            print(y)
class CodeGen:
    def __init__(self,string):
        self.string = string
        self.ir = IR(self.string).ir()
        self.cg_statements = {
        'VARIABLE_NUMBER':'double IDENTIFIER = FLOAT;',
        'VARIABLE_STRING':'string IDENTIFIER = STRING;'
        }
        self.code = []
    def prep(self):
        self.code.append('#include <iostream>')
        self.code.append('#using namespace std;')
        self.code.append('int main() {')
        for stat in self.ir:
            for key in stat:
                if key in self.cg_statements:
                    old_string = self.cg_statements[key]
                    im_list = []
                    for i in stat[key]:
                        im_list.append(i[0])
                        if i[0] in self.cg_statements[key]:
                            new_string = old_string.replace(i[0],i[1])
                            old_string = new_string
                            if i[0] not in new_string:
                                for type in im_list:
                                    if type in new_string:
                                        pass
                                    else:
                                        fc = ' '*2 + new_string
                                        self.code.append(fc)
                                        break

                            else:
                                pass
                else:
                    pass
        self.code.append('  return 0;')
        self.code.append('}')
        raw_string = '\n'.join(self.code)
        return raw_string
    def stage_two(self):
        old = self.prep().split('\n')
        string_list = []
        for i in old:
            for stat in self.ir:
                for key in stat:
                        for item in stat[key]:
                            if item[0] in string_list:
                                pass
                            else:
                                string_list.append(item[0])
        return string_list
    def final_stage(self):
        old_list = self.prep().split('\n')
        for i in old_list:
            for x in self.stage_two():
                if x in i:
                    lindex = old_list.index(i)
                    old_list.pop(lindex)
                else:
                    pass
        return old_list
    def cg(self):
        return '\n'.join(self.final_stage())
    def visual(self):
        print(self.cg())

class Manager:
    def __init__(self, file):
        self.file = file
        self.utils = Utils()
        self.cpp_name = self.utils.return_cpp_name(self.file)
        self.bin_name = self.utils.return_bin_name(self.file)
        self.hex_code = self.utils.read_from_file(self.file)
        self.cpp_code = CodeGen(self.hex_code).cg()
    def cpp(self):
        try:
            cpp_file = open(self.cpp_name, 'w')
            cpp_file = open(self.cpp_name, 'a')
            cpp_file.write(self.cpp_code)
            cpp_file.close()
        except Exception as errror:
            print(colorama.Fore.RED + str(error) + colorama.Back.RESET)
            sys.exit()
        if os.path.isfile(self.cpp_name) == True:
            print(colorama.Fore.CYAN + 'Transpilation finished!' + colorama.Back.RESET)
        else:
            print(colorama.Fore.RED + 'Transpilation failed!' + colorama.Back.RESET)
    def binary(self,static):
        compiler_command = [
        'g++'
        ]
        self.cpp()
        if static == True:
            compiler_command.append(self.file)
            compiler_command.append('-o')
            compiler_command.append(self.bin_name)
            compiler_command.append('-static')
            try:
                os.system(' '.join(compiler_command))
            except Exception as error:
                print(colorama.Fore.RED + str(error) + colorama.Back.RESET)
                sys.exit()
        else:
            compiler_command.append(self.file)
            compiler_command.append('-o')
            compiler_command.append(self.bin_name)
            try:
                os.system(' '.join(compiler_command))
            except Exception as error:
                print(colorama.Fore.RED + str(error) + colorama.Back.RESET)
                sys.exit()
    def lint(self):
        try:
            AST(self.hex_code).linter()
            print(colorama.Fore.GREEN + 'Checks passed!' + colorama.Back.RESET)
        except Exception as error:
            print(colorama.Fore.RED + str(error) + colorama.Back.RESET)
            print(colorama.Fore.GREEN + 'Checks failed!' + colorama.Back.RESET)
            sys.exit()
    def verbose(self):
        CodeGen(self.cpp_code).visual()


class HexLang:
    def run(self):
        Utils().check_env()
        parser = ArgumentParser()
        parser.add_argument('--version', help='displays version info', action='store_true')
        parser.add_argument('--static', help='compile a hexLang file statically', action='store_true')
        parser.add_argument('--lint', help='check if the code is correct')
        parser.add_argument('--cpp', help='convert a HexLang file to a C++ file')
        parser.add_argument('--bin', help='compile a HexLang file to a binary executable')
        parser.add_argument('--verbose', help='print out C++ code for a HexLang file')
        args = parser.parse_args()
        if args.version:
            version_info = NAME + ' ' + VERSION + '\n by ' + AUTHOR + '\nlicensed under the ' + LICENSE
            print(colorama.Fore.MAGENTA + version_info + colorama.Back.RESET)
        elif args.cpp:
            manager = Manager(str(args.cpp))
            manager.cpp()
        elif args.linter:
            manager = Manager(str(args.cpp))
            manager.lint()
        elif args.bin and args.static:
            manager = Manager(str(args.bin))
            manager.binary(True)
        elif args.bin:
            manager = Manager(str(args.bin))
            manager.binary(False)
        elif args.verbose:
            manager = Manager(str(args.verbose))
            manager.verbose()
        else:
            print(colorama.Fore.CYAN + 'Wrong argument combo provided!\nTry the "--help" flag!' + colorama.Back.RESET)
            sys.exit()


def main():
    HexLang().run()
if __name__ == '__main__':
    main()
