from  functions import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    auto = Automate("automate_test.txt")
    auto.recognise_automate_from_file()
    auto.print_automate_details()
    auto.print_transitions_table()
    standardize(auto)
    auto.print_automate_details()
    auto.print_transitions_table()






