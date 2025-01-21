import pygame
import socket
import network
import player_assets
from gameWiin import Game

class MultiplayerNetwork :
    def __init__(self):
        # the server will be initialized here
        self.connections = []
        self.connection  = None
    def connectServer(self):
        self.connections = network.start_server_multi()
        if self.connections:  # Ensure connections were successfully established
            print("Network setup complete for server!")
            self.conn1, self.addr1 = self.connections[0]
            self.conn2, self.addr2 = self.connections[1]
            print("Both clients are connected. Starting game...")
        else:
            print("Failed to establish connections with clients.")
            exit(1)
    def connectClient(self):
        server_ip = input("Enter server IP address: ").strip()
        server_port = int(input("Enter server port (default 12345): ") or 12345)
        self.connection = network.start_client(server_ip, server_port)
        # Wait for the start signal from the server before initializing the game window
        #STEP4: Both wait for the start signal
        start_signal = ""
        while start_signal != "START_GAME":
            # If the received message is not START_GAME just print it and wait again.
            start_signal = network.receive_message(self.connection)
            if start_signal != "START_GAME":
                print(f"Received something but still waiting for start signal. Received: {start_signal}")
                
        if start_signal == "START_GAME":
            print("Server Reports: Both clients are connected. Starting the game...")
            #OK Ready to Start: Go go go!
            size = (700, 500)
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("Template")
        # Ensure a connection was established
        if self.connection:
            print("Network setup complete!")
        else:
            print("Failed to establish a network connection.")
            exit(1)

# An error occurred during client operation: 'SpaceShooterMult' object has no attribute 'connection'
class SpaceShooterMult(Game):
    def __init__(self, dim, title, mode):
        super().__init__(dim, title)
        self.BLACK=(0,0,0)
        self.WHITE=(255,255,255)
        self.GREEN=(0,255,0)
        self.RED=(255,0,0)
        self.BLUE=(0,0,255)
        self.main_loop = True #flag to indicate that we are working on main loop
        self.playerA = player_assets.Ball(self.RED, 20, 20 )
        self.playerA.rect.center = (20, 200)
        self.playerB = player_assets.Ball(self.BLUE, 20, 20 )
        self.playerB.rect.center = (670, 200)
        self.all_sprites_list=pygame.sprite.Group()
        self.all_sprites_list.add(self.playerA)
        self.all_sprites_list.add(self.playerB)
        self.clock=pygame.time.Clock()
        self.counter = 1
        self.network = MultiplayerNetwork()
        self.mode = mode
        if mode == 's':
            self.network.connectServer()
        else :
            self.network.connectClient()
    def onControl(self):
        super().onControl()
        if self.mode == 's':
            try:
                
                # Receive data from Client A
                data_from_clientA = network.receive_data(self.network.conn1)
                # Receive data from Client B
                data_from_clientB = network.receive_data(self.network.conn2)
                
                
                if data_from_clientA:
                    if data_from_clientA['action'] != 'no_action':
                        if data_from_clientA['action'] == 'moveUp':
                            self.playerA.moveUp()
                        elif data_from_clientA['action'] == 'moveDown':
                            self.playerA.moveDown()

                
                if data_from_clientB:
                    if data_from_clientB['action'] != 'no_action':
                        if data_from_clientB['action'] == 'moveUp':
                            self.playerB.moveUp()
                        elif data_from_clientB['action'] == 'moveDown':
                            self.playerB.moveDown()

                game_state = {
                    'playerA_y': self.playerA.rect.y,
                    'playerB_y': self.playerB.rect.y,
                }
                network.send_data(self.network.conn1, game_state)
                network.send_data(self.network.conn2, game_state)
                counter=counter+1
            except Exception as e:
                print(f"An error occurred during the game loop: {e}")
                return
        elif self.mode == 'c':
            try:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        main_loop=False
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_x:
                            main_loop=False
                # Capture and send player movement input
                keys = pygame.key.get_pressed()
                action = None
                if keys[pygame.K_w]:
                    action = 'moveUp'
                elif keys[pygame.K_s]:
                    action = 'moveDown'
                    
                # If no action is detected, send a dummy packet
                # *SOS* if we do not send a packet the server will be blocked waiting
                if action:
                    client_data = {'action': action}
                else:
                    client_data = {'action': 'no_action'}  # Dummy packet to indicate no input
                network.send_data(self.network.connection, client_data)

                # Receive and process game state updates
                game_state = network.receive_data(self.network.connection)
                if game_state:
                    if "result" in game_state:
                        print(game_state["result"])
                        main_loop = False  # Exit the loop when the game ends
                    else:
                        # Update local variables or display based on the received game state
                        #STEP3: Update Game State
                        # Update the game display based on received game state
                        self.playerA.rect.y = game_state['playerA_y']
                        self.playerB.rect.y = game_state['playerB_y']
                    
                        # -- Game Logic

                    self.all_sprites_list.update()
                    self.screen.fill(self.BLACK) #background color of screen/ Redraw black
                    #draw the net
                    # pygame.draw.line(screen, WHITE, [349,0],[349,500],5)
                    self.all_sprites_list.draw(self.screen)
                    

                pygame.display.flip() #update the screen            

            except Exception as e:
                print(f"An error occurred during client operation: {e}")



mode = input("Start as server (s) or client (c)? ").strip().lower()
game = SpaceShooterMult( dim = (800,800), title = "Space Shooter", mode=mode)
game.run()