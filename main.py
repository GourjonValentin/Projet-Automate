from  functions import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    auto = Automate("/automates/A7-19.txt")
    print("RECOGNISE")
    auto.recognise_automaton_from_file()
    print("PRINTING DETAILS")
    auto.print_automate_details()
    print("PRINTING TABLE")
    auto.print_transitions_table()
    
    print("DETERMINIZE")
    auto.determinize()
    print("PRINTING DETAILS")
    auto.print_automate_details()
    print("PRINTING TABLE")
    auto.print_transitions_table()
    print("COMPLETE")
    auto.complete_automaton()
    print("PRINTING DETAILS")
    auto.print_automate_details()
    print("PRINTING TABLE")
    auto.print_transitions_table()

    
    









