import time
import socket
import select
import sys
import string
import indexer
import pickle as pkl
from chat_utils import *
import chat_group as grp
import piece
import referee
import run_xiangqi as rxq
#WABBA LUBBA DUB DUB

class XiangQi:
    """
    This will contain all of the rules from the piece and referee instances
    """
    def __init__(self, Player1, Player2):
        self.game_board, self.dictionary = piece.initialize_game()
        self.players = [Player1, Player2]
        self.player_color = {Player1:'red', Player2:'black'}
        self.turn = 0
#        self.game_board = piece.Board()
        self.color = ''
        self.ID = ''
        self.new_location_to_move = []
#        self.p_move_piece = piece.move_piece(self.color, self.ID, self.new_location_to_move, self.game_board, self.dictionary)
    def next_turn(self):
        self.turn += 1
    
    def func_player_to_move(self):
        if self.turn % 2 != 0:
            self.player_to_move = self.players[0]
        else:
            self.player_to_move = self.players[1]
        
        return self.player_to_move
    def is_victory(self):
        pass
    def is_tie(self):
        pass
            

class Server:
    def __init__(self):
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        # sonnet
        self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        self.sonnet = pkl.load(self.sonnet_f)
        self.sonnet_f.close()
        
    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        #read the msg that should have login code plus username
        msg = myrecv(sock)
        if len(msg) > 0:
            code = msg[0]

            if code == M_LOGIN:
                name = msg[1:]
                if self.group.is_member(name) != True:
                    #move socket from new clients list to logged clients
                    self.new_clients.remove(sock)
                    #add into the name to sock mapping
                    self.logged_name2sock[name] = sock
                    self.logged_sock2name[sock] = name
                    #load chat history of that user
                    if name not in self.indices.keys():
                        try:
                            self.indices[name]=pkl.load(open(name+'.idx','rb'))
                        except IOError: #chat index does not exist, then create one
                            self.indices[name] = indexer.Index(name)
                    print(name + ' logged in')
                    self.group.join(name)
                    mysend(sock, M_LOGIN + 'ok')
                else: #a client under this name has already logged in
                    mysend(sock, M_LOGIN + 'duplicate')
                    print(name + ' duplicate login attempt')

            else:
                print ('wrong code received')
        else: #client died unexpectedly
            self.logout(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code 
        msg = myrecv(from_sock)
        if len(msg) > 0:
            code = msg[:1].strip()           
#==============================================================================
# handle connect request
#==============================================================================
            if code == M_CONNECT:
                to_name = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = M_CONNECT + 'hey you'
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = M_CONNECT + 'ok'
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, M_CONNECT + from_name)
                else:
                    msg = M_CONNECT + 'no_user'
                mysend(from_sock, msg)
            
            
            
            #WABBA LUBBA DUB DUB
            
            if code == M_GAME:
                to_name = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                print( "G|"+to_name+"|"+str(self.group.list_me(to_name)) )
                if to_name == from_name:
                    msg = M_GAME + 'hey you'
                # connect to the peer
                elif self.group.is_member(to_name) and len(self.group.list_me(to_name)) == 1:
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    mysend(to_sock, M_GAME + from_name)
                    msg = M_GAME + 'ok'
                    
                    self.game = XiangQi(from_name,to_name)
#                    mysend(from_sock, M_IN_GAME + self.game.game_board.print_board() )
#                    mysend(to_sock, M_IN_GAME + self.game.game_board.print_board() )
                else:
                    msg = M_GAME + 'no_user'
                mysend(from_sock, msg)
#==============================================================================
# handle message exchange   
#==============================================================================
            elif code == M_EXCHANGE:
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                said = msg[1:]
                said2 = text_proc(said, from_name)
                self.indices[from_name].add_msg_and_index(said2)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    self.indices[g].add_msg_and_index(said2)                
                    mysend(to_sock, msg)
            # Wabba Lubba Dub Dub
            elif code == M_IN_GAME:
                
                from_name = self.logged_sock2name[from_sock]
                print(from_name)
                print(self.game.func_player_to_move())
                to_name = self.group.list_me(from_name)[1]
                to_sock = self.logged_name2sock[to_name]
                letter_to_number_dict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6\
                                      ,'H':7,'I':8}
#                print(from_name)
#                print(to_name)
#                print(to_sock)
#                print(self.game.players)
#                print(self.game.players[0])                
#                print(self.game.player_to_move())
                
                # It's your turn
                if self.game.turn == 0:
                    rules = "In order to move the desired piece, enter the following message: M piece location\n"
                    mysend(to_sock, M_IN_GAME + rules + self.game.game_board.print_board())
                    mysend(from_sock, M_IN_GAME + rules + self.game.game_board.print_reversed_board())
                    self.game.next_turn()

                elif self.game.func_player_to_move() == from_name:
                    print('YAY YOUR TURN')
                    if len(msg.rstrip()) > 1:
                        if msg[1] == 'M' and msg[2:].isalpha() == False:
                            try:
                                move = msg[2:].split()
                                piece_to_move = int(move[0])
    #                            _x_ = int(move[1][0])
                                KEY = move[1][0]
                                _x_ = letter_to_number_dict[KEY]
                                _y_ = int(move[1][1])
                                desired_loc = [_x_,_y_]
#                                print(piece.move_piece(self.game.player_color[from_name], piece_to_move, desired_loc, self.game.game_board, self.game.dictionary))
                                if piece.move_piece(self.game.player_color[from_name], piece_to_move, desired_loc, self.game.game_board, self.game.dictionary) == True:
                                    print(piece.move_piece(self.game.player_color[from_name], piece_to_move, desired_loc, self.game.game_board, self.game.dictionary))
                                    mysend(to_sock, M_IN_GAME \
                                           + 'Turn #{} \n'.format(self.game.turn))
                                    mysend(to_sock, M_IN_GAME + from_name \
                                           + ' moved piece ' + move[0] \
                                           + ' to position ' + move[1] + '\n')
                                    if self.logged_name2sock[from_name] == from_sock:
                                        if self.game.func_player_to_move() == self.game.players[0]:
                                            mysend(to_sock, M_IN_GAME + self.game.game_board.print_board() + '\nYour turn')
                                            mysend(from_sock, M_IN_GAME + self.game.game_board.print_reversed_board())
                                            self.game.next_turn()
    #                                    """
                                        else:
                                            mysend(to_sock, M_IN_GAME + self.game.game_board.print_reversed_board() + '\nYour turn')
                                            mysend(from_sock, M_IN_GAME + self.game.game_board.print_board())
                                            self.game.next_turn()
                                elif piece.move_piece(self.game.player_color[from_name], piece_to_move, desired_loc, self.game.game_board, self.game.dictionary) == "Cannot move opponent's piece!":
                                    mysend(from_sock, M_IN_GAME + 'Cannot move opponent\'s piece!')
                                    
                                elif piece.move_piece(self.game.player_color[from_name] ,piece_to_move, desired_loc, self.game.game_board, self.game.dictionary) == 'END':
                                    pass
                            except IndexError:
                                pass
                                            
#                                    """
#                                else:
#                                    pass
                                

#                                    mysend(from_sock, M_IN_GAME + self.game.game_board.print_board())
#                                self.game.next_turn()

#                            except:
#                                pass
                        else:
                            mysend(to_sock, M_IN_GAME + '[' + from_name + ']' + msg[1:])
                    else:
                        pass
#                    mysend(to_sock, M_IN_GAME + '[' + from_name + ']' + msg[1:])
#                    self.game.next_turn()
                # Not your turn
                elif self.game.func_player_to_move() != from_name:
#                    print('Please wait patiently for your turn')
#                    mysend(to_sock, M_IN_GAME + '[' + from_name + ']' + msg[1:])
#                    mysend(from_sock, M_IN_GAME + 'Please wait patiently for your turn.\n')
                    mysend(to_sock, M_IN_GAME + '[' + from_name + ']' + msg[1:])
                # Simple Chat
                else:
                    print('Chatting chatting')
                    mysend(to_sock, M_IN_GAME + '[' + from_name + ']' + msg[1:])
            
                """
                # If it is the sender's turn
                if  from_name == self.game.player_to_move():
                    print('This would be Player 1\'s turn')
                    print('Assuming this is a valid move, this will end the end the turn')
                    mysend(to_sock, M_IN_GAME + self.game.placeholder() + 'Opponent\'s turn')
                    self.game.next_turn()
                elif from_name != self.game.player_to_move():
                    print('It\'s not your turn to move!!!')
                else:
                    mysend(to_sock, M_IN_GAME + "[" + from_name + "]" + msg[1:])
                    
                    
                    
                """
#                if from_name == self.game.players[ self.game.current_player % 2 ] and msg[1] in ("1","2","3") and msg[2] in ("1","2","3"):
#                    # Legal move
#                    if self.game.update( int(msg[1])-1, int(msg[2])-1 ):
#                        # Not a winning move
#                        if not self.game.check_victory()[0] and not self.game.check_tie():
#                            mysend(from_sock, M_IN_GAME + str(self.game) + "Waiting on opponent...\n")
#                            mysend(to_sock, M_IN_GAME + str(self.game) + "\nYOUR TURN: ")
#                        # Winning move
#                        elif self.game.check_victory()[0]:
#                            mysend(from_sock, M_IN_GAME + str(self.game) + "\nYOU WIN!\n")
#                            mysend(to_sock, M_IN_GAME + str(self.game) + "\nYOUR OPPONENT WON!\n" )
#                        # It's a tie!
#                        elif self.game.check_tie():
#                            mysend(from_sock, M_IN_GAME + str(self.game) + "\nIT'S A TIE!\n")
#                            mysend(to_sock, M_IN_GAME + str(self.game) + "\nIT'S A TIE!\n" )
#                    # Illegal Move
#                    else:
#                        mysend(from_sock, M_IN_GAME + str(self.game) + "THAT SQUARE IS OCCUPIED!\n")
#
#                # If it is not the sender's turn but they tried to play anyway        
#                elif from_name != self.game.players[ self.game.current_player % 2 ] and msg[1] in ("1","2","3") and msg[2] in ("1","2","3"):
#                    mysend(from_sock, M_IN_GAME + str(self.game) + "NOT YOUR TURN!\n")
#
#                # Other types of messages
#                else:
#                    mysend(to_sock, M_IN_GAME + "[" + from_name + "]" + msg[1:])
#==============================================================================
#listing available peers
#==============================================================================
            elif code == M_LIST:
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all()
                mysend(from_sock, msg)
#==============================================================================
#retrieve a sonnet
#==============================================================================
            elif code == M_POEM:
                poem_indx = int(msg[1:])
                from_name = self.logged_sock2name[from_sock]
                print(from_name + ' asks for ', poem_indx)
                poem = self.sonnet.get_sect(poem_indx)
                print('here:\n', poem)
                mysend(from_sock, M_POEM + poem)
#==============================================================================
#time
#==============================================================================
            elif code == M_TIME:
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, ctime)
#==============================================================================
#search
#==============================================================================
            elif code == M_SEARCH:
                term = msg[1:]
                from_name = self.logged_sock2name[from_sock]
                print('search for ' + from_name + ' for ' + term)
                search_rslt = (self.indices[from_name].search(term)).strip()
                print('server side search: ' + search_rslt)
                mysend(from_sock, M_SEARCH + search_rslt)

#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif code == M_DISCONNECT:
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, M_DISCONNECT)
#==============================================================================
#the "from" guy really, really has had enough
#==============================================================================
            elif code == M_LOGOUT:
                self.logout(from_sock)
        else:
            #client died unexpectedly
            self.logout(from_sock)   

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)
           
def main():
    server=Server()
    server.run()

if __name__ == '__main__':
    main()
