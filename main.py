from  functions import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    auto = Automate("automate_test.txt")
    auto.recognise_automate_from_file()
    auto.print_automate_details()
    auto.transition_to_tab()
    auto.print_transitions_table()
    auto.standardize()
    auto.print_automate_details()
    auto.complete_automaton()
    auto.print_transitions_table()

    auto2 = auto.complementary_language()
    auto2.print_automate_details()
    auto2.print_transitions_table()







