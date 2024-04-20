from  functions import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    auto = Automate("/automates/A7-23.txt")
    print("RECOGNISE")
    auto.recognise_automaton_from_file()
    print("PRINTING DETAILS")
    auto.print_automate_details()
    print("PRINTING TABLE")
    auto.print_transitions_table()
    print("STANDARDIZE")
    auto.standardize_automaton()
    print("PRINTING DETAILS")
    auto.print_automate_details()
    print("PRINTING TABLE")
    auto.print_transitions_table()
    print("COMPLETE")
    auto.complete_automaton()
    print("PRINTING TABLE")
    auto.print_transitions_table()

    auto2 = auto.complementary_language()
    auto2.print_automate_details()
    auto2.print_transitions_table()







