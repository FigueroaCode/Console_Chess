from package.Chess_board import *

#    Main
board = Chess_board()
board.print_board()
checkmate = False
isBlack = False
color = "White"
check = False
while(not checkmate):
        #Ask for input
    print("\n\n"+ color +"'s Move. Which Piece?")
    try:
        current_x = input("Location(Letter): ").upper()
        current_y = int(input("Location(Number): "))
        print("\n To where?")
        x = input("Location(Letter): ").upper()
        y = int(input("Location(Number): "))

        #Update Board 
        board.save_board()
        update = board.updateBoard(isBlack,current_x,current_y,x,y)
        if  update and board.in_check(isBlack):
            print('Still in check')
            board.revert_board()
            checkmate = board.is_checkmated(isBlack,current_y,current_x,y,x)
            print('Checkmate: ' + str(checkmate))
        elif update:
            board.promotion(color,current_y,current_x,y,x)
            if isBlack:
                isBlack = False
                color = "White"
            else:
                isBlack = True
                color = "Black"
            check = board.in_check(isBlack)
            if check:
                if board.is_checkmated(isBlack,current_y,current_x,y,x):
                    checkmate = True
                    print('Checkmate')
                else:
                    print('Check')
        
        board.print_board()
        board.print_captured()

    except:
        print('Invalid Input. Try again.')

#NOTE: En passant featureless Chess
