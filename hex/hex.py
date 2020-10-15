import re
import sys
import os

STD_FILE_ENDING = '.n'
VERSION = '1.0beta'
NAME = 'NEO LANG'
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
            print(str(error))
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
            print('\n\n')
            for key in stat:
                print(key + ':')
                stat_dict = {}
                for token in stat[key]:
                    new_list = []
                    for myst in self.ir_statements:
                        if token[0] == myst:
                            pass
                        else:
                            new_list.append(token[1])
                    stat_dict[key] = new_list
                    ir.append(stat_dict)
                    del new_list
                del stat_dict
        return ir
    def visual(self):
        print(self.ir())
class CodeGen:
    def __init__(self,string):
        self.string = string
        self.ir = IR(self.string).ir()
        self.cg_statements = {
        'VARIABLE_NUMBER':'double IDENTIFIER = FLOAT;',
        'VARIABLE_STRING':'string IDENTIFIER = STRING;'
        }
        self.code = []
    def cg(self):
        self.code.append('#include <iostream>')
        self.code.append('#using namespace std;')
        self.code.append('int main() {')
        for key in self.ir:
            pass
        self.code.append('\treturn 0;')
        self.code.append('}')
        return '\n'.join(self.code)
    def visual(self):
        print(self.cg())

def main():
    line = 'var hello = 45.6;\nvar two = 47.6;'
    IR(line).visual()
if __name__ == '__main__':
    main()
