import os  # used in MatrixCreationFile
import numpy as np  # used in matrixCasual


def MatrixCreationFile(fileName='inputMatrixCreation.txt'):
    """ Reads the file containing information about creation of the matrix and game mode """

    file_path = os.path.join('D:\Raccolta\Progetti\Advanced Py\Row Column Game', 'inputMatrixCreation.txt')
    with open(file_path, 'rt') as file:
        file_vector = []
        for line in file:
            file_vector.append(line)  # creates a vector containing the file
        f_rows = int(file_vector[2][8:-1].strip())  # extract the rows number from the 3° line of the file
        f_columns = int(file_vector[3][11:-1].strip())  # extract the columns number from the 4° line of the file
        game_mode = file_vector[11][0]  # extract the mode number from the 12° line of the file
    return f_rows, f_columns, game_mode


def matrixCasual(rows_f, columns_f):
    """ Creates a matrix with casual numbers from one to nine """
    rng = np.random.default_rng()
    matrix_f = rng.integers(1, 10, (rows_f, columns_f))
    return matrix_f


def printMatrix(matrix_f):
    """ Prints on the console the matrix with the remaining numbers and a matrix with only the possible choices
     it uses external variable columns"""
    str_matrix = matrix_f.astype('U')  # converts the matrix values into strings
    for row, line in enumerate(str_matrix):  # erases all non-selectable items
        for column, num in enumerate(line):
            if int(num) <= 0:  # every non-selectable number is negative or 0 in the program logic
                str_matrix[row, column] = ' '
    print('La matrice:\n')
    ran = [i for i in range(columns)]  # indexes for the columns
    ran2 = ['_' for i in range(columns)]
    print('/', ' ', *ran)
    print(' ', ' ', *ran2)
    for index, line in enumerate(str_matrix):  # indicatore riga
        print(index, '|', *line)


def possibilities(matrix_f, coord_f):
    """ Returns the coordinates numbers in the same row/column as the coord input """

    choice_list_f = []
    row, column = coord_f
    for index, num in enumerate(matrix_f[row]):
        if num > 0:
            choice_list_f.append((row, index))
    for index, num in enumerate(matrix_f[:, column]):
        if num > 0:
            choice_list_f.append((index, column))
    return choice_list_f


def printMatrixAndPossibilities(matrix_f, last_move=None):
    """ prints on the console the matrix with the remaining numbers and a matrix with only the possible choices
     It uses external variable columns"""
    str_matrix = matrix_f.astype('U')  # converts the matrix values into strings
    for row, line in enumerate(str_matrix):  # erases all non-selectable items
        for column, num in enumerate(line):
            if int(num) <= 0:  # every non-selectable number is negative or 0 in the program logic
                str_matrix[row, column] = '.'
            if (row, column) == last_move: str_matrix[row, column] = '/' #the last_move is in the parenthesis

    str_matrix_possibilities = np.copy(str_matrix)  # copy for the possibilities matrix
    choices = possibilities(matrix_f, coord)
    for i in range(rows):  # erase every number that is not in the same row/column
        for j in range(columns):
            if (i, j) not in choices and (i,j) != last_move:
                str_matrix_possibilities[i, j] = ' '  # erase means it is not visualized on console
    # Visualization
    print('La prima matrice è quella completa, mentre la seconda è quella delle scelte possibili\n')
    ran = [i for i in range(columns)]
    ran2 = ['_' for i in range(columns)]
    print('/', ' ', *ran, '  ', '/', ' ', *ran)
    print(' ', ' ', *ran2, '  ', ' ', ' ', *ran2)
    for i_row in range(rows):
        print(i_row, '|', *str_matrix[i_row], '  ', i_row, '|', *str_matrix_possibilities[i_row])


def askForCoordinates(choice_list_f):
    """ asks for number's coordinates and checks the input """

    coord_input = input('Enter Row,Column:\n')  # console input
    try:  # transforms the input into a coordinates tuple
        coord_input = coord_input.split(',')
        row = int(coord_input[0].strip())
        col = coord_input[1]
        col.replace(',', '')
        coord_f = (row, int(col.strip()))
        if coord_f in choice_list_f:
            return coord_f  # return (row,column) tuple
        else:
            print('You have to select a number in the same row or column of the previous number')
            return askForCoordinates(choice_list_f)
    except ValueError:
        print('!!Wrong syntax, retry!!')
        return askForCoordinates(choice_list_f)
    except IndexError:
        print('!!Wrong syntax, retry!!')
        return askForCoordinates(choice_list_f)


def eraseNumber(matrix_f, coord_f):
    """ The selected number is transformed into negative, as it means it is not a possible choice
    The program returns the number corresponding to the selected coordinates """
    row, column = coord_f
    number_f = matrix_f[row, column]
    matrix_f[row, column] = -matrix_f[row, column]
    return number_f


def addNumber(matrix_f, coord_f):
    number = matrix_f[coord_f[0], coord_f[1]]  # matrix[raw , column]
    matrix_f[coord_f[0], coord_f[1]] = -matrix_f[coord_f[0], coord_f[1]]
    return number


def pointsDict(matrix_f):
    dic_f = {}
    for i in range(rows):
        for j in range(columns):
            dic_f[(i, j)] = matrix_f[i, j]
    return dic_f


def machine2(matrix_f,coord_f):
    """

    global lists:
     - follow_path: list useful in the creation of all_paths. Basically while machine2() is working this list
    captures the depth at witch machine arrived, so that when there are no more possibilities it is appended to
     all_pathways.
      - all_pathways: contains all the possible pathways through witch the game can evolve
      - skimmer: it is made to check if the followed path is the full path before it is attached to all_pathways
    """
    global follow_path,all_pathways, skimmer
    choice_list_f = possibilities(matrix_f,coord_f)
    follow_path.append(coord_f)
    while choice_list_f:
        coord_f_r = choice_list_f.pop()
        choice_list_f_r = possibilities(matrix_f.copy(), coord_f_r)
        eraseNumber(matrix_f, coord_f_r)

        if choice_list_f_r:
            coord_f_u = machine2(matrix_f.copy(), coord_f_r)
            if coord_f_u: addNumber(matrix_f, coord_f_u)

        else:  # TUTTA QUESTA PARTE POTREBBE ESSERE INUTILE
            print(follow_path, skimmer)
            if follow_path != skimmer:
                all_pathways.append(follow_path.copy())
                skimmer = all_pathways.copy()[:-1]
            addNumber(matrix_f, coord_f_r)
            return None
    if follow_path != skimmer:
        all_pathways.append(follow_path.copy())
    skimmer = follow_path.copy()[:-1]
    addNumber(matrix_f, coord_f)
    follow_path.pop()
    return coord_f


def path_final_score_dict_creator(all_pathways_f: {list}, value_dict_f: {dict}):
    """taking every single possible path from all_pathways, it converts the single coordinate into its value and then
    the program sum-subtract the value for every coordinate, repeated for the entire path. Then creates a dictionary
    where the key is the path and the value is the final result
    - Final result is calculated by subtracting the points during even turns and adding the points during odd turns
        as even turns are player turns and odd turns are machine ones"""
    path_final_resul_dict_f = {}  # the returned dictionary
    for path_f in all_pathways_f:
        t_path_f = tuple(path_f)  # transforms the path from a list to a tuple, as dict name cannot be a list
        path_final_resul_dict_f[t_path_f] = 0  # starts the points calculation
        for index_f,item2 in enumerate(t_path_f):
            if index_f % 2 == 0 or index_f == 0:  # not sure index_f is really needed
                path_final_resul_dict_f[t_path_f] = path_final_resul_dict_f[t_path_f] - value_dict_f[item2]
            else:
                path_final_resul_dict_f[t_path_f] = path_final_resul_dict_f[t_path_f] + value_dict_f[item2]
    return path_final_resul_dict_f


def playing():
    global path_values_dictionary, turn_counter
    list = []
    for path, final_score in path_values_dictionary.items():
        list.append(path[turn_counter])


'''Program structure'''

'''Matrix creation'''
rows, columns, game_mode = MatrixCreationFile()  # these values are fixed and not to be changed
matrix = matrixCasual(rows, columns)
choice_list = [(row, column)
               for row in range(rows)
               for column in range(columns)]  # creates the first choice list with every number in the matrix

if game_mode == '4':
    '''Game mode 4, player VS player (not required)'''
    player1_points = 0
    player2_points = 0
    player1_turn = True  # use: understand if is player1 turn or player2 turn
    printMatrix(matrix)
    while choice_list:

        if player1_turn:
            print('player1 turn')
        else:
            print('player2 turn')  # displays player turn

        coord = askForCoordinates(choice_list.copy())  # ask the player for cell coordinates and checks correctness

        if player1_turn:
            player1_points = player1_points + eraseNumber(matrix, coord)
        else:
            player2_points = player2_points + eraseNumber(matrix, coord)  # adds the point to the right player

        player1_turn = not player1_turn  # player turn change
        printMatrixAndPossibilities(matrix)  # visualize the playing field
        print(f'player1 points: {player1_points}, player2 points: {player2_points}')  # visualize player's points
        choice_list = possibilities(matrix, coord)  # refresh choice list to new possible choices

    '''Declare rightful winner'''
    if player1_points < player2_points:
        print('Player 2 wins!')
    elif player1_points > player2_points:
        print('Player 1 wins!')
    else:
        print('Draw!')

elif game_mode == '1':
    """ Game mode 1, player VS machine1
    the already existing variables are: rows, columns, matrix and choice_list
    How machine works:
    
    program structure:
        1) First Move: asks the player to do a first move
        2) Machine calculations: machine looks at all the possible paths creating all_pathways list and path values
            dictionary.
        3) Core game: the game moves on, the machine makes its move and then is player time. The cycle ends when the next 
            player has no more possible moves.
        4) Results: based on the points made results are displayed on the screen.
        """
    """1) first move"""
    values_dictionary = pointsDict(matrix)  # Just useful to use, not really fundamental
    points_player, points_machine = 0, 0  # initialization of point counters
    printMatrix(matrix)  # Prints the matrix so that the player can make the first move
    print("Let's play! -- Make the first move")  # self-explain
    coord = askForCoordinates(choice_list)  # look at the documentation
    points_player = points_player + eraseNumber(matrix, coord)  # look at the documentation, adds the cell value to pl_p
    """2) Machine calculations"""
    # seeking pathways
    follow_path, all_pathways, skimmer = [], [], [0]  # look at machine2() documentation
    machine2(matrix.copy(),coord)  # look at documentation, compiles all_pathways list
    # path - finalResult dictionary creation
    path_fs_dict = path_final_score_dict_creator(all_pathways, values_dictionary)  # look at documentation
    """3) Core game"""
    choice_list = possibilities(matrix, coord)
    turn_counter = 0
    while choice_list:
        turn_counter += 1
        if turn_counter % 2 != 0:
            # max in choice list is valued as double point in victory prob.
            max_poss_choice = [int(values_dictionary[nn])
                               for nn in choice_list]
            # machine choice
            win_numerator = [0 for i in range(len(choice_list))]  # creates a list that contains a counter for all
                # the win paths possible after the i'th choice (out of n choice from choice list)
            numerator = [0 for i in range(len(choice_list))]  # creates a list that counts all possible choices after
                # the machine choice
            for index,item in enumerate(choice_list):  # for every possible choice
                for key_path,final_score in path_fs_dict.items(): # takes the key path and fs
                    try:
                        if key_path[turn_counter] == item: # confronts the first coord of the path & if == item
                            numerator[index] += 1  # moves the counter in the i'th cell of the numerator
                            if final_score > 0:  # & if machine wins
                                win_numerator[index] += 1  # moves the counter in the i'th cell of the win_numerator
                            if index == max_poss_choice.index(max(max_poss_choice)):
                                win_numerator[index] +=1
                    except IndexError: continue
            win_probability = [win_numerator[i]/numerator[i] for i in range(len(win_numerator))]  # calculates the win
                # probability for every possible choice the machine has
            max_win_probability = win_probability.index(max(win_probability))  # finds the best choice for winning
            max_win_probability_coord = choice_list[max_win_probability]  # returns the coordinate for best choice
            coord = max_win_probability_coord  # just because the other commands have to work also for the player turn
            points_machine = points_machine + eraseNumber(matrix, coord)  # adds the point to the point counter

        else:
            # player turn
            printMatrixAndPossibilities(matrix, coord)
            if turn_counter != 1:  # print results and machine previous move
                print(f'Player points: {points_player}, Machine points: {points_machine} || '
                      f'Machine choice: {coord} & relative points {values_dictionary[coord]}')

            coord_player = askForCoordinates(choice_list)  # ask for coordinates
            points_player = points_player + eraseNumber(matrix, coord_player)  # erase the cell and sums the points

            coord = coord_player  # to create a necessary variable for functions: possibilities and printMatr...

        choice_list = possibilities(matrix,coord)

    # end while

    if points_player < points_machine:
        print(f'Machine wins! || Player points: {points_player}, Machine points: {points_machine}')
    elif points_player > points_machine:
        print(f'Player wins! || Player points: {points_player}, Machine points: {points_machine}')
    else:
        print(f'Draw! || Player points: {points_player}, Machine points: {points_machine}')

elif game_mode == '2':
    ''' Game mode 1, player VS machine1 '''
    ''' Machine1 works by selecting the higher number within the possible choices, then the program stops when there 
    are no more possible choices for the player/machine and gives the results'''
    '''The given variables are rows, columns, matrix and choice_list'''
    points_machine2 = 0
    points_machine1 = 0
    turn_counter = 0  # player plays odd turns while machine plays even turns
    printMatrix(matrix)
    while choice_list:

        turn_counter += 1  # turn counter

        if turn_counter % 2 != 0:  # player turn
            '''player turn: print results, ask for coordinates, then erase the cell, then sum the points'''

            if turn_counter != 1:  # print results and machine previous move
                print(f'Player points: {points_machine2}, Machine points: {points_machine1} || '
                      f'Machine choice: {max_number}, cell coordinates: {max_coord}')

            coord_player = askForCoordinates(choice_list)  # ask for coordinates
            points_machine2 = points_machine2 + eraseNumber(matrix, coord_player)  # erase the cell and sums the points

            coord = coord_player  # to create a necessary variable for functions: possibilities and printMatr...

        if turn_counter % 2 == 0:  # machine turn
            '''machine turn: select the higher number within the possibilities, erase the cell, then sum the points'''
            max_number = 0  # variable useful to establish the higher number within possibilities
            for index, coord_machine in enumerate(choice_list):  # for every possible choice...
                if matrix[coord_machine[0], coord_machine[1]] > max_number:  # asses if the number is the highest
                    max_number = matrix[coord_machine[0], coord_machine[1]]  # changes the max variable to new standard
                    max_coord = coord_machine  # changes coord to the maximum one
            points_machine1 = points_machine1 + eraseNumber(matrix, max_coord)

            coord = max_coord  # to create a necessary variable for functions: possibilities and printMatr...

        choice_list = possibilities(matrix, coord)  # refresh choice list to new possible choices
        printMatrixAndPossibilities(matrix)  # visualize game field

    if points_machine2 < points_machine1:
        print('Machine wins!')
    elif points_machine2 > points_machine1:
        print('Player wins!')
    else:
        print('Draw!')

elif game_mode == '3':
    """Game mode 3, machine1 VS machine2"""
    values_dictionary = pointsDict(matrix)
    points_machine1, points_machine2 = 0, 0
    turn_counter = 0  # machine2 plays odd turns while machine1 plays even turns
    printMatrix(matrix)
    while choice_list:

        if turn_counter % 2 == 0:  # machine turn
            '''machine1 turn: select the higher number within the possibilities, erase the cell, then sum the points'''
            max_number = 0  # variable useful to establish the higher number within possibilities
            for index, coord_machine in enumerate(choice_list):  # for every possible choice...
                if matrix[coord_machine[0], coord_machine[1]] > max_number:  # asses if the number is the highest
                    max_number = matrix[coord_machine[0], coord_machine[1]]  # changes the max variable to new standard
                    max_coord = coord_machine  # changes coord to the maximum one
            points_machine1 = points_machine1 + eraseNumber(matrix, max_coord)
            coord = max_coord  # to create a necessary variable for functions: possibilities and printMatr...
        if turn_counter == 0:
            follow_path, all_pathways, skimmer = [], [], [0]  # look at machine2() documentation
            machine2(matrix.copy(), coord)  # look at documentation, compiles all_pathways list

            # path - finalResult dictionary creation
            path_fs_dict = path_final_score_dict_creator(all_pathways, values_dictionary)  # look at documentation

        elif turn_counter % 2 != 0:  # player turn
            # machine choice
            win_numerator = [0 for i in range(len(choice_list))]  # creates a list that contains a counter for all
                # the win paths possible after the i'th choice (out of n choice from choice list)
            numerator = [0 for i in range(len(choice_list))]  # creates a list that counts all possible choices after
                # the machine choice
            for index,item in enumerate(choice_list):  # for every possible choice
                for key_path,final_score in path_fs_dict.items(): # takes the key path and fs
                    try:
                        if key_path[turn_counter] == item: # confronts the first coord of the path & if == item
                            numerator[index] += 1  # moves the counter in the i'th cell of the numerator
                            if final_score > 0:  # & if machine wins
                                win_numerator[index] += 1  # moves the counter in the i'th cell of the win_numerator
                    except IndexError: continue
            win_probability = [win_numerator[i]/numerator[i] for i in range(len(win_numerator))]  # calculates the win
                # probability for every possible choice the machine has
            max_win_probability = win_probability.index(max(win_probability))  # finds the best choice for winning
            max_win_probability_coord = choice_list[max_win_probability]  # returns the coordinate for best choice
            coord = max_win_probability_coord  # just because the other commands have to work also for the player turn
            points_machine2 = points_machine2 + eraseNumber(matrix, coord)  # adds the point to the point counter

        choice_list = possibilities(matrix, coord)  # refresh choice list to new possible choices
        turn_counter += 1  # turn counter

    printMatrix(matrix)
    if points_machine2 < points_machine1:
        print(f'Machine1 wins! || Machine1 points: {points_machine1}, Machine2 points: {points_machine2}')
    elif points_machine2 > points_machine1:
        print(f'Machine2 wins! || Machine1 points: {points_machine1}, Machine2 points: {points_machine2}')
    else:
        print('Draw!')

