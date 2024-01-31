from itertools import combinations
import calc_wirt
import sym_hm
import pandas as pd


def get_seeds(strands, length):
    '''
    input:
        strands: the list of strands in our knot diagram
        length: the desired number of seed strands to start out with
    output:
        An object list of tuples representing seed strands.
        ex: [('A','B'), ('A','C'), ('A','D'), ('B','C'),... ]
    '''
    seeds = combinations(strands, length)
    return seeds


def find_color(strand, strand_colors_dict):
    '''
    Finds the key in strand_colors_dict that contains a list containing strand. In other words, give it a strand and
    it will output what color it is. If the strand is uncolored, the empty character is returned
    Input:
        strand: A char representing a strand in a knot diagram
        strand_colors_dict: A dictionary whose keys are our seed strands and whose values are lists of strands which are
            the same color as the key. Note each value contains a character representing its key.
            Strand_color_dict is of the form
            d_k = {
                    A: ['A', ...]
                    B: ['B', ...]
                    .
                    .
                },
    Output:
        retruns either the color of the strand, (key in dictionary containing a list where strand is an element)
        or returns the empty character if no such key can be found
    '''
    for color in strand_colors_dict:
        if strand in strand_colors_dict[color]:
            return color
    return ''


def maximally_extend(seeds, knot_dict):
    '''
    input:
        seeds: a tuple of chars containing the strands that start out colored
        knot_dict: A dictionary with strands as keys and a list of crossings for which that key is an over strand, as
            output from create_knot_dictionary
    output:
        strand_colors_dict: A dictionary whose keys are our seed strands and whos values are lists of strands which are
            the same color as the key. Note each value contains a character representing its key.
            Strand_color_dict is of the form
            d_k = {
                    A: ['A', ...]
                    B: ['B', ...]
                    .
                    .
                },
    '''
    strand_colors_dict = {}
    for strand in seeds:
        strand_colors_dict[strand] = []
    for seed in strand_colors_dict:
        strand_colors_dict[seed].append(seed)
    colored_strands = []
    for s in seeds:
        colored_strands.append(s)
    new_coloring = True
    while new_coloring:
        new_coloring = False
        for seed in strand_colors_dict:
            for strand in strand_colors_dict[seed]:
                for crossing in knot_dict[strand][1]:
                    if crossing[0] in colored_strands and crossing[1] not in colored_strands:
                        color = find_color(crossing[0], strand_colors_dict)
                        strand_colors_dict[color].append(crossing[1])
                        colored_strands.append(crossing[1])
                        new_coloring = True
                    elif crossing[0] not in colored_strands and crossing[1] in colored_strands:
                        color = find_color(crossing[1], strand_colors_dict)
                        strand_colors_dict[color].append(crossing[0])
                        colored_strands.append(crossing[0])
                        new_coloring = True
    return strand_colors_dict


def is_colored(strand, strand_colors_dict):
    '''
    Determines if a strand is currently colored.

    Input:
        strand: A char representing a strand in a knot diagram
        strand_colors_dict: A dictionary whose keys are our seed strands and whos values are lists of strands which are
            the same color as the key. Note each value contains a character representing its key.
            Strand_color_dict is of the form
            d_k = {
                    A: ['A', ...]
                    B: ['B', ...]
                    .
                    .
                },
    '''
    for color in strand_colors_dict:
        if strand in strand_colors_dict[color]:
            return True
    return False


def count_multicolored_crossings(strand_colors_dict, knot_dict):
    '''
    Given two dictionaries, one of which represents a maximal extension of a set of seeds, this function counts the
    number of multicolored crossings resulting from the maximal extension
    Input:
        strand_colors_dict: A dictionary where the keys are seed strands and the values are a list of
            characters representing the strands that are the same color as the seed
        knot_dict: A dictionary with strands as keys and a list of crossings for which that key is an over strand, as
            output from create_knot_dictionary
    Output:
        n_multicolored_crossings: An integer representing the number of multicolored crossings in our maximal extension
    '''
    n_multicolored_crossings = 0
    for color in strand_colors_dict:
        for strand in strand_colors_dict[color]:
            for crossing in knot_dict[strand][1]:
                if is_colored(crossing[0], strand_colors_dict) and is_colored(crossing[1], strand_colors_dict):
                    if crossing[1] not in strand_colors_dict[find_color(crossing[0], strand_colors_dict)]:
                        n_multicolored_crossings += 1
    return n_multicolored_crossings


def count_separate_knot(strand_colors_dict, knot_dict):
    '''
    Input:
        strand_colors_dict: A dictionary where the keys are seed strands and the values are a list of
            characters representing the strands that are the same color as the seed
        knot_dict: A dictionary with strands as keys and a list of crossings for which that key is an over strand, as
            output from create_knot_dictionary
    Output:
        this will return 1 if there are two separating knots, and 0 otherwise.
    '''
    num_colors = len(strand_colors_dict)
    if num_colors >= 2:
        num_separate_knots = 0
        for color in strand_colors_dict:
            list_strands_this_color = strand_colors_dict[color]
            # initialize: first strand in this color
            first_strand_letter = list_strands_this_color[0]
            concatenating = knot_dict[first_strand_letter][0]
            start_number_concatenating = concatenating[0]
            current_end_number_concatenating = concatenating[-1]
            list_strands_this_color.remove(first_strand_letter)
            number_strands_left = len(list_strands_this_color)
            while number_strands_left >= 1:
                for strand in list_strands_this_color:
                    current_strand_corresponding_list_numbers = knot_dict[strand][0]
                    start_number_current_strand = current_strand_corresponding_list_numbers[0]
                    # end current strand
                    end_number_current_strand = current_strand_corresponding_list_numbers[-1]
                    if start_number_current_strand == current_end_number_concatenating:
                        concatenating += current_strand_corresponding_list_numbers[1:]
                        start_number_concatenating = concatenating[0]
                        current_end_number_concatenating = concatenating[-1]
                        list_strands_this_color.remove(strand)
                        number_strands_left = len(list_strands_this_color)
                    elif end_number_current_strand == start_number_concatenating:
                        concatenating = current_strand_corresponding_list_numbers + concatenating[1:]
                        start_number_concatenating = concatenating[0]
                        current_end_number_concatenating = concatenating[-1]
                        list_strands_this_color.remove(strand)
                        number_strands_left = len(list_strands_this_color)
                # end for
            # done all strands
            start_number_concatenating = concatenating[0]
            end_number_concatenating = concatenating[-1]
            if start_number_concatenating == end_number_concatenating:
                num_separate_knots += 1
                separating_knot_list_number = concatenating[:-1]
                # here we want to check if over strands are colored
                list_positive_nodes = []
                for idx in separating_knot_list_number:
                    if idx < 0:
                        list_positive_nodes.append(-idx)
                # done check over strands
                list_colored_numbers = ()
                for idx_color in strand_colors_dict:
                    this_colored_strand_number = knot_dict[idx_color][0]
                    list_colored_numbers += this_colored_strand_number
                    for strand_in_this_branch in strand_colors_dict[idx_color]:
                        this_colored_strand_number = knot_dict[strand_in_this_branch][0]
                        list_colored_numbers += this_colored_strand_number
                set_all_colored_nodes = list(set(list_colored_numbers))
                # check if positive nodes are colored
                num_positive_node = len(list_positive_nodes)
                count_positive_colored = 0
                for idx_positive_node in list_positive_nodes:
                    if idx_positive_node in set_all_colored_nodes:
                        count_positive_colored += 1
                if count_positive_colored == num_positive_node:
                    # done check positive nodes colored
                    return 1
    return 0


def calc2(knot_dict, strands):
    '''
    Note this implementation depends on knowing before hand that the Gauss code is of a bridge number four knot. Moreover,
    the Gauss code represents a diagram that actuall realizes Wirtinger number four.

    input:
        raw_gauss_code: A list of characters representing a Gauss code.

    output:
        An upper bound on the Gabai width
    '''
    for s in knot_dict:
        strands.append(s)
    seeds_set = get_seeds(strands, 3)
    # pick 3 strands out of n strands
    for seeds in seeds_set:
        strand_colors_dict = maximally_extend(seeds, knot_dict)
        n_multicolored_crossings = count_multicolored_crossings(strand_colors_dict, knot_dict)
        n_count_separate_knot = count_separate_knot(strand_colors_dict, knot_dict)
        if n_multicolored_crossings > 0 or n_count_separate_knot == 1:
            colored_set = []
            for keys in strand_colors_dict:
                for s in strand_colors_dict[keys]:
                    colored_set.append(s)
            for potential_seed in strands:
                if potential_seed not in colored_set:
                    seed_addition = (potential_seed,)
                    new_seeds = seeds + seed_addition
                    new_strand_colors_dict = maximally_extend(new_seeds, knot_dict)
                    new_colored_set = []
                    for new_keys in new_strand_colors_dict:
                        for t in new_strand_colors_dict[new_keys]:
                            new_colored_set.append(t)
                    if set(new_colored_set) == set(strands):
                        return 6
    return 8


def main1link():
    code_list = [[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]
    knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(code_list)
    if len(seed_strand_set) == 4:
        transpositions = sym_hm.sym_group_crafter()
        hmorph, sym_gen_set = sym_hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, transpositions)
        if hmorph:
            lower_bound_num_colors = len(sym_gen_set)
            if lower_bound_num_colors == 4:
                output_6or8 = calc2(knot_dict, list(seed_strand_set))
                print("\nRESULT for code list", code_list, "\nWirtinger Trunk is ", output_6or8)
        else:
            print("Not good link.")


def maincsv():
    # prepare for output
    count_num_colors_4_good = 0
    count_output_6 = 0
    count_output_8 = 0
    list_good_links = []
    list_trunk = []

    file_path = '12in.xls'
    # 12in: short

    # file_path = '13in.xls'

    # file_path = '14in1.xls'
    # file_path = '14in2.xls'
    # 14in1 and 2: very long

    # file_path = 'Links.xls'
    # Links: for 2-11: short

    df = pd.read_excel(file_path)
    df = df.iloc[:, 2]

    int_list = []
    for idx in range(len(df)):
        t2 = []
        row_list = df.loc[idx].split(";")
        for my_list in row_list:
            t3 = [int(kdx) for kdx in my_list.split(",")]
            t2.append(t3)
        int_list.append(t2)

    # for testing:
    # for code_list in int_list[1:12]:
    for code_list in int_list:
        knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(code_list)
        if len(seed_strand_set) == 4:
            transpositions = sym_hm.sym_group_crafter()
            hmorph, sym_gen_set = sym_hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, transpositions)
            if hmorph:
                lower_bound_num_colors = len(sym_gen_set)
                if lower_bound_num_colors == 4:
                    count_num_colors_4_good += 1
                    output_6or8 = calc2(knot_dict, list(seed_strand_set))
                    print("\nRESULT for code list", code_list, "\nWirtinger Trunk is ", output_6or8)
                    if output_6or8 == 6:
                        count_output_6 += 1
                    if output_6or8 == 8:
                        count_output_8 += 1
                    list_good_links.append(code_list)
                    list_trunk.append(output_6or8)
            else:
                print("Not good link.")

    print("total numbers links we run", len(int_list))
    print("total numbers links with EXACTLY num colors 4 ", count_num_colors_4_good)
    print("total numbers links with output 6 ", count_output_6)
    print("total numbers links with output 8 ", count_output_8)

    output_links_trunks = pd.DataFrame({'list_good_links': list_good_links, 'list_trunk': list_trunk})
    output_links_trunks.to_excel('file_12in_output_links_trunks.xlsx', sheet_name='sheet1', index=False)
    # output_links_trunks.to_excel('file_13in_output_links_trunks.xlsx', sheet_name='sheet1', index=False)
    # output_links_trunks.to_excel('file_14in1_output_links_trunks.xlsx', sheet_name='sheet1', index=False)
    # output_links_trunks.to_excel('file_14in2_output_links_trunks.xlsx', sheet_name='sheet1', index=False)
    # output_links_trunks.to_excel('file_Links_output_links_trunks.xlsx', sheet_name='sheet1', index=False)

# maincsv()
main1link()
