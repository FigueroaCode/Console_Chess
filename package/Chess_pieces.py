class Chess_pieces:
    black_pieces = [[True, 'Br'],[True, 'Bk'],
                    [True, 'Bb'],[True, 'BQ'],
                    [True, 'BK'],[True, 'B1']]
    white_pieces = [[False, 'Wr'],[False, 'Wk'],
                    [False, 'Wb'],[False, 'WQ'],
                    [False, 'WK'],[False, 'W1']]
    empty = ['--','--']
    captured_white = []
    captured_black = []
    black_has_moved = {"BK":False,"Br":False,"Br":False}#left rook, right rook
    white_has_moved = {"WK":False,"Wr":False,"Wr":False}
    #get piece
    def get_black_piece(self, index):
        return self.black_pieces[index]
    def get_white_piece(self, index):
        return self.white_pieces[index]
    def getEmpty(self):
        return self.empty
    def get_color(self, grid, current_y, current_x):
        return grid[current_y][current_x][0] # True is Black, False is White
    def capture(self,grid,current_y, current_x, y, x):
        #return false if piece is the same color
        #if different colors capture
        #work on storing captured pieces later
        current_color = self.get_color(grid,current_y, current_x)
        going_color = self.get_color(grid,y, x)
        if current_color == going_color:
            print('Can not capture your own pieces.')
            return False
        else:
            #store captured piece into a list
            captured = grid[y][x]
            if going_color:
                #Captured Piece is Black
                self.captured_black.append(captured)
            else:
                self.captured_white.append(captured)
            return True
    #remove last item from capture list
    def pop_captured_black(self):
        self.captured_black.pop()
    def pop_captured_white(self):
        self.captured_white.pop()
    def get_piece_location(self,grid,piece):
        index = []
        for i in range(8):
            for j in range(8):
                if grid[i][j][1] == piece:
                    index.append(i)
                    index.append(j)
        return index
#piece movement
    def knight_movement(self,current_y, current_x, y, x):
        valid = True
        #Knight Movement
        diff_y = abs(current_y - y)
        diff_x = abs(current_x - x)
        if diff_y == 2:
            if diff_x == 1:
                valid = True
            else:
                valid = False
        elif diff_x == 2:
            if diff_y == 1:
                valid = True
            else:
                valid = False
        else:
            valid = False
        
        return valid
        #end of Knight Movement

    def bishop_movement(self,grid,current_y, current_x, y, x):
        valid = True
        #Bishop Movement
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if diff_x == diff_y:
            valid = True
            #check for pieces in the way
            if current_x > x:
                if current_y < y:
                    #current is above going
                    #new position is before current
                    j = 1
                    for i in range(x+1,current_x):
                        if grid[y-j][i] == self.getEmpty():
                            valid = True
                        else:
                            valid = False
                            break
                        j += 1
                elif current_y > y:
                    #below going
                    j = 0
                    for i in range(x,current_x):
                        if grid[y+j][i] == self.getEmpty():
                            valid = True
                        else:
                            valid = False
                            break
                        j += 1
                else:
                    valid = False
            elif current_x < x:
                #new position is after current
                if current_y < y:
                    #current is above going
                    #new position is before current
                    j = 1
                    for i in range(current_x+1, x):
                        if grid[current_y+j][i] == self.getEmpty():
                            valid = True
                        else:
                            valid = False
                            break
                        j += 1
                elif current_y > y:
                    #below going
                    j = 1
                    for i in range(current_x+1, x):
                        if grid[current_y-j][i] == self.getEmpty():
                            valid = True
                        else:
                            valid = False
                            break
                        j += 1
                else:
                    valid = False
        else:
            #its in the same spot, invalid move
            valid = False
        return valid
    #end of Bishop Movement

    #Rook Movement
    def rook_movement(self,grid,color,current_y, current_x, y, x):
        valid = True
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if diff_y == 0:
            #check for pieces horizontally
            if current_x > x:
                for i in range(x+1, current_x):
                    if grid[y][i] == self.getEmpty():
                        valid = True
                    else:
                        valid = False
                        break
            elif current_x < x:
                for i in range(current_x+1, x):
                    if grid[y][i] == self.getEmpty():
                        valid = True
                    else:
                        valid = False
                        break
        elif diff_x == 0:
            #check for pieces vertically
            if current_y > y:
                for i in range(y, current_y):
                    if grid[i][x] == self.getEmpty():
                        valid = True
                    else:
                        valid = False
                        break
            elif current_y < y:
                #moving down
                for i in range(current_y+1, y):
                    if grid[i][x] == self.getEmpty():
                        valid = True
                    else:
                        valid = False
                        break
        else:
            valid = False
        if valid:
            if color:
                self.black_has_moved[self.get_black_piece(0)[1]] = True
            else:
                self.white_has_moved[self.get_white_piece(0)[1]] = True
        return valid
    #end of Rook movement

    #Queens Movement
    def queen_movement(self,grid,color,current_y, current_x, y, x):
        valid = True
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if diff_x == 0 or diff_y == 0:
            #rook movements
            valid =self.rook_movement(grid,color,current_y, current_x, y, x)
        elif diff_x == diff_y:
            #bishop movements
            valid = self.bishop_movement(grid,current_y, current_x, y, x)
        else:
            valid = False
        return valid
    #End of Queen movement

    #Pawn Movement
    def white_pawn_movement(self,grid,current_y, current_x, y, x):
        #Do pass by capture check later
        valid = True
        diff_x = abs(current_x - x)
        diff_y = current_y - y
        if current_y == 6:
            #its on starting row, so it can move two spaces
            #if its positive then it is moving up
            if diff_y > 0 and diff_y < 3:
                #Valid range, check for pieces in the way
                for i in range(y,current_y):
                    if grid[i][x] == self.getEmpty():
                        valid = True
                    else:
                        valid = False
                        break
            else:
                valid = False
            if diff_x == 1 and diff_y == 1:
                #check for capture
                if grid[y][x] == self.getEmpty():
                    valid = False
                else:
                    valid = True
            elif diff_x != 0:
                valid = False
        #Normal Movement
        elif diff_y == 1:
            #check for pieces in the way
            if grid[y][x] == self.getEmpty():
                valid = True
            else:
                valid = False
                    
            if diff_x == 1:
                #check for capture
                if grid[y][x] == self.getEmpty():
                    valid = False
                else:
                    valid = True
            elif diff_x != 0:
                valid = False
        else:
            valid = False
        #outer
        return valid
    def black_pawn_movement(self,grid,current_y, current_x, y, x):
        valid = True
        diff_x = abs(current_x - x)
        diff_y = y - current_y
        if current_y == 1:
            #its on starting row, so it can move two spaces
            #if its positive then it is moving down
            if diff_y > 0 and diff_y < 3:
                #Valid range, check for pieces in the way
                for i in range(current_y+1, y+1):
                    if grid[i][x] == self.getEmpty():
                        valid = True
                    else:
                        valid = False
                        break
            else:
                valid = False
            if diff_x == 1 and diff_y == 1:
                #check for capture
                if grid[y][x] == self.getEmpty():
                    valid = False
                else:
                    valid = True
            elif diff_x != 0:
                valid = False
        #Normal Movement
        elif diff_y == 1:
            #check for pieces in the way
            if grid[y][x] == self.getEmpty():
                valid = True
            else:
                valid = False
    
            if diff_x == 1:
                #check for capture
                if grid[y][x] == self.getEmpty():
                    valid = False
                else:
                    valid = True
            elif diff_x != 0:
                valid = False
        else:
            valid = False
        #outer
        return valid
    #King Movement
    def king_movement(self,board,color,current_y, current_x, y, x):
        valid = True
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if diff_x < 2 and diff_y < 2:
            #Valid, can only move 1 space in any direction
            valid = True
            if color:
                self.black_has_moved[self.get_black_piece(4)[1]] = True
            else:
                self.white_has_moved[self.get_white_piece(4)[1]] = True
        #check for castling
        elif diff_y == 0 and diff_x == 2:
            if color:#black
                if not (self.black_has_moved.get(0)) and not (self.black_has_moved.get(1)) and not (self.black_has_moved.get(2)):#no piece has moved                   
                    #cant be in check, piece cant be there, enemy piece cant be threatening path
                    if board.in_check(color):
                        valid = False
                    else:
                        #checking for threat
                        board.save_board()
                        temp_x = current_x - x
                        if temp_x < 0:
                            if board.grid[current_y][current_x+1] == self.getEmpty() and board.grid[y][x] == self.getEmpty():#make sure theres no piece where the king is moving to
                                valid = True
                            else:
                                valid = False
                        else:
                            if board.grid[current_y][current_x-1] == self.getEmpty() and board.grid[y][x] == self.getEmpty():#make sure theres no piece where the king is moving to
                                valid = True
                            else:
                                valid = False
                        if valid:
                            #move king to check if it would be in check there
                            board.grid[y][x] = board.grid[current_y][current_x]
                            board.grid[current_y][current_x] = self.getEmpty()
                            valid = not board.in_check(color)
                        board.revert_board()
                        #now move rook
                        if valid:
                            temp_x = current_x - x #if negative then moved to the right
                            #so move rook to kings left, otherwise to the kings right
                            if temp_x < 0:
                                temp = board.grid[0][7]
                                board.grid[0][5] = temp
                                board.grid[0][7] = self.getEmpty()
                            else:
                                board.grid[0][3] = board.grid[0][0]
                                board.grid[0][0] = self.getEmpty()
                else:
                    #one of pieces moved
                    valid = False
            else:
                #white
                if not (self.white_has_moved.get(0)) and not (self.white_has_moved.get(1)) and not (self.white_has_moved.get(2)):
                    if board.in_check(color):
                        valid = False
                    else:
                        board.save_board()
                        temp_x = current_x - x
                        if temp_x < 0:
                            if board.grid[current_y][current_x+1] == self.getEmpty() and board.grid[y][x] == self.getEmpty():#make sure theres no piece where the king is moving to
                                valid = True
                            else:
                                valid = False
                        else:
                            if board.grid[current_y][current_x-1] == self.getEmpty() and board.grid[y][x] == self.getEmpty():#make sure theres no piece where the king is moving to
                                valid = True
                            else:
                                valid = False
                        if valid:
                            #move king to check if it would be in check there
                            board.grid[y][x] = board.grid[current_y][current_x]
                            board.grid[current_y][current_x] = self.getEmpty()
                            valid = not board.in_check(color)
                        board.revert_board()
                        if valid:
                            #if negative then moved to the right
                            #so move rook to kings left, otherwise to the kings right
                            if temp_x < 0:
                                temp = board.grid[7][7]
                                board.grid[7][5] = temp
                                board.grid[7][7] = self.getEmpty()
                            else:
                                board.grid[7][3] = board.grid[7][0]
                                board.grid[7][0] = self.getEmpty()
                else:
                    valid = False
        else:
            #invalid
            valid = False
            
        return valid
########################### Get Paths #############################
    #rook path
    def get_rook_path(self,grid,current_y, current_x, y, x):
        path = []
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if diff_y == 0:
            #check for pieces horizontally
            if current_x > x:
                for i in range(x+1, current_x):
                    if grid[y][i] == self.getEmpty():
                        path.append([y,i])
                    else:
                        break
            elif current_x < x:
                for i in range(current_x+1, x):
                    if grid[y][i] == self.getEmpty():
                        path.append([y,i])
                    else:
                        break
        elif diff_x == 0:
            #check for pieces vertically
            if current_y > y:
                for i in range(y, current_y):
                    if grid[i][x] == self.getEmpty():
                        path.append([i,x])
                    else:
                        break
            elif current_y < y:
                #moving down
                for i in range(current_y+1, y):
                    if grid[i][x] == self.getEmpty():
                        path.append([i,x])
                    else:
                        break
        return path
    #end of Rook movement
    #bishop path
    def get_bishop_path(self,grid,current_y, current_x, y, x):
        path = []
        #Bishop Movement
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if current_x > x:
            if current_y < y:
                #current is above going
                #new position is before current
                j = 1
                for i in range(x+1,current_x):
                    if grid[y-j][i] == self.getEmpty():
                        path.append([y-j,i])
                    else:
                        break
                    j += 1
            elif current_y > y:
                #below going
                j = 0
                for i in range(x,current_x):
                    if grid[y+j][i] == self.getEmpty():
                        path.append([y+j,i])
                    else:
                        break
                    j += 1
        elif current_x < x:
            #new position is after current
            if current_y < y:
                #current is above going
                #new position is before current
                j = 1
                for i in range(current_x+1, x):
                    if grid[current_y+j][i] == self.getEmpty():
                        vpath.append([current_y+j,i])
                    else:
                        break
                    j += 1
            elif current_y > y:
                #below going
                j = 1
                for i in range(current_x+1, x):
                    if grid[current_y-j][i] == self.getEmpty():
                        path.append([current_y-j,i])
                    else:
                        break
                    j += 1

        return path
    #end of Bishop Movement
    #Queen path
    def get_queen_path(self,grid,current_y, current_x, y, x):
        path = []
        diff_x = abs(current_x - x)
        diff_y = abs(current_y - y)
        if diff_x == 0 or diff_y == 0:
            #rook movements
            path =self.get_rook_path(grid,current_y, current_x, y, x)
        elif diff_x == diff_y:
            #bishop movements
            path = self.get_bishop_path(grid,current_y, current_x, y, x)
        return path
    #End of Queen movement
