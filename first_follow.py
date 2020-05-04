import itertools
# test cases
# https://www.gatevidyalay.com/first-and-follow-compiler-design/

gram = {


    'A' : [['B','X','b','c'] , ['d','e','f'] , ['g','h','i'] , ['𝛆']],
    'X' : [['q']],
    'B' : ['s','𝛆']
}

gram2 = {
    'S': [['A','B','C','D']],
    'A': [['a'], ['𝛆']],
    'B': [['C','D'], ['b']],
    'C': [['c'],['𝛆']],
    'D': [['A','a'], ['d'],['𝛆']]

}

pr1 = {
    'S': [['A']],
    'A': [['a','B',"A'"]],
    "A'": [['d',"A'"],['𝛆']],
    'B': [['b']],
    "A'": [['d',"A'"],['𝛆']],
    'C': [['g']]

}

pr3 = {
    'S': [['(','L',')'],['a']],
    'L': [['S',"L'"]],
    "L'": [[',','S'],['𝛆']],
}
non_terminal_list = ['A','X','B']
non_terminal_list2 = ['S','A','B','C','D']
termial_pr1 = ["S", "A" , "A'", "B", "C"]
termial_pr3 = ["S", "L", "L'"]

G_follow = {}
def is_non_terminal(A, non_terminal_list):
    if A in non_terminal_list:
        return True
    return False

def has_epsilon(my_list):
    if '𝛆' in my_list:
        return True
    return False

def get_first(grammar, non_terminal, non_terminal_list):
    first_i = set()

    # scanning each list in non_terminal
    for j in grammar[non_terminal]:
        #print(f'{j[0]}')
        if is_non_terminal(j[0], non_terminal_list):
            # scanning each element in list
            for element in j:
                flag = False
                if is_non_terminal(element, non_terminal_list):
                    x = get_first(grammar, element, non_terminal_list)

                    f = has_epsilon(x)

                    """
                    if has_epsilon(x):
                        x.remove('𝛆')
                        flag = True
                    else:
                        break

                    """
                    
                    if f:
                        x.remove('𝛆')
                        first_i.update(x)
                        flag = True
                    else:
                        first_i.update(x)
                        break
                    
                else:
                    if element == '𝛆':
                        flag = True 
                    else:
                        first_i.add(element)
                #print(flag)
                    #break
            if flag:
                #print('flag is true')
                first_i.add('𝛆')       
        else:
            first_i.add(j[0])
    return first_i


    

def get_first_1(grammar, non_terminal, non_terminal_list):
    '''
    https://www.gatevidyalay.com/first-and-follow-compiler-design/

    rules applied: 

        1) For a production rule X → ∈,
            First(X) = { ∈ }

        2) For any terminal symbol ‘a’,
            First(a) = { a }

        3) For a production rule X → Y1Y2Y3,
            calculate first(Y1):
                If ∈ ∉ First(Y1), then First(X) = First(Y1)
                If ∈ ∈ First(Y1), then First(X) = { First(Y1) – ∈ } ∪ First(Y2Y3)
            else repeat 3) for Y(n+1)

        assumption for recursion:
            left recursion is eliminated

    '''
    first_i = set()

    # scanning each list in non_terminal
    for j in grammar[non_terminal]:
        ##print(j[0])

        # if terminal add it directly
        if not is_non_terminal(j[0], non_terminal_list):
            first_i.add(j[0])
            
        else:
            # if a non-terminal,walk through
            for k in j:
                if is_non_terminal(k, non_terminal_list):
                    temp = get_first(grammar, k, non_terminal_list)
                    first_i.update(temp)
                    if not has_epsilon(temp):
                        break
                else:
                    ##print(k)
                    first_i.add[k]
                    break
                    

    return first_i

def get_follows(grammar, first_set, start_symbol, non_terminal_list):
    follows = {}
    for non_terminal in non_terminal_list:
        follow = get_follow(grammar, non_terminal, first_set, start_symbol, non_terminal_list)
        follows[non_terminal] = follow

    return follows

def get_follow(grammar, non_terminal, first_set, start_symbol, non_terminal_list):
    '''
        1) for starting symbol place $ in the follow set
        2) if the is a production A → 𝞪B𝝱:
            Follow(B) = First(𝝱)
            if First(𝝱) has 𝝴 :
                Follow(B) = Follow(A)
        3) if the is a production A → 𝞪B:
            Follow(B) = Follow(A)

        find_first_sole → returns firsts and follows NT

    '''
    follow_i = set()
    if non_terminal is start_symbol:
        follow_i.add('$')
        ##print("follow first")

    # step one get the follows based on firsts
    productions = parse_production(get_rhs(grammar, non_terminal))
    print(f'productions for {non_terminal} : {productions}')

    #first_follow = find_first_sole(grammar, non_terminal, productions, non_terminal_list)
    first, follow = find_first_sole(grammar, non_terminal, productions, non_terminal_list)
    first_follow = parse_find_first(first, follow)
    ##print(f'initial follows are {first_follow[0]} : {first_follow[1]}')

    follow_i.update(first_follow[0])
    for i in first_follow[1]:
        follow_i.update(get_follow(grammar, i, first_set, start_symbol, non_terminal_list)) 
    return follow_i



def parse_production(production_list):
    new_production_list = {}
    new_list_out = []
    temp = []
    for i in production_list:
        ##print(production_list[i])
        new_list = []
        for j in production_list[i]:
            ##print(j)
            
            if not j:
                ##print("epsilon")
                temp = ['𝛆']
            else:
                temp = j
            new_list.append(temp)
        new_production_list[i] = new_list    
        #new_list_out.append(new_list)
    ##print(new_production_list)
    return new_production_list


def find_first_sole(grammar, non_terminal, non_terminal_production, non_terminal_list, epsilon=0):
    #non terminal production for one non-terminal
    first = set()
    follow_of_follow = set()
    external_list = []
    
    for i in non_terminal_production:
        count = 0
        for j in non_terminal_production[i]:
            count += 1

            ##print(f'*{j}*')
            ##print(f'len of j : {len(j)}')
            for element in j:
                internal_list = set()
                if is_non_terminal(element, non_terminal_list):
                    first_part = get_first(grammar, element, non_terminal_list)
                    ##print(f'get partial first {first_part} for {element}')
                    first.update(first_part)
                    internal_list.update(first_part)



                    # this part added for parsing table
                    if epsilon == 1:
                        if '𝛆' in first_part:
                            first.add('𝛆')

                    # if a NT has no epsilon then no need to continue
                    if '𝛆' not in first_part:
                        break
                    # if NT has epsilon and it's the last one in list
                    elif count == len(j):
                        follow_of_follow.add(i)

                else:
                    if element == '𝛆':
                        follow_of_follow.add(i)
                        # this part added for parsing table
                        if epsilon == 1:
                                first.add('𝛆')
                    else:
                        first.add(element)
                        internal_list.add(element) 

                    break
            external_list.append(internal_list)
            #print(f'internal list: {internal_list}')

        ##print("*.*"*20)
    if '𝛆' in first:
        if not epsilon:
            first.remove('𝛆')
    if '𝛆'in follow_of_follow:
        follow_of_follow.remove('𝛆')
    if non_terminal in follow_of_follow:
        # ignore it (avoid recursion)
        follow_of_follow.remove(non_terminal)

    return first, follow_of_follow
    

def parse_find_first(first_set , follow_set):
    return [first_set, follow_set]

def find_first(grammar, non_terminal_production, non_terminal_list):
    '''
    
    '''
    first_i = set()
    follow_of_follow = set()

    count = 0

    for i in non_terminal_production:
        ##print(i)
        for j in non_terminal_production[i]:
            break
            #print(j)
    
    ##print(f'terminal production = {terminal_production}')
    """ 
    for i in non_terminal_production:
        #print(f'non-terminal production part: {non_terminal_production[i]}')
        if len(non_terminal_production[i]) == 0:
            #print("just get follow")
            break

        ##print("enteur find")
        # going to each list for a 
        for j in non_terminal_production[i]:
            count += 1
            #print(f'j is : {j}')

            for k in j:
                # first of non-terminal = get_first
                #print(len(non_terminal_production[i]))
                if is_non_terminal(k, non_terminal_list):
                    #print(f"{k} is non-terminal")

                    first_ii = get_first(grammar, k, non_terminal_list)
                    #print(f'first : {first_ii}')
                    first_i.update(first_ii)
                    if '𝛆' not in first_ii:
                        #print("epsilon not found!!")
                        # if last of the list of firsts  &&  is a non-terminal
                        # add follow of j
                        break
                    
                    # if we are in the last element and this element has 𝛆
                    # then get follow of j 
                    if count == len(non_terminal_production[i]):
                        #print(f"followee = {i}")
                        follow_of_follow.add(i)

                else:
                    first_i.add(j)
    first_i.remove('𝛆')
    #print(f'i in find first = {count}') 
    """
    return first_i


def get_index(key, the_list ):

    
    index_list = []

    for i in range(0, len(the_list)):
        print(the_list[i])
        if the_list[i] == key:
            index_list.append(i)
    return index_list

def slice_list(index_list, the_list):

    slices = set()
    for i in range(0, len(index_list)-1):
        begin = index_list[i] + 1
        end = index_list[i+1] - 1
        slices.add(tuple(the_list[begin: end]))
        print(f'{the_list[begin: end]}')
    begin = index_list[i]
    last_element = the_list[begin:]
    
    
    
    return slices


def get_rhs(grammar, non_terminal):
    rhs_dict = {}
    #first = set()
   
    # for each rule
    for i in grammar:
        ##print(grammar[i])
        # for each list in a rule
        first = set()
        second = []
        indx_list = set()
        slices = []

        for j in grammar[i]:
            ##print(f'j is: {j}')
            if non_terminal in j:
                
                # if terminal is found, let slice it
                ##print("guard")
                # temp = j
                the_index = get_index(non_terminal, j)

                # get first occurance of the NT
                indx = j.index(non_terminal)
                temp = j[indx+1:]
                if non_terminal in temp:
                    slices_temp = [list(y) for x, y in itertools.groupby(temp, lambda z: z == non_terminal) if not x]
                    for z in slices_temp:
                        if z not in slices:
                            slices.append(z)
                else:
                    if temp not in slices:
                        slices.append(temp) 

                print(f"*slices are* {slices} **")
                ##print(indx)
                ##print(f"{i} --> *{j[indx+1:]}* ")
                #if j[indx+1:] not in first:
                #first.add(j[indx+1:])
                #first.add('ff')
                tick_list = tuple(slices)
                #first.add(tick_list)

        #slices = list(dict.fromkeys(slices))
        

        if len(slices) != 0:
            rhs_dict[i] = list(slices)
        
        print(slices)
        #first.clear()
    print(rhs_dict)
    return rhs_dict

def separate_production(production_list):
    sep_production = []

    # for each production
    for i in production_list:
        # for each list in a production
        for j in production_list[i]:
            
            sep_production.append({ i: j})
    print(sep_production)
    return sep_production


def build_parsing_table(grammar, non_terminal_list, start_symbol):

    '''
    build a predictive parsing table

    for each production n → 𝞪
        for each a ∈ first(𝞪)
            add n → 𝞪 to T[n,a]
        if 𝜺 ∈ first(𝞪) then
            for each b ∈ follow(n)
                add n → 𝞪 to T[n,a]

    let P be the list of grammar {n → 𝞪} , T the parsing table:

        b = n → 𝞪
        for P in grammar:
            x = first(P.𝞪)
            for i in x:
                if i != 𝜺:
                    T[n,i] = P
            if has_espilon(x):
                y = follow(P.n)
                for j in y:
                    T[n,j] = P 

    '''

    # separate grammar
    # get list of dicts each point to one production
    #sep_production = separate_production(grammar)
    T = {}
    first_set = get_firsts(grammar, non_terminal_list)

    for g in grammar:

        ## returns modified production list dict()
        # alpha shall be a list of production list
        print("*"*15)
        print('[start] separate grammar production')
        productions_list = separate_grammar_production(g, grammar[g])
        # need n--> NT ,
        # get_dict_items()
        for p in productions_list:
            print(f'i in production  n → 𝞪 : {p}')
            x,_ = find_first_sole(grammar, 'z',p,non_terminal_list,1)
            key,val =  get_dict_items(p)
            for i in x:
                if i != '𝜺':
                    print(f'[n,i] → P, [{key},{i}]  → {p}')
                    temp_dict = {i:p}
                    T[key]= temp_dict  
            if has_epsilon(x):
                print("has 𝜺!")
                y = get_follow(grammar,key, first_set, start_symbol,non_terminal_list)
                for j in y:
                    temp_dict = {j:p}
                    T[key]= temp_dict

            #print(f"x is {x}***")
            if not x:
                print("empty")
            print('[end] separate grammar production')
            print("*"*15)

    print(T)
    print(T['S']['a'])

        
        # x = find_first_sole(grammar, 'z',alpha[0],non_terminal_list)
        ## p --> terminal , gramamr[p] --> list of lists
        #print(f'{p}: {grammar[p]}')
        

    
    """ 
    for g in grammar:
        print({g: grammar[g]})
        temp_production = {g: grammar[g]}
        list_sep = separate_production(temp_production)
        for i in list_sep:
            sep_production.append(i)

    for g in sep_production:
        # [{'C': [['b', 'C']]}, {'C': [['𝛆']]}]
        print('--.--.--')
        # production list
        print(g)
    """
    
    """  
    # for each production n → 𝞪
    for n in sep_production:
        # for each a ∈ first(𝞪)
        # add n → 𝞪 to T[n,a]
        #find_first_sole(grammar, )
        #print(n)
        #print(f'---> {n[0]}')
        
        # one iteration loop
        for i in n:
            print(f'*.*.*{n[i]} , {i}*.*.*')
            firsts, follows = find_first_sole(grammar, i, n, non_terminal_list)
            print(firsts)
    """


def separate_grammar_production(key, value):
    '''
        key is the non-terminal
        value is the list pointed to
    '''
    production_dict = {key: value}
    alpha = []

    for i in value:
        alpha.append({key: [i]})

    #print(alpha)
    return alpha

def get_dict_items(the_dict):
    for i in the_dict:
        return i, the_dict[i][0]

def get_firsts(grammar , non_terminal_list):
    '''
     collects each firsts in a BIG dictionary   
    
    '''
    firsts = {}
    for i in grammar:
        first_i = get_first(grammar, i, non_terminal_list)
        firsts[i] = first_i
    return firsts


def main():
   #print("ho ho ho")
   

   #he_dict = {'S': [['A','a','A','b'],['B','b', 'B', 'a']]}
   #separate_production(the_dict)
   #the_list = ['g','A','f','A']
   #delim = 'A'
   #slices = [list(y) for x, y in itertools.groupby(the_list, lambda z: z == delim) if not x]
   #print(slices)

   

   #index = get_index('A', ['A','B','A','h'])

   #x = slice_list(index, ['a','B','D','h'] )
   #print(f'len of x = {len(x)}')

   grammar = {
    
    'S' : [['a','B','D','h']],
    'B' : [['c', 'C']],
    'C' : [['b','C'],['𝛆']],
    'D' : [['E','F']],
    'E' : [['g'],['𝛆']],
    'F' : [['f'],['𝛆']]

   }

   print("Hey hey!")
   non_terminal_list_22 = {'S','A', 'B','C','D', 'E', 'F'}
   build_parsing_table(grammar, non_terminal_list_22, 'S')

   
   #non_terminal = 'F'
   #first_D = get_first(grammar, 'D', non_terminal_list)
   #fist_new = get_first_1(grammar, 'D', non_terminal_list_22)
   ##print(fist_new)
   ##print(first_D)

   #first_set = get_firsts(grammar,non_terminal_list)
   ##print(first_set)
   #start_symbol = 'S'

   #follows = get_follow(grammar, non_terminal, first_set, start_symbol, non_terminal_list_22)
   #print("follows are")
   #print(follows)


if __name__ == '__main__':
    main()
