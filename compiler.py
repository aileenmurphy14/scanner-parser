'''
Predictive Parser for LL(1) TinyC language based on the following grammar: 
<program> ::= <statement_list>
<statement_list> ::= <statement> SC <statement_list> | ∈
<statement> ::= IF <paren_expr> <statement> |
                WHILE <paren_expr> <statement> |
                DO <statement> WHILE <paren_expr> |
                id ASGN <expr> |
                SC
<paren_expr> ::= LP <expr> RP
<expr> ::= <test>
<test> ::= <sum> <test_opt>
<test_opt> ::= COMPARE <sum> | ∈
<sum> ::= <term> <sum_opt>
<sum_opt> ::= ADD <term> <sum_opt> | SUB <term> <sum_opt> | ∈
<term> ::= id | num | <paren_expr>
'''
import re
import sys

#global variables
EPSILON  = "e"
count = 0
tokList = []   

def getFile():
    sys.stdout = open('parse_tree.txt', 'w')         # outputs the output of the code to text file.   
    with open(sys.argv[1], 'r') as my_file:          # uses the commandline argument to input file
        contents = my_file.read();
        return contents

#------------- SCANNER----------------------------------------------------------------------------
#this function matches the string to a keyword or symbol and adds it to the list
def getToken(t):
    if t == '(':
        tok = 'LP'
    elif t == ')':
        tok = 'RP'
    elif t == '<':
        tok = 'COMPARE'
    elif t == '=':
        tok = 'ASGN'
    elif t == ';':
        tok = 'SC'
    elif t == '+':
        tok = 'ADD'
    elif t == '-':
        tok = 'SUB'
    elif t == 'if':
        tok = 'IF'
    elif t == 'then':
        tok = 'THEN'
    elif t == 'while':
        tok = 'WHILE'
    elif t == 'do':
        tok = 'DO'
    elif findId(t)==True:
        tok = 'id'
    elif findNum(t)==True:
        tok = 'num'
    else:
        tok = 'LEXICAL_ERROR'
    return tok

#this function checks if the string is an id. Must match alphabetical and have length of 1. Returns true or false.
def findId(t):
    x = re.match("[a-z]",t)
    if x and len(t)==1 :
        return True

#this function checks if the string is a number. Returns true or false.
#https://stackoverflow.com/questions/20793578/regex-for-a-valid-32-bit-signed-integer
def findNum(t):
    x = re.match("^-?(\d{1,9}|1\d{9}|2(0\d{8}|1([0-3]\d{7}|4([0-6]\d{6}|7([0-3]\d{5}|4([0-7]\d{4}|8([0-2]\d{3}|3([0-5]\d{2}|6([0-3]\d|4[0-7])))))))))$|^-2147483648$",t)
    if x:
        return True

#This function is a "by hand" Scanner. It outputs a dictionary of symbols and tokens extracted from an input source code into an array to be parsed. 
def scanner():
    global tokList
    string = getFile();    
    KWS = ['(', ')', '=', ';', '+', '-', '<', '^-?(\d{1,9}|1\d{9}|2(0\d{8}|1([0-3]\d{7}|4([0-6]\d{6}|7([0-3]\d{5}|4([0-7]\d{4}|8([0-2]\d{3}|3([0-5]\d{2}|6([0-3]\d|4[0-7])))))))))$|^-2147483648$', '[a-z]', 'if', 'then', 'else', 'while', 'do'] #list of keyword and symbols
    space = ' '
    newline = '\n'
    tab = '\t'
    t = ''  
    for i, char in enumerate(string):           
        if char != space and char != newline and char != tab:  
            t += char
        if(i+1 < len(string)):
            if string[i+1] == space or string[i+1] == newline or string[i+1] == tab or string[i+1] in KWS or t in KWS :
                if t != '':
                    tok = getToken(t)
                    if tok == 'LEXICAL_ERROR':
                        print('error')
                        exit()
                    tokList.append(tok)
                    t = ''
        else:              
            if t != '':
                tok = getToken(t)
                if tok == 'LEXICAL_ERROR':
                        print('error')
                        exit()
                tokList.append(tok)
#--------------------------------------------------------------------------------------------------------------

#---------PARSER-----------------------------------------------------------------------------------------------
def getNextToken():     
    global tokList
    if (count < len(tokList)):
        return tokList[count]

def parsingTable(top, token):
    x = '';
    if(top == '<program>'):
        return['<statement_list>']

    elif(top == '<statement_list>'):
        if(getNextToken()): 
            return['<statement>', 'SC', '<statement_list>']
        else:
            return ['e']
    elif(top == '<statement>'):
        if(token == 'IF'):
            return['IF', '<paren_expr>', '<statement>']
        elif(token == 'WHILE'):
            return ['WHILE', '<paren_expr>', '<statement>']
        elif(token == 'DO'):
            return ['DO', '<statement>', 'WHILE', '<paren_expr']
        elif(token== 'id'):
            return ['id','ASGN', '<expr>']
        elif(token == 'SC'):
            return['SC'] 
    elif(top == '<paren_expr>'):
        return['LP', '<expr>', 'RP']
    elif(top == '<expr>'):
        return['<test>'] 
    elif(top == '<test>'):
        return ['<sum>', '<test_opt>']
    elif(top == '<test_opt>'):
        if(token=='COMPARE'):
            return['COMPARE', '<sum>']
        else:
            return['e']
    elif(top == '<sum>'):
        return['<term>', '<sum_opt>']
    elif(top == '<sum_opt>'):
        if(token == 'ADD'):
            return ['ADD', '<term>', '<sum_opt>']
        elif(token == 'SUB'):
            return ['SUB', '<term>', '<sum_opt>']
        else:
            return[EPSILON]
    elif(top == '<term>'):
        if(token == 'id'):
            return['id']
        elif(token=='num'):
            return['num']
        elif(token == 'LP'):
            return['<paren_expr>']
    return x;

def parser():
    global count        #count in tokenArr
    global tokList      # list of tokens from scanner
    terminals = {'LP', 'RP', 'COMPARE', 'ASGN', 'SC', 'ADD', 'SUB', 'IF', 'THEN', 'WHILE', 'DO', 'id', 'num', '$'}
    nonterminals = {'<program>', '<statement_list>', '<statement>', '<paren_expr>', '<expr>', '<test>', '<test_opt>', '<sum>', '<sum_opt>', '<term>'}
    stack = []
    token = getNextToken() 
    count = count + 1
    stack.append('$')
    stack.append('<program>')
    top = stack[-1]
    while (top != '$'):
        if(top != EPSILON):
            print(top)
        if(top == EPSILON):
            stack.pop()
        if top in terminals:
            if top == token:
                stack.pop()
                token = getNextToken()
                count = count + 1
            else:
                print("error")
                break
        elif top in nonterminals:
            elements = parsingTable(top, token)  
            if(elements):
                stack.pop()
                backwardsArr = list(reversed(elements))
                for j in backwardsArr:
                    stack.append(j)
            else:
                print("error")
                break
        top = stack[-1]
#--------------------------------------------------------------------------------------------------------
def main():
    scanner()
    parser()

if __name__ == "__main__":
    main()
