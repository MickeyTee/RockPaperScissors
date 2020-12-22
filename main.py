import random


def print_instructions():
    """Prints the instructions of the game."""

    # Print a "title screen"
    print("Welcome to...\n"+
            " ___           _\n" +
            "| _ \ ___  __ | |__\n" +
            "|   // _ \\/ _|| / /\n" +
            "|_|_\\\\___/\__||_\_\\\n" +
            "    ___        _ __\n" +
            "   | _ \ __ _ | '_ \ ___  _ _\n" +
            "   |  _// _` || .__// -_)| '_|\n" +
            "   |_|  \__/_||_|   \___||_|\n" +
            "        ___      _\n" +
            "       / __| __ (_) ___ ___ ___  _ _  ___\n" +
            "       \__ \/ _|| |(_-/(_-// _ \| '_|(_-/\n" +
            "       |___/\__||_|/__//__/\___/|_|  /__/\n")

    # Print some instructions
    print("Welcome to the schoolyard! In this game, players simultaneously \"throw\" either rock, paper, or scissors",
          "by making a shape with their hands. In this version, you'll play the computer (who has no hands, so you'll",
          "just have to use your imagination). Rock beats scissors, scissors beats paper, and paper beats rock.",
          "\nGood luck!")

    return None


def get_game_length():
    """Asks the player what format of game they'd like to play (best of 5, 7, 11, or 15) and returns the player
    selection as an integer."""

    choice_string = input("You can play a match in four possible formats. Best of 5, 7, 11, or 15. Please enter the" +
                          " format of match you'd like to play (enter only the numeric digits):")

    # Use an infinite loop with try except blocks to guarantee valid input
    while True:
        try:
            # Check to see if the response is in the allowed game lengths
            if int(choice_string) in (5, 7, 11, 15):
                # If it is, set the choice variable and break the loop
                choice = int(choice_string)
                break
            # If it isn't in the allowed game lengths, ask again
            else:
                choice_string = input("Invalid input. Please enter 5, 7, 11, or 15.")
        # Catch any value errors and ask again
        except ValueError:
            choice_string = input("Invalid input. Please enter 5, 7, 11, or 15.")

    # The score limit for any Best of X is (X + 1) / 2, so return that
    return (choice + 1) / 2


def check_match(computer_score, player_score, score_limit):
    """Checks to see if the score limit for the match has been reached and returns True if it has and False if it
    hasn't."""

    # If the computer has hit the score limit, say so and set score_reached to true
    if computer_score >= score_limit:
        print("The computer has reached", str(score_limit), "points and wins the match!")
        score_reached = True
    # Do the same for the player
    elif player_score >= score_limit:
        print("You have reached", str(score_limit), "points and win the match!")
        score_reached = True
    # Otherwise just return False
    else:
        score_reached = False

    return score_reached


def computer_move(move_list):
    """Determines the move the computer will make and returns the move as a string. The basic strategy is to check the
    last three moves the player made and then go back over the last 100 moves the player made to look for that same
    sequence of three moves, then guess what their next move will be based on past behavior.
    """

    # Create a dictionary to make converting randint to RPS a little easier
    move_dict = {1: "Rock", 2: "Paper", 3: "Scissors"}
    # Get the length of the move list (purely for readability later)
    list_length = len(move_list)

    # Start by randomly select an integer from 1-3 and picking that value in the move dictionary
    move_int = random.randint(1, 3)
    move_choice = move_dict[move_int]

    # If there have been at least 4 moves, check if we can do better
    if len(move_list) >= 4:

        # Check whatever the last three moves were
        last_three = [move_list[list_length - 3], move_list[list_length - 2], move_list[list_length - 1]]

        # Initialize some counter variables
        rock_cnt = pap_cnt = sci_cnt = 0

        # Iterate over the last 100 moves (if they exist) to find every instance where those three moves appeared
        # in the same sequence
        for i in range(max(3, list_length - 6), list_length):

            # For every i, if the last three moves match our CURRENT last three moves, increment the appropriate counter
            if [move_list[i - 3], move_list[i - 2], move_list[i - 1]] == last_three:
                if move_list[i] == "Rock":
                    # Let's also penalize older moves by multiplying them by a "decay" factor based on i
                    rock_cnt += 1 * (i ** 0.5) / 10
                elif move_list[i] == "Paper":
                    pap_cnt += 1 * (i ** 0.5) / 10
                elif move_list[i] == "Scissors":
                    sci_cnt += 1 * (i ** 0.5) / 10

        # If the move sequence has never appeared before, just use our random move from before
        if max(rock_cnt, pap_cnt, sci_cnt) == 0:
            pass
        # Otherwise pick whatever has happened the most before
        else:
            # If rock_cnt is the max (or tied for max) just throw paper
            if max(rock_cnt, pap_cnt, sci_cnt) == rock_cnt:
                move_choice = "Paper"
            # If pap_cnt is the max (or tied for max) just throw scissors
            elif max(rock_cnt, pap_cnt, sci_cnt) == pap_cnt:
                move_choice = "Scissors"
            # Otherwise scissors must be the most observed, so throw rock
            else:
                move_choice = "Rock"

    return move_choice


def player_move():
    """Asks the player what move they'd like to make, attempting to handle input errors in the process and returning
    the selected move as a string."""

    # Get some input from the player to determine which RPS move they'd like to make
    choice_string = input("For this turn,you can play [R]ock, [P]aper, or [S]cissors by typing the first letter. " +
                          "Please enter the choice of move you'd like to make this turn:\n")

    # Use an infinite loop with try except blocks to guarantee valid input
    while True:
        try:
            # Accept any string starting with the first (case-insensitive) letter of a valid choice
            if choice_string[0].upper() == 'R':
                move_choice = "Rock"
                break
            elif choice_string[0].upper() == 'P':
                move_choice = "Paper"
                break
            elif choice_string[0].upper() == 'S':
                move_choice = "Scissors"
                break
            # Otherwise ask again
            else:
                choice_string = input("Invalid input. Please enter [R]ock, [P]aper, or [S]cissors.")
        # Catch any instances where the player just hits Enter and ask again
        except IndexError:
            choice_string = input("Invalid input. Please enter [R]ock, [P]aper, or [S]cissors.")

    return move_choice


def handle_moves(comp_choice, player_choice,  comp_score, player_score):
    """Takes the players move and the computers move and determines who, if anyone, has scored a point, then returns
    the updated score for the player and computer.
    """
    # Set a container variable
    player_wins = None
    # If the two choices are the same, it's a draw (we handle this later).
    if player_choice == comp_choice:
        pass
    # Otherwise, there's no draw. Check if the player played rock...
    elif player_choice == "Rock":
        # ...if they did, check if the computer player scissors and the player lost
        if comp_choice == "Scissors":
            player_wins = True
        # ...otherwise they must have played scissors and the player won
        else:
            player_wins = False
    # Repeat for scissors
    elif player_choice == "Scissors":
        if comp_choice == "Paper":
            player_wins = True
        else:
            player_wins = False
    # Repeat for paper
    elif player_choice == "Paper":
        if comp_choice == "Rock":
            player_wins = True
        else:
            player_wins = False

    # If player_wins is still None, we must have drawn. Print a message
    if player_wins is None:
        print("Draw! Both players threw", player_choice, "and no points are awarded.")
    # If player_wins is False, computer won. Print a message and increment their score
    elif not player_wins:
        print(comp_choice, "beats", player_choice, "! Your opponent wins a point!")
        comp_score += 1
    # Otherwise player_wins must be True.
    else:
        print(player_choice, "beats", comp_choice, "! You win a point!")
        player_score += 1

    return comp_score, player_score


def check_play_again():
    """Checks if the player would like to play another match and returns True if they want to play again
    and False if they don't."""

    # Ask the player if they'd like to play again
    play_again = input("Would you like to play again? Please enter [Y] to play again, and [N] to quit.")

    # Use a while loop to force valid input
    while True:
        try:
            # Accept any response where the first letter is valid
            if play_again[0].upper() == 'Y':
                # Set the return variable to True if they'd like to play again and break
                play_choice = True
                break
            elif play_again[0].upper() == 'N':
                # Set the returned variable to False if they would not like to play again and break
                play_choice = False
                break
            # Otherwise ask again
            else:
                play_again = input("Invalid input. Please enter [Y] to play again, and [N] to quit.")
        # Handle cases where the player just hits Enter and there is no index 0
        except IndexError:
            play_again = input("Invalid input. Please enter [Y] to play again, and [N] to quit.")

    return play_choice


def main():

    # Set a flag variable for the game running or not
    game_running = True
    # Create an empty list to populate with player moves for the computer to scan
    move_list = []
    # Print titles
    print_instructions()

    # Loop the game as long as game_running is True
    while game_running:
        # Initialize scores
        computer_score = player_score = 0
        # Select the score limit
        score_limit = get_game_length()
        # Set a flag variable for the match being over or not
        match_over = False

        # Loop the match as long as match_over is False
        while not match_over:
            # Determine the computer move
            computer_choice = computer_move(move_list)
            # Ask the player for their move
            player_choice = player_move()
            # Add the player's move selection to the move list
            move_list.append(player_choice)
            # Print some feedback for the player.
            print("The computer threw", computer_choice, "and you threw", player_choice + ".")
            # Update scores.
            computer_score, player_score = handle_moves(computer_choice, player_choice, computer_score, player_score)
            # Print some more feedback
            print("The score is", player_score, " - ", computer_score)
            # Check if the match is over or not
            match_over = check_match(computer_score, player_score, score_limit)

        # Ask the player if they'd like to play again
        game_running = check_play_again()

    # Print a little goodbye
    print("Thanks for playing! Goodbye!")


if __name__ == '__main__':
    main()
