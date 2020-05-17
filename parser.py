#global variables
EPSILON  = "e"
count = 0
tokenArr = []

#converts tokens from the scanner to nonterminals
def convertTokens(t):
    tok = ''
    if t == 'LP: "("':
        tok = 'LP'
    elif t == 'RP: ")"':
        tok = 'RP'
    elif t == 'COMPARE: "<"':
        tok = 'COMP'
    elif t == 'ASGN: "="':
        tok = 'ASGN'
    elif t == 'SC: ";"':
        tok = 'SC'
    elif t == 'ADD: "+"':
        tok = 'ADD'
    elif t == 'SUB: "-"':
        tok = 'SUB'
    elif t == 'IF: "if"':
        tok = 'IF'
    elif t == 'THEN: "then"':
        tok = 'THEN'
    elif t == 'WHILE: "while"':
        tok = 'WHILE'
    elif t == 'DO: "do"':
        tok = 'DO'
    elif "id" in t:
        tok = 'id'
    elif "num" in t:
        tok = 'num'
    return tok

#gets next token from the scanner
def getNextToken():     
    global tokenArr
    if (count < len(tokenArr)):
        return tokenArr[count]

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
        if(token=='COMP'):
            return['COMP', '<sum>']
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


def main():
    global count
    global tokenArr
    terminals = {'LP', 'RP', 'COMP', 'ASGN', 'SC', 'ADD', 'SUB', 'IF', 'THEN', 'WHILE', 'DO', 'id', 'num', '$'}
    nonterminals = {'<program>', '<statement_list>', '<statement>', '<paren_expr>', '<expr>', '<test>', '<test_opt>', '<sum>', '<sum_opt>', '<term>'}
    arr = ['id: "i"', 'ASGN: "="', 'num: "1"', 'SC: ";"', 'WHILE: "while"', 'LP: "("', 'id: "i"', 'COMPARE: "<"', 'num: "10"', 'RP: ")"', 'id: "i"', 'ASGN: "="', 'id: "i"', 'ADD: "+"', 'num: "1"','SC: ";"'] #this will be the input from tokens.txt
    #arr = ['id: "x"' , 'ASGN: "="', 'num: "10"', 'SC: ";"', 'id: "i"', 'ASGN: "="', 'LP: "("', 'LP: "("', 'id: "i"', 'ADD: "+"', 'num: "5"', 'RP: ")"', 'SUB: "-"', 'LP: "("',' id: "x"', 'ADD: "+"', 'id: "i"', 'RP: ")"', 'RP: ")"', 'SC: ";"'] #from in5.tinyc
    #arr = ['IF: "if"', 'LP: "("', 'num: "10"', 'COMPARE: "<"', 'id: "z"', 'RP: ")"', 'id: "z"', 'ASGN: "="', 'num: "0"', 'SC: ";"']    #from in4.tinyc
    #arr = ['LEXICAL_ERROR']        #from in_err1.tinyc
    #arr = ['id: "a"','ASGN: "="', 'LEXICAL_ERROR']     #from in_err2.tinyc
    for i in range(len(arr)):
        t = convertTokens(arr[i])
        tokenArr.append(t)
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


if __name__ == "__main__":
    main()

#SOURCES:
#https://thepythonguru.com/python-builtin-functions/reversed/