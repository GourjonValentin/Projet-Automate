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

    def recognise_automate_from_file(self):
        file = open("./"+self.fichier,"r")
        self.nb_symb = int(file.readline())
        self.nb_states = int(file.readline())
        self.states = [i for i in range(self.nb_states)]


        init_states = file.readline()
        self.nb_init_states = int(init_states[0])
        self.init_states = init_states[1:].split()

        self.term_states = file.readline()
        self.nb_term_states = int(self.term_states[0])
        self.term_states = self.term_states[1:].split()

        self.nb_transitions = int(file.readline())
        for i in range (self.nb_transitions):
            line = file.readline()
            self.transitions.append(tuple(line[:-1]))

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
        states = self.states.copy()
        # Initialiser le tableau de transition avec des listes vides
        transitions_table = [[''] * (self.nb_symb + 1) for _ in range(self.nb_states)]

        # Remplir le tableau de transition avec les transitions
        for i in range(self.nb_transitions):
            current_state,symbol,next_state = self.transitions[i]
            current_state_index = int(current_state) if current_state != "Init" else -1
            symbol_index = self.symb[symbol]

            if transitions_table[current_state_index][0] == "":
                transitions_table[current_state_index][0] = current_state

            if transitions_table[current_state_index][symbol_index] == "":
                transitions_table[current_state_index][symbol_index] = [next_state]
            else:
                transitions_table[current_state_index][symbol_index].append(next_state)

        for j in range(self.nb_states):
            if transitions_table[j][0] in states:
                states.remove(transitions_table[j][0])
            else:

                transitions_table[j][0] = j
                states.remove(j)

        return transitions_table

    def transition_to_init_state(self):
        for i in self.transitions:
            if i[2] in self.init_states:
                return True
        return False

    def is_deterministic(self):
        transition_table = self.transition_to_tab()
        print(transition_table)
        for transition in transition_table:
            if (len(transition[1]) > 1 or len(transition[2]) > 1 or self.nb_init_states>1):

                return False
        return True

    def is_standard(self):
        if self.nb_init_states > 1:
            return False
        return not(self.transition_to_init_state())

    def is_complete(self):
        transition_tab = self.transition_to_tab()
        for row in transition_tab:
            if '' in row[1:]:
                return False
        return True

    def print_transitions_table(self):
        transition_table = self.transition_to_tab()
        state = ""
        for i in range(0, self.nb_states):
            print("\n")
            print("--------------------------------------------------------")
            for j in range(0, self.nb_symb + 2):
                if j == 0:
                    if str(transition_table[i][0]) in self.term_states and str(transition_table[i][0]) in self.init_states:
                        print("          ES|", end="")
                    elif str(transition_table[i][0]) in self.term_states:

                        print("           S|", end="")
                    elif str(transition_table[i][0]) in self.init_states:

                        print("           E|", end="")
                    else:
                        print("            |", end="")



                else:


                    if j>=2:
                        print(" " * (10 - 2*(len(transition_table[i][j - 1]))), end="")
                        for k in range (len(transition_table[i][j-1])):
                            print(int(transition_table[i][j-1][k]),end=" ")
                    else:
                        print(" " * 10, end="")
                        print(f"{transition_table[i][j-1]}", end="")
                    print("|",end="")
        print("\n")
        print("--------------------------------------------------------")


def standardize(auto: Automate):
    if auto.is_standard():
        return

    transition_from_init = [trans for trans in auto.transitions if trans[0] in auto.init_states]
    auto.states.append("Init")
    auto.nb_states += 1
    auto.init_states = ["Init"]
    auto.nb_init_states = 1
    for trans in transition_from_init:
        auto.transitions.append(('Init', trans[1], trans[2]))
        auto.nb_transitions += 1


