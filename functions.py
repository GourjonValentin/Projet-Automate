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
        self.states = []



        init_states = file.readline()
        self.nb_init_states = int(init_states[0])
        self.init_states = init_states[1:].split()

        self.term_states = file.readline()
        self.nb_term_states = int(self.term_states[0])
        self.term_states = self.term_states[1:].split()

        self.nb_transitions = int(file.readline())
        for i in range (self.nb_transitions):
            state1 = ""
            state2 = ""
            line = file.readline()
            j=0
            while(line[j] not in self.symb):
                state1 += line[j]
                j+=1
            k=j
            j+=1
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
        # Initialisation du tableau de transitions avec des listes vides
        transitions_table = [[''] * (self.nb_symb + 1) for _ in range(self.nb_states)]
        # Remplissage du tableau de transitions avec les transitions
        for i in range(self.nb_transitions):
            current_state, symbol, next_state = self.transitions[i]
            # Vérifier si l'état actuel est spécial
            if current_state == "Init":
                current_state_index = -1
            elif current_state == "P" and "Init" in self.states:
                current_state_index = -2
            elif current_state == "P" and "Init" not in self.states:
                current_state_index = -1
            else:
                current_state_index = self.states.index(current_state)
            symbol_index = self.symb[symbol]

            if transitions_table[current_state_index][0] == "":
                transitions_table[current_state_index][0] = current_state

            if transitions_table[current_state_index][symbol_index] == "":
                transitions_table[current_state_index][symbol_index] = next_state
            else:
                # Si plusieurs transitions pour un même symbole, les regrouper en une liste
                if not isinstance(transitions_table[current_state_index][symbol_index], list):
                    transitions_table[current_state_index][symbol_index] = [
                        transitions_table[current_state_index][symbol_index]]
                transitions_table[current_state_index][symbol_index].append(next_state)

        if "P" in self.states and "Init" in self.states:
            transitions_table[-2] = ["P", ["P"] * (self.nb_symb + 1)]

        elif "P" in self.states and "Init" not in self.states:
            transitions_table[-1] = ["P", ["P"] * (self.nb_symb + 1)]

        return transitions_table

    def transition_to_init_state(self):
        for i in self.transitions:
            if i[2] in self.init_states:
                return True
        return False

    def is_deterministic(self):
        transition_table = self.transition_to_tab()
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
        print(transition_table)
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
                            if transition_table[i][j-1][k]!="P":
                                print(int(transition_table[i][j-1][k]),end=" ")
                            else:
                                print(transition_table[i][j - 1][k], end=" ")
                    else:
                        print(" " * 10, end="")
                        print(f"{transition_table[i][j-1]}", end="")
                    print("|",end="")
        print("\n")
        print("--------------------------------------------------------")

    def complete_automaton(self):
        if not self.is_complete():
            self.nb_states += 1
            self.states.append("P")
            transition_table = self.transition_to_tab()
            for i in range(len(transition_table)):
                for j in range(len(transition_table[i])):
                    if transition_table[i][j] == "" and str(transition_table[i][0]) not in self.term_states:
                        transition_table[i][j] = 'P'
                        # Obtenir le symbole correspondant à la valeur j
                        symbol = self.get_key_from_value(self.symb, j)
                        self.transitions.append((transition_table[i][0], symbol, "P"))
                        self.nb_transitions+=1
            for i in range(self.nb_symb):
                symbol = self.get_key_from_value(self.symb, i+1)
                self.transitions.append(("P",symbol,"P"))
                self.nb_transitions+=1
    def get_key_from_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key

    def standardize(self):
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
            complement_automate.recognise_automate_from_file()
            complement_automate.transitions = self.transitions
            complement_automate.init_states = self.init_states
            complement_automate.nb_transitions = self.nb_transitions
            complement_automate.nb_states = self.nb_states
            print("transitions:",self.transitions)



            for i in range(self.nb_transitions):
                current_state, symbol, next_state = self.transitions[i]

                # Si l'état suivant est dans la liste des états terminaux, le rendre non terminal
                if current_state in self.term_states:
                    if current_state in complement_automate.term_states:
                        complement_automate.term_states.remove(current_state)
                        complement_automate.nb_term_states -= 1
                    # Sinon, rendre l'état suivant terminal
                elif current_state not in complement_automate.term_states:
                    complement_automate.term_states.append(current_state)
                    complement_automate.nb_term_states += 1



            return complement_automate



        elif self.is_deterministic() == False and self.is_complete() == False:
            print("L'automate doit être déterministe et complet !!! \n")

        elif self.is_deterministic() == True and self.is_complete() == False:
            print("L'automate doit être complet !!! \n")

        else:
            print("doit être deterministe  !!! \n")

    def minimization(self):
        if not (self.is_complete() and self.is_deterministic()):
            print("L'automate doit être déterministe complet pour pouvoir minimiser")
            return None

        # Créer une partition initiale des états en états terminaux et non terminaux
        partition = [set(self.term_states), set(self.states) - set(self.term_states)]

        # Créer un dictionnaire pour stocker les nouvelles transitions minimisées
        new_transitions = {}

        # Initialiser une liste de partitions à explorer
        partitions_to_explore = [partition]

    def recognize_langage(self, word):
        tab_transition = self.transition_to_tab()
        index = self.init_states[0]  # Utilisation de l'état initial directement
        for letter in word:
            # Vérifier si la lettre est reconnue
            if letter not in self.symb:
                print(f"Lettre '{letter}' non reconnue. Mot invalide.")
                return False
            letter_index = self.symb[letter]

            # Convertir l'indice en entier
            index = int(index)
            # Accéder à l'état suivant dans le tableau de transitions
            index = tab_transition[index][letter_index]
        return index in self.term_states


