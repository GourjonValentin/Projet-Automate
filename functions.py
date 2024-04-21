from math import *

class Automate:
    def __init__(self,fichier):
        self.fichier = fichier
        self.transitions = []
        self.states = []
        self.nb_symb = 0
        self.nb_states = 0
        self.init_states = []
        self.nb_init_states = 0
        self.term_states = []
        self.nb_term_states = 0
        self.nb_transitions = 0
        self.symb = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26}

    def recognise_automaton_from_file(self):
        file = open(f"./{self.fichier}","r")
        self.nb_symb = int(file.readline())
        self.nb_states = int(file.readline())
        self.states = []

        init_states = file.readline()
        self.nb_init_states = int(init_states[0])
        self.init_states = init_states[1:].split()

        self.term_states = file.readline()
        self.nb_term_states = int(self.term_states[0])
        self.term_states = self.term_states[1:].split()

        self.nb_transitions = int(file.readline())

        for _ in range (self.nb_transitions):
            state1, state2 = "", ""
            line = file.readline()
            j = 0

            while(line[j] not in self.symb):
                state1 += line[j]
                j += 1
            k = j
            j += 1

            while (j<len(line)):
                if(line[j] !="\n"):
                    state2 += line[j]
                j += 1

            if(state1 not in self.states):
                self.states.append(state1)

            if (state2 not in self.states):
                self.states.append(state2)

            self.transitions.append((state1,line[k],state2))

    def print_automate_details(self):
        print("Number symbols", self.nb_symb)
        print("Number of states", self.nb_states)
        print("Number of initial states", self.nb_init_states)
        print("Initials states", self.init_states)
        print("Number of terminal states", self.nb_term_states)
        print("Terminals states", self.term_states)
        print("Number of transitions", self.nb_transitions)
        print("Transitions :", self.transitions)
        print("Complet ? ",self.is_complete())
        print("Standard ? ",self.is_standard())
        print("Déterministe ?",self.is_deterministic())

    def transition_to_tab(self):
        # Copie de la liste des états
        # Initialisation du tableau de transitions avec des listes vides
        transitions_table = [[[' ']] * (self.nb_symb+1) for _ in range(self.nb_states)]
        # Remplissage du tableau de transitions avec les transitions

        states = []
        for transition in self.transitions:
            if transition[0] not in states:
                    states.append(transition[0])
            if transition[2] not in states:
                states.append(transition[2])

        for i in range(self.nb_transitions):
            current_state, symbol, next_state = self.transitions[i]

            # Vérifier si l'état actuel est spécial
            current_state_index = self.states.index(current_state)

            symbol_index = self.symb[symbol]

            if transitions_table[current_state_index][0] == [' ']:
                transitions_table[current_state_index][0] = current_state

            if transitions_table[current_state_index][symbol_index] == [' ']:
                transitions_table[current_state_index][symbol_index] = [next_state]
            else:
                transitions_table[current_state_index][symbol_index].append(next_state)

        for state in states:
            notintable = all(state != row[0] for row in transitions_table)
            if notintable :
                for row in transitions_table:
                    if row[0] == [' ']:
                        row[0] = state

        if "P" in self.states:
            if "Init" in self.states:
                transitions_table[-2] = ["P"]+[["P"]]*self.nb_symb
            else:
                transitions_table[-1] = ["P"]+[["P"]]*self.nb_symb

        return transitions_table

    def transition_to_init_state(self):
        return any(i[2] in self.init_states for i in self.transitions)

    
    def print_transitions_table(self):
        transition_table = self.transition_to_tab()
        symbols = self.get_symbols()

        print("             +" + "-----------+" * self.nb_symb)
        print("             |", end="")
        for symbol in symbols:
            print(" {:^9} |".format(symbol), end="")
        print()

        print("--+----------+" + "-----------+" * self.nb_symb)
        
        for i in range(self.nb_states):
            
            if str(transition_table[i][0]) in self.term_states and str(transition_table[i][0]) in self.init_states:
                print("ES|", end="")
            elif str(transition_table[i][0]) in self.term_states:
                print(" S|", end="")
            elif str(transition_table[i][0]) in self.init_states:
                print(" E|", end="")
            else:
                print("  |", end="")

            print(' {:>8} |'.format(transition_table[i][0]), end="")
            print_strings = []
            
            for row in transition_table[i][1:]:
                if len(row) > 1:
                    print_strings.append((' {:^9} |').format(','.join(row)))
                else:
                    print_strings.append((' {:^9} |').format(*row))

            for value in print_strings:
                print(value, end="")

            print()
            print("--+----------+" + "-----------+" * self.nb_symb)

    def is_complete(self):
        transition_table = self.transition_to_tab()
        return all([''] not in row[1:] for row in transition_table) and all([' '] not in row[1:] for row in transition_table)

    def complete_automaton(self):
        transition_table = self.transition_to_tab()
        if self.is_complete():
            return
        self.nb_states += 1
        self.states.append("P")

        
        

        for i in range(len(self.transitions)):
            for j in range(len(self.transitions[i])):
                if self.transitions[i][j] == '':
                    self.transitions[i][j] = 'P'


        transition_table = self.transition_to_tab()

        for i in range(len(transition_table)):
            for j in range(len(transition_table[i])):
                if transition_table[i][j] == [' '] or transition_table[i][j] == ['']:
                    transition_table[i][j] = ['P']
                    # Obtenir le symbole correspondant à la valeur j
                    symbol = self.get_key_from_value(self.symb, j)
                    self.transitions.append((transition_table[i][0], symbol, "P"))
                    self.nb_transitions += 1

        for i in range(self.nb_symb):
            symbol = self.get_key_from_value(self.symb, i+1)
            self.transitions.append(("P", symbol, "P"))
            self.nb_transitions += 1
        
        

    def is_deterministic(self):
        transition_table = self.transition_to_tab()
        if self.nb_init_states > 1:
            return False
        
        return not any(len(transition[i]) > 1 for transition in transition_table for i in range(1, len(transition)))
    
    def determine_automaton(self):
        pass

    def is_standard(self):
        if self.nb_init_states > 1:
            return False
        return not(self.transition_to_init_state())

    def standardize_automaton(self):
        if self.is_standard():
            return

        transition_from_init = [trans for trans in self.transitions if trans[0] in self.init_states]
        self.states.append("Init")
        self.nb_states += 1
        self.init_states = ["Init"]
        self.nb_init_states = 1
        
        for trans in transition_from_init:
            self.transitions.append(('Init', trans[1], trans[2]))
            self.nb_transitions += 1

    def complementary_language(self):
        if self.is_deterministic() and self.is_complete():
            complement_automate = Automate("automate_test.txt")
            complement_automate.recognise_automaton_from_file()
            complement_automate.transitions = self.transitions
            complement_automate.init_states = self.init_states
            complement_automate.nb_transitions = self.nb_transitions
            complement_automate.nb_states = self.nb_states
            complement_automate.nb_symb = self.nb_symb
            complement_automate.nb_init_states = self.nb_init_states
            complement_automate.nb_term_states = self.nb_term_states
            complement_automate.states = self.states
            complement_automate.symb = self.symb
            complement_automate.term_states = self.term_states

            complement_automate.term_states = list(
                set(complement_automate.states) - set(complement_automate.term_states))
            complement_automate.nb_term_states = len(complement_automate.term_states)

            return complement_automate



        elif self.is_deterministic() == False and self.is_complete() == False:
            print("L'automate doit être déterministe et complet !!! \n")

        elif self.is_deterministic() == True and self.is_complete() == False:
            print("L'automate doit être complet !!! \n")

        else:
            print("doit être deterministe  !!! \n")

    def get_key_from_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key

    def get_symbols(self):
        langage = []
        for transition in self.transitions:
            if transition[1] not in langage:
                langage.append(transition[1])

        langage.sort()
        return langage
    
    def recognize_langage(self, word):
        tab_transition = self.transition_to_tab()
        state_dict = self.create_state_dictionary()  
        for init_state in self.init_states:
            index = init_state
            for letter in word:
                if letter not in self.symb:
                    return False
                letter_index = self.symb[letter]

    
                if index in state_dict:
                    index = state_dict[index]
                else:
                    return False

            
                index = tab_transition[index][letter_index]
        return index in self.term_states

    def create_state_dictionary(self):
        state_dict = {}
        index = 0
        for state in self.states:
            state_dict[state] = index
            index += 1
        return state_dict
    
    def get_transitions_from_state(self, state):
        invert_symb = {v: k for k, v in self.symb.items()}

        trans = {}
        for i in range(self.nb_symb):
            trans[invert_symb[i+1]] = ''

        split_states = [*state]
        for i in self.transitions:
            current_state, symbol, next_state = i
            transwithsymb = trans[symbol]
            if current_state in split_states and next_state not in [*transwithsymb]:
                trans[symbol] = trans[symbol] + next_state

        return trans

    def determinize(self):
        if self.is_deterministic():
            return

        transition_table = self.transitions
        new_transitions = []
        new_states = []
        new_init_states = []
        new_term_states = []

        # Etats initiaux
        init_state = ""
            
        for i in self.init_states:
            init_state += str(i)

        new_init_states.append(init_state)
        new_states.append(init_state)
        newstate_ind = 0
        while newstate_ind < len(new_states):
            
            state = new_states[newstate_ind]

        
            new_trans = self.get_transitions_from_state(state)
            for trans in new_trans.items():
                new_transitions.append([state, trans[0], trans[1]])
                # Ajout de l'état d'arrivé si nouveau
                if trans[1] not in new_states and trans[1]!='':
                    new_states.append(trans[1])
                    # Test si état final
                    for i in [*trans[1]]:
                        if i in self.term_states:
                            new_term_states.append(trans[1])

            newstate_ind += 1

        self.transitions = new_transitions
        self.states = new_states
        self.init_states = new_init_states
        self.term_states = new_term_states
        self.nb_states = len(new_states)
        self.nb_init_states = len(new_init_states)
        self.nb_term_states = len(new_term_states)
        self.nb_transitions = len(new_transitions)