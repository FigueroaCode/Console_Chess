from .Chess_pieces import Chess_pieces
import copy
#board
class Chess_board:
    pieces = Chess_pieces()
    #Set up board
    grid = [[pieces.get_black_piece(0), pieces.get_black_piece(1), pieces.get_black_piece(2),
             pieces.get_black_piece(3),pieces.get_black_piece(4),pieces.get_black_piece(2),
             pieces.get_black_piece(1),pieces.get_black_piece(0)],
            [pieces.get_black_piece(5),pieces.get_black_piece(5),pieces.get_black_piece(5),pieces.get_black_piece(5),pieces.get_black_piece(5),
             pieces.get_black_piece(5),pieces.get_black_piece(5),pieces.get_black_piece(5)],
            [pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty()],
            [pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty()],
            [pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty()],
            [pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty(),pieces.getEmpty()],
            [pieces.get_white_piece(5),pieces.get_white_piece(5),pieces.get_white_piece(5),pieces.get_white_piece(5),pieces.get_white_piece(5),
             pieces.get_white_piece(5),pieces.get_white_piece(5),pieces.get_white_piece(5)],
            [pieces.get_white_piece(0), pieces.get_white_piece(1), pieces.get_white_piece(2), pieces.get_white_piece(3),
             pieces.get_white_piece(4),pieces.get_white_piece(2),pieces.get_white_piece(1),pieces.get_white_piece(0)]]
    old_grid = copy.deepcopy(grid)
    #convert to board coordinates
    def convertY(self, y):
        return 8 - y
    def convert_letter(self, letter):
        letters = ['A','B','C','D','E','F','G','H']
        index = 0
        while(index < len(letters)):
            if letter == letters[index]:
                break;
            index +=1
        return (index)
    def save_board(self):
        self.old_grid = copy.deepcopy(self.grid)
    def revert_board(self):
        self.grid = copy.deepcopy(self.old_grid)
    def promotion(self,color, c_y,c_x,y,x):
        #get piece
        piece = self.grid[current_y][current_x][1]
        if color:#black
            if piece == self.pieces.get_black_piece(5)[1]:
                #if its a pawn
                if y == 7:
                    promoted = False
                    while(not promoted):
                        #Ask which piece they want
                        options = [self.pieces.get_black_piece(3),self.pieces.get_black_piece(0),self.pieces.get_black_piece(1),self.pieces.get_black_piece(2)]
                        promo = input('Which piece do you want to turn it into?(BQ,Br,Bk,Bb )')
                        for i in options:
                            if promo == i[1]:
                                self.grid[y][x] = i
                                promoted = True
                        if not promoted:
                            print('Invalid Input')
        else:#white
            if piece == self.pieces.get_black_piece(5)[1]:
                #if its a pawn
                if y == 0:
                    promoted = False
                    while(not promoted):
                        #Ask which piece they want
                        options = [self.pieces.get_white_piece(3),self.pieces.get_white_piece(0),self.pieces.get_white_piece(1),self.pieces.get_black_piece(2)]
                        promo = input('Which piece do you want to turn it into?(WQ,Wr,Wk,Wb )')
                        for i in options:
                            if promo == i[1]:
                                self.grid[y][x] = i
                                promoted = True
                        if not promoted:
                            print('Invalid Input')
    #---------------------------------------------check for check-------------------------------------
    def in_check(self,color):
        #make list for storing which pieces are checking king, and their path
        if not color:#whites Turn
            #white king
            kings_position = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(4)[1])
            #black rooks
            rook_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(0)[1])
            #black bishops
            bishop_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(2)[1])
            #black queen
            queens_position = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(3)[1])
            #black knights
            knight_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(1)[1])

            #time for the actual work
            #Rook 1 movement
            if len(rook_positions) > 0 and self.pieces.rook_movement(self.grid,color, rook_positions[0], rook_positions[1], kings_position[0], kings_position[1]):
                return True
            #Rook 2 movement
            if len(rook_positions) > 2 and self.pieces.rook_movement(self.grid,color, rook_positions[2], rook_positions[3], kings_position[0], kings_position[1]):
                return True
            #Bishop 1 movement
            if len(bishop_positions) > 0 and self.pieces.bishop_movement(self.grid, bishop_positions[0], bishop_positions[1], kings_position[0], kings_position[1]):
                return True
            #Bishop 2 movement
            if len(bishop_positions) > 2 and self.pieces.bishop_movement(self.grid, bishop_positions[2], bishop_positions[3], kings_position[0], kings_position[1]):
                return True
            #Knight 1 movement
            if len(knight_positions) > 0 and self.pieces.knight_movement(knight_positions[0], knight_positions[1], kings_position[0], kings_position[1]):
                return True
            #Knight 2 movement
            if len(knight_positions) > 2 and self.pieces.knight_movement(knight_positions[2], knight_positions[3], kings_position[0], kings_position[1]):
                return True
            #Queen Movement
            if len(queens_position) > 0 and self.pieces.queen_movement(self.grid, color,queens_position[0], queens_position[1], kings_position[0], kings_position[1]):
                return True
            #Pawn movement
            #if theres a black pawn at top right or left of king
            if kings_position[0] > 0 and kings_position[1] > 0 and self.grid[kings_position[0]-1][kings_position[1]-1][1] == self.pieces.get_black_piece(5)[1]:
                return True
            if kings_position[0] > 0 and kings_position[1] < 7 and self.grid[kings_position[0]-1][kings_position[1]+1][1] == self.pieces.get_black_piece(5)[1]:
                return True
        else:#Blacks Turn
            #black king
            kings_position = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(4)[1])
            #white rooks
            rook_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(0)[1])
            #white bishops
            bishop_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(2)[1])
            #white queen
            queens_position = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(3)[1])
            #white knights
            knight_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(1)[1])

             #time for the actual work
            #Rook 1 movement
            if len(rook_positions) > 0 and self.pieces.rook_movement(self.grid, color,rook_positions[0], rook_positions[1], kings_position[0], kings_position[1]):
                return True
            #Rook 2 movement
            if len(rook_positions) > 2 and self.pieces.rook_movement(self.grid,color, rook_positions[2], rook_positions[3], kings_position[0], kings_position[1]):
                return True
            #Bishop 1 movement
            if len(bishop_positions) > 0 and self.pieces.bishop_movement(self.grid, bishop_positions[0], bishop_positions[1], kings_position[0], kings_position[1]):
                return True
            #Bishop 2 movement
            if len(bishop_positions) > 2 and self.pieces.bishop_movement(self.grid, bishop_positions[2], bishop_positions[3], kings_position[0], kings_position[1]):
                return True
            #Knight 1 movement
            if len(knight_positions) > 0 and self.pieces.knight_movement(knight_positions[0], knight_positions[1], kings_position[0], kings_position[1]):
                return True
            #Knight 2 movement
            if len(knight_positions) > 2 and self.pieces.knight_movement(knight_positions[2], knight_positions[3], kings_position[0], kings_position[1]):
                return True
            #Queen Movement
            if len(queens_position) > 0 and self.pieces.queen_movement(self.grid,color, queens_position[0], queens_position[1], kings_position[0], kings_position[1]):

                return True
            #Pawn Movement
            if kings_position[0] > 0 and kings_position[1] > 0 and self.grid[kings_position[0]-1][kings_position[1]-1][1] == self.pieces.get_white_piece(5)[1]:
                return True
            if kings_position[0] > 0 and kings_position[1] < 7 and self.grid[kings_position[0]-1][kings_position[1]+1][1] == self.pieces.get_white_piece(5)[1]:
                return True
        return False
    #end of check
    #------------------------------------------check for checkmate----------------------------------------
    def is_checkmated(self, color, current_y, current_x, y, x):
        check = [True,True,True,True,True,True,True,True]
        self.save_board()
        if color:
            #kings movements IMPROVE later with a loop. Can be done in like 2 lines
            #black king
            kings_position = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(4)[1])
            #check all the kings possible moves
            if (kings_position[0] + 1)  <= 7 and (kings_position[1]+1) <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] + 1, kings_position[1] + 1):
                check[0] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] - 1)  >= 0  and (kings_position[1] + 1)  <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] - 1, kings_position[1] + 1):
                check[1] = self.in_check(color)
                self.revert_board()
            if (kings_position[1] - 1)  >= 0  and (kings_position[0] + 1)  <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] + 1, kings_position[1] - 1):
                check[2] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] - 1)  >= 0  and (kings_position[1] + 1)  >= 0 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] - 1, kings_position[1] - 1):
                check[3] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] + 1) <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] + 1, kings_position[1]):
                check[4] = self.in_check(color)
                self.revert_board()
            if (kings_position[1] + 1) <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0], kings_position[1] + 1):
                check[5] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] - 1) >= 0 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] - 1, kings_position[1]):
                check[6] = self.in_check(color)
                self.revert_board()
            if (kings_position[1] - 1) >= 0 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0], kings_position[1] - 1):
                check[7] = self.in_check(color)
                self.revert_board()
        else:
            #white king
            kings_position = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(4)[1])
            #check all the kings possible moves
            if (kings_position[0] + 1)  <= 7 and (kings_position[1]+1) <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] + 1, kings_position[1] + 1):
                check[0] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] - 1)  >= 0  and (kings_position[1] + 1)  <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] - 1, kings_position[1] + 1):
                check[1] = self.in_check(color)
                self.revert_board()
            if (kings_position[1] - 1)  >= 0  and (kings_position[0] + 1)  <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] + 1, kings_position[1] - 1):
                check[2] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] - 1)  >= 0  and (kings_position[1] + 1)  >= 0 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] - 1, kings_position[1] - 1):
                check[3] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] + 1) <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] + 1, kings_position[1]):
                check[4] = self.in_check(color)
                self.revert_board()
            if (kings_position[1] + 1) <= 7 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0], kings_position[1] + 1):
                check[5] = self.in_check(color)
                self.revert_board()
            if (kings_position[0] - 1) >= 0 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0] - 1, kings_position[1]):
                check[6] = self.in_check(color)
                self.revert_board()
            if (kings_position[1] - 1) >= 0 and self.move_piece(color, kings_position[0], kings_position[1], kings_position[0], kings_position[1] - 1):
                check[7] = self.in_check(color)
                self.revert_board()
        # now check if any piece can block, find out which pieces are checking king
        #use whiteRanges or blackRanges to check for movement
        if color:#black king needs to get out of danger, so check for black pieces that can block
            #black rooks
            rook_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(0)[1])
            #black bishops
            bishop_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(2)[1])
            #black queen
            queens_position = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(3)[1])
            #black knights
            knight_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(1)[1])
            #black pawns
            pawn_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(5)[1])
            #list of positions
            positions = [rook_positions,bishop_positions,queens_position,knight_positions, pawn_positions]
            
            threats = self.get_threats(color)
            #check for capture first
            #check which piece is checking
            #see if black piece can capture
            index = 0
            for threat in threats:#index 1 is the current position in threat
                if len(positions[index]) > 0:
                    check.append(not self.inRange(color, positions[index][0], positions[index][1], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                if len(positions[index]) > 2:
                    check.append(not self.inRange(color, positions[index][2], positions[index][3], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                #for pawns
                if len(positions[index]) > 4:# 3 pawns
                    check.append(not self.inRange(color, positions[index][4], positions[index][5], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                if len(positions[index]) > 6:# 4 pawns
                    check.append(not self.inRange(color, positions[index][6], positions[index][7], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                if len(positions[index]) > 8:# 5 pawns
                    check.append(not self.inRange(color, positions[index][8], positions[index][9], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                if len(positions[index]) > 10:# 6 pawns
                    check.append(not self.inRange(color, positions[index][10], positions[index][11], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                if len(positions[index]) > 12:# 7 pawns
                    check.append(not self.inRange(color, positions[index][12], positions[index][13], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                if len(positions[index]) > 14:# 8 pawns
                    check.append(not self.inRange(color, positions[index][14], positions[index][15], threat[1][0],threat[1][1]))
                    if not check[len(check)-1]:#if its false then it did capture
                        self.pieces.pop_captured_white()
                index += 1
            #blocking
            for x in threats:
                for threat in x[2]:
                    #rook 1
                    if len(rook_positions) > 0:
                        check.append(not self.pieces.rook_movement(self.grid, color,rook_positions[0], rook_positions[1], threat[0], threat[1]))
                    #rook 2
                    if len(rook_positions) > 2:
                        check.append(not self.pieces.rook_movement(self.grid, color,rook_positions[2], rook_positions[3], threat[0], threat[1]))
                    #bishop 1
                    if len(bishop_positions) > 0:
                        check.append(not self.pieces.bishop_movement(self.grid, bishop_positions[0], bishop_positions[1], threat[0], threat[1]))
                    #bishop 2
                    if len(bishop_positions) > 2:
                        check.append(not self.pieces.bishop_movement(self.grid, bishop_positions[2], bishop_positions[3], threat[0], threat[1]))
                    #Queen
                    if len(queens_position) > 0:
                        check.append(not self.pieces.queen_movement(self.grid, color,queens_position[0], queens_position[1], threat[0], threat[1]))
                    #Knight 1
                    if len(knight_positions) > 0:
                        check.append(not self.pieces.knight_movement( knight_positions[0], knight_positions[1], threat[0], threat[1]))
                    #Knight 2
                    if len(knight_positions) > 2:
                        check.append(not self.pieces.knight_movement( knight_positions[2], knight_positions[3], threat[0], threat[1]))
                    #pawn
                    for j in range(0,len(pawn_positions)-1, 2):
                        check.append(not self.pieces.black_pawn_movement(self.grid,pawn_positions[j], pawn_positions[j+1],threat[0], threat[1]))
                    
        else:#white pieces
            #white rooks
            rook_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(0)[1])
            #white bishops
            bishop_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(2)[1])
            #white queen
            queens_position = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(3)[1])
            #white knights
            knight_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(1)[1])
            #white pawns
            pawn_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(5)[1])
            #list of positions
            positions = [rook_positions,bishop_positions,queens_position,knight_positions, pawn_positions]
            
            threats = self.get_threats(color)
            #check for capture first
            #check which piece is checking
            #see if black piece can capture
            for threat in threats:#index 1 is the current position in threat
                for index in range(len(positions)):
                    if len(positions[index]) > 0:
                        check.append(not self.inRange(color, positions[index][0], positions[index][1], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    if len(positions[index]) > 2:
                        check.append(not self.inRange(color, positions[index][2], positions[index][3], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    #for pawns
                    if len(positions[index]) > 4:# 3 pawns
                        check.append(not self.inRange(color, positions[index][4], positions[index][5], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    if len(positions[index]) > 6:# 4 pawns
                        check.append(not self.inRange(color, positions[index][6], positions[index][7], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    if len(positions[index]) > 8:# 5 pawns
                        check.append(not self.inRange(color,positions[index][8], positions[index][9], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    if len(positions[index]) > 10:# 6 pawns
                        check.append(not self.inRange(color,positions[index][10], positions[index][11], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    if len(positions[index]) > 12:# 7 pawns
                        check.append(not self.inRange(color,positions[index][12], positions[index][13], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
                    if len(positions[index]) > 14:# 8 pawns
                        check.append(not self.inRange(color,positions[index][14], positions[index][15], threat[1][0],threat[1][1]))
                        if not check[len(check)-1]:#if its false then it did capture
                            self.pieces.pop_captured_black()
            #blocking
            for x in threats:
                for threat in x[2]:
                    #rook 1
                    if len(rook_positions) > 0:
                        check.append(not self.pieces.rook_movement(self.grid, color,rook_positions[0], rook_positions[1], threat[0], threat[1]))
                    #rook 2
                    if len(rook_positions) > 2:
                        check.append(not self.pieces.rook_movement(self.grid, color,rook_positions[2], rook_positions[3], threat[0], threat[1]))
                    #bishop 1
                    if len(bishop_positions) > 0:
                        check.append(not self.pieces.bishop_movement(self.grid, bishop_positions[0], bishop_positions[1], threat[0], threat[1]))
                    #bishop 2
                    if len(bishop_positions) > 2:
                        check.append(not self.pieces.bishop_movement(self.grid, bishop_positions[2], bishop_positions[3], threat[0], threat[1]))
                    #Queen
                    if len(queens_position) > 0:
                        check.append(not self.pieces.queen_movement(self.grid, color,queens_position[0], queens_position[1], threat[0], threat[1]))
                    #Knight 1
                    if len(knight_positions) > 0:
                        check.append(not self.pieces.knight_movement(knight_positions[0], knight_positions[1], threat[0], threat[1]))
                    #Knight 2
                    if len(knight_positions) > 2:
                        check.append(not self.pieces.knight_movement(knight_positions[2], knight_positions[3], threat[0], threat[1]))
                    #pawn
                    for j in range(0,len(pawn_positions)-1, 2):
                        check.append(not self.pieces.white_pawn_movement(self.grid,pawn_positions[j], pawn_positions[j+1],threat[0], threat[1]))
         
        for c in check:
            if not c:
                #if any is False then not in checkmate
                return False
        # if it makes it this far, everything in check is True
        return True
    #End of Checkmate
    #------------------------------------------------------Threats--------------------------------------------
    def get_threats(self,color):
        #make list for storing which pieces are checking king, and their path
        threatening = []#[Piece,current position,..coordinates]
        if not color:#whites Turn
            #white king
            kings_position = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(4)[1])
            #black rooks
            rook_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(0)[1])
            #black bishops
            bishop_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(2)[1])
            #black queen
            queens_position = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(3)[1])
            #black knights
            knight_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(1)[1])

            #time for the actual work
            #Rook 1 movement
            if len(rook_positions) > 0 and self.pieces.rook_movement(self.grid, color,rook_positions[0], rook_positions[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_piece(0)[1],[rook_positions[0],rook_positions[1]], self.pieces.get_rook_path(self.grid,rook_positions[0],rook_positions[1], kings_position[0],kings_position[1])])
            #Rook 2 movement
            if len(rook_positions) > 2 and self.pieces.rook_movement(self.grid, color,rook_positions[2], rook_positions[3], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_piece(0)[1],[rook_positions[2], rook_positions[3]], self.pieces.get_rook_path(self.grid,rook_positions[2],rook_positions[3], kings_position[0],kings_position[1])])
            #Bishop 1 movement
            if len(bishop_positions) > 0 and self.pieces.bishop_movement(self.grid, bishop_positions[0], bishop_positions[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_piece(2)[1],[ bishop_positions[0], bishop_positions[1]], self.pieces.get_bishop_path(self.grid,bishop_positions[0],bishop_positions[1], kings_position[0],kings_position[1])])
            #Bishop 2 movement
            if len(bishop_positions) > 2 and self.pieces.bishop_movement(self.grid, bishop_positions[2], bishop_positions[3], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_piece(2)[1], [bishop_positions[2], bishop_positions[3]], self.pieces.get_bishop_path(self.grid,bishop_positions[0],bishop_positions[1], kings_position[0],kings_position[1])])
            #Knight 1 movement
            if len(knight_positions) > 0 and self.pieces.knight_movement(knight_positions[0], knight_positions[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_pieces(1)[1], [knight_positions[0],knight_positions[1]]])
            #Knight 2 movement
            if len(knight_positions) > 2 and self.pieces.knight_movement(knight_positions[2], knight_positions[3], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_pieces(1)[1], [knight_positions[2],knight_positions[3]]])
            #Queen Movement
            if len(queens_position) > 0 and self.pieces.queen_movement(self.grid, color,queens_position[0], queens_position[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_black_piece(3)[1], [queens_position[0], queens_position[1]],self.pieces.get_queen_path(self.grid,queens_position[0],queens_position[1], kings_position[0],kings_position[1])])
            #Pawn movement
            #if theres a black pawn at top right or left of king
            if (kings_position[0]+1) <= 7 and (kings_position[1]-1) >= 0 and self.grid[kings_position[0]+1][kings_position[1]-1][1] == self.pieces.get_black_piece(5)[1]:
                threatening.append([self.pieces.get_white_pieces(5)[1],[kings_position[0]+1,kings_position[1]-1]])
            if (kings_position[0]+1) <= 7 and (kings_position[1]+1) <= 7 and self.grid[kings_position[0]+1][kings_position[1]+1][1] == self.pieces.get_black_piece(5)[1]:
                threatening.append([self.pieces.get_white_pieces(5)[1],[kings_position[0]+1,kings_position[1]+1]])
        else:#Blacks Turn
            #black king
            kings_position = self.pieces.get_piece_location(self.grid,self.pieces.get_black_piece(4)[1])
            #white rooks
            rook_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(0)[1])
            #white bishops
            bishop_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(2)[1])
            #white queen
            queens_position = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(3)[1])
            #white knights
            knight_positions = self.pieces.get_piece_location(self.grid,self.pieces.get_white_piece(1)[1])

             #time for the actual work
            #Rook 1 movement
            if len(rook_positions) > 0 and self.pieces.rook_movement(self.grid, color,rook_positions[0], rook_positions[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_piece(0)[1], [rook_positions[0], rook_positions[1]], self.pieces.get_rook_path(self.grid,rook_positions[0],rook_positions[1], kings_position[0],kings_position[1])])               
            #Rook 2 movement
            if len(rook_positions) > 2 and self.pieces.rook_movement(self.grid, color,rook_positions[2], rook_positions[3], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_piece(0)[1],[rook_positions[2], rook_positions[3]], self.pieces.get_rook_path(self.grid,rook_positions[0],rook_positions[1], kings_position[0],kings_position[1])])                 
            #Bishop 1 movement
            if len(bishop_positions) > 0 and self.pieces.bishop_movement(self.grid, bishop_positions[0], bishop_positions[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_piece(2)[1], [bishop_positions[0], bishop_positions[1]], self.pieces.get_bishop_path(self.grid,bishop_positions[0],bishop_positions[1], kings_position[0],kings_position[1])])
            #Bishop 2 movement
            if len(bishop_positions) > 2 and self.pieces.bishop_movement(self.grid, bishop_positions[2], bishop_positions[3], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_piece(2)[1],[ bishop_positions[2], bishop_positions[3]],self.pieces.get_bishop_path(self.grid,bishop_positions[0],bishop_positions[1], kings_position[0],kings_position[1])])
            #Knight 1 movement
            if len(knight_positions) > 0 and self.pieces.knight_movement(knight_positions[0], knight_positions[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_pieces(1)[1],[ knight_positions[0],knight_positions[1]]])
            #Knight 2 movement
            if len(knight_positions) > 2 and self.pieces.knight_movement(knight_positions[2], knight_positions[3], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_pieces(1)[1], [knight_positions[2],knight_positions[3]]])
            #Queen Movement
            if len(queens_position) > 0 and self.pieces.queen_movement(self.grid, color,queens_position[0], queens_position[1], kings_position[0], kings_position[1]):
                threatening.append([self.pieces.get_white_piece(3)[1], [queens_position[0], queens_position[1]],self.pieces.get_queen_path(self.grid,queens_position[0],queens_position[1], kings_position[0],kings_position[1])])
            #Pawn Movement
            if (kings_position[0]-1) >= 0 and (kings_position[1]-1) >= 0 and self.grid[kings_position[0]-1][kings_position[1]-1][1] == self.pieces.get_white_piece(5)[1]:
                threatening.append([self.pieces.get_white_pieces(5)[1],[kings_position[0]-1,kings_position[1]-1]])
            if (kings_position[0]-1) >= 0 and (kings_position[1]+1) <= 7 and self.grid[kings_position[0]-1][kings_position[1]+1][1] == self.pieces.get_white_piece(5)[1]:
                threatening.append([self.pieces.get_white_pieces(5)[1],[kings_position[0]-1,kings_position[1]+1]])
        return threatening
    #End of Get threats
    #Set up Board display
    def print_board(self):
        num = 8
        for i in self.grid:
            print(str(num) + '| ', end='')
            for j in i:
                print(j[1] + " ", end='')
            print()
            num -=1
        print('   ', end='')
        letters = ['A','B','C','D','E','F','G','H']
        for l in letters:
            print(l +'  ', end='')      
    #Move Pieces
    def move_piece(self,isBlack, c_x, c_y, x, y):
        #save moving piece
        piece_to_move = self.grid[c_y][c_x]
        #check move
        if self.checkMove(isBlack,c_y, c_x, y, x):
            #replace with empty space
            self.grid[c_y][c_x] = self.pieces.getEmpty()
            #move piece
            self.grid[y][x] = piece_to_move
            return True
        else:
            return False
    #Update
    def updateBoard(self,isBlack,ctemp_x,ctemp_y, temp_x, temp_y):
        #convert values
        try:
            current_x = self.convert_letter(ctemp_x)
            x = self.convert_letter(temp_x)
            current_y = self.convertY(ctemp_y)
            y = self.convertY(temp_y)
            if self.move_piece(isBlack,current_x,current_y, x, y):
                return True
            else:
                print("Invalid Move. Try again.")
        except:
            print('Invalid Input. Try again.')
        return False
    #Check for invalid moves
    def checkMove(self, isBlack,current_y, current_x, y, x):
        #piece must be there
        #must be their piece
        #must be within that pieces range of movement
        if self.grid[current_y][current_x][1] != self.pieces.getEmpty() and isBlack == self.grid[current_y][current_x][0] and self.inRange(isBlack,current_y, current_x, y, x):
            return True
        else:
            return False
    def blackRanges(self,piece,color, current_y, current_x, y, x):
        valid = True
        #Knight Movement
        if piece == self.pieces.get_black_piece(1)[1]:
            valid = self.pieces.knight_movement(current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Bishop Movement
        elif piece == self.pieces.get_black_piece(2)[1]:
            valid = self.pieces.bishop_movement(self.grid,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Rook Movement
        elif piece == self.pieces.get_black_piece(0)[1]:
             valid = self.pieces.rook_movement(self.grid,color,current_y, current_x, y, x)
             if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Queen Movement
        elif piece == self.pieces.get_black_piece(3)[1]:
            valid = self.pieces.queen_movement(self.grid,color,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Pawn Movement
        elif piece == self.pieces.get_black_piece(5)[1]:
            valid = self.pieces.black_pawn_movement(self.grid,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #King Movement
        elif piece == self.pieces.get_black_piece(4)[1]:
            valid = self.pieces.king_movement(self,color,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        else:
            valid = False
        #End of Movement
        return valid
    def whiteRanges(self,piece, color,current_y, current_x, y, x):
        valid = True
        #Knight Movement
        if piece == self.pieces.get_white_piece(1)[1]:
            valid = self.pieces.knight_movement(current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Bishop Movement
        elif piece == self.pieces.get_white_piece(2)[1]:
            valid = self.pieces.bishop_movement(self.grid,current_y, current_x, y, x)
        #Rook Movement
        elif piece == self.pieces.get_white_piece(0)[1]:
            valid = self.pieces.rook_movement(self.grid,color,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Queen Movement
        elif piece == self.pieces.get_white_piece(3)[1]:
            valid = self.pieces.queen_movement(self.grid,color,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #Pawn Movement
        elif piece == self.pieces.get_white_piece(5)[1]:
            valid = self.pieces.white_pawn_movement(self.grid,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        #King Movement
        elif piece == self.pieces.get_white_piece(4)[1]:
            valid = self.pieces.king_movement(self,color,current_y, current_x, y, x)
            if valid and self.grid[y][x] != self.pieces.getEmpty():
                valid = self.pieces.capture(self.grid,current_y, current_x, y, x)
        else:
            valid = False
        return valid
            
    def inRange(self,isBlack, current_y, current_x, y, x):
        #Get which Piece they are moving using current
        #Then evualte if it can move like that
        piece = self.grid[current_y][current_x][1]
        #check for piece color
        if(isBlack):
            return self.blackRanges(piece,isBlack,current_y, current_x, y, x)
        else:
            return self.whiteRanges(piece,isBlack,current_y, current_x, y, x)
        
    def print_captured(self):
        if len(self.pieces.captured_white) > 0: 
            print("\nCaptured White: " + str(self.pieces.captured_white))
        if  len(self.pieces.captured_black) > 0:
            print("Captured Black: " + str(self.pieces.captured_black))
