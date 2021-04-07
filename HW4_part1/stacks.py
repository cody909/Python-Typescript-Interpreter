from psElements import Value, StrConstant, ArrayConstant, FunctionBody
class Stacks:
    def __init__(self):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        
        #The builtin operators supported by our interpreter
        self.builtin_operators = {
             #TO-DO in part1
        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        return self.opstack.pop(-1)

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        return self.dictstack.pop(-1)

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        self.dictstack.append(d)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    def define(self,name, value):
        if len(self.dictstack) == 0:
            self.dictstack.append({})
        self.dictstack[-1].update({name:value})

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the opstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        name = "/" + name
        for dictionary in reversed(self.dictstack):
            value = dictionary.get(name)
            if value != None:
                return value
        print("Error: lookup - definition was not found in the dictstack")
        return None
    
    #------- Arithmetic Operators --------------
    
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op2 * op1)
            else:
                print("Error: mul - one of the operands is not a number value")
        else:
            print("Error: mul expects 2 operands")

        

    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if op1 == op2:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: eq expects 2 operands")
    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        if len(self.opstack) > 1:
            top = self.opPop()
            bottom = self.opPop()
            if bottom < top:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: lt expects 2 operands")
        

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        if len(self.opstack) > 1:
            top = self.opPop()
            bottom = self.opPop()
            if bottom > top:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: gt expects 2 operands")
    # ------- String and Array Operators --------------
    """ 
       Pops a string or array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support both ArrayConstant and StrConstant values.
    """
    def length(self):
        op = self.opPop()
        if isinstance(op, StrConstant):
            self.opPush(len(op.value) - 2)
        if isinstance(op, ArrayConstant):
            self.opPush(len(op.value))
        else:
            print("Error: length expects am ArrayConstant or a StrConstant")

    """ 
        Pops a StrConstant or an ArrayConstant and an index from the operand opstack.  
        If the argument is a StrConstant, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an ArrayConstant, pushes the value at the `index` of array onto the opstack;
    """
    def get(self):
        if len(self.opstack) > 1:
            index = self.opPop()
            op = self.opPop()
            if isinstance(op, StrConstant):
                self.opPush(ord(op.value[index + 1])) # +1 becase of parentheses around StrConstant
            elif isinstance(op, ArrayConstant):
                self.opPush(op.value[index])
            else:
                print("Error: get expects am ArrayConstant or a StrConstant")
        else:
            print("Error: get expects 2 operands")
        
    """
    Pops a StrConstant or ArrayConstant value, an (zero-based) `index`, and an `item` from the opstack
    If the argument is a StrConstant, replaces the character at `index` of the StrConstant's string with the character having the ASCII value of `item`.
    If the argument is an ArrayConstant, replaces the element at `index` of the ArrayConstant's list with the value `item`.
    <argument> <index> <value>
    """
    def put(self):
        if len(self.opstack) > 2:
            value = self.opPop()
            index = self.opPop()
            argument = self.opPop()
            if isinstance(argument, StrConstant):
                temp = list(argument.value)
                # print("temp = " + str(temp))
                temp[index+1] = chr(value)
                # print("temp now = " + str(temp))
                argument.value = ''.join(map(str,temp))
            elif isinstance(argument, ArrayConstant):
                argument.value[index] = value
            else:
                print("Error: put expects an ArrayConstant or a StrConstant")

                
        else:
            print("Error: put expects 3 operands")

        
            
    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        return self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print("opstack")
        for item in self.opstack:
            print(item + " ")

    """
       Copies the top element in opstack.
    """
    def dup(self):
        op = self.opPop()
        self.opPush(op)
        self.opPush(op)

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        count = self.pop()
        list = []
        while count > 0:
            list.append(self.pop())
            count = count - 1
        for item in reversed(list):
            self.opPush(item)
        for item in reversed(list):
            self.opPush(item)

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        del self.opstack[:]
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        first = self.pop()
        second = self.pop()
        self.opPush(first)
        self.opPush(second)

    """
       Pops an integer from the opstack (size argument) and pushes an  empty dictionary onto the opstack.
    """
    def psDict(self):
        size = self.pop()
        self.opPush({})
        

    """
       Pops the dictionary at the top of the opstack; pushes it to the dictstack.
    """
    def begin(self):
        dictionary = self.pop()
        if isinstance(dictionary, dict):
            self.dictstack.append(dictionary)
        else:
            print("Error: begin expects a dictionary to be at the top of the opstack")

    """
       Removes the top dictionary from dictstack.
    """
    def end(self):
        if len(self.dictstack) > 0:
            self.dictstack.pop(-1)
        else: 
            print("Error: no dictionaries in dictstack")
        
    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    def psDef(self):
        value = self.pop()
        name = self.pop()
        self.define(name, value)

    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
    def psIf(self):
        pass
        # TO-DO in part2

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        pass
        # TO-DO in part2


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops the `loopbody`, `end`index, `increment`, `start` index arguments from opstack; 
       loop counter starts at `start` , incremented by `increment` value, and ends at `end`. 
       for each value of loop counter, push the counter value on opstack, and  evaluate the `loopbody`. 
    """   
    def psFor(self):
        pass
        # TO-DO in part2

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []
