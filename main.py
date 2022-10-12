from random import choice
import time
import pickle
import os
import re

build = str("v.1.4")
header = str("──────────────────────────────────────────────────────────────────────────────<")
short_header = header[:42] + str("<")

sv_folder = str("ctbg_savedata/")
sv_folder_dir = re.sub('/', '', sv_folder)

def start():
    global sv_folder
    global sv_folder_dir
    sv_folder_check_start = time.time()
    if not os.path.exists(sv_folder_dir):
        print(f"sv_folder: {sv_folder_dir} not found, creating...")
        os.makedirs(sv_folder_dir)
    else:
        print(f"sv_folder: {sv_folder_dir} found")
    print("Checking completed   " + str(time.time() - sv_folder_check_start) + "s")
    main.main()

class entity:
    def __init__(self, health, power, balance, level):
        self.health = health
        self.power = power
        self.balance = balance
        self.level = level

player = entity(100, 30, 10, 1)
enemy_easy = entity(100, 10, 20, 1)
enemy_normal = entity(100, 30, 50, 2)
enemy_hard = entity(100, 50, 100, 3)

difficulty_list = ["easy", "normal", "hard"]

class main:

    win = int(1)
    lose = int(1)

    potion_token = int(5)
    defense_token = int(5)
    train_token = int(1)

    potion_healing = int(50)

    potion_token_add = int(2)
    defense_token_add = int(3)
    train_token_add = int(1)

    shop_potion_price = int(50)
    shop_defense_price = int(50)

    t_time = int(1) #Wait time for turn and input respond

    def main():
        print(header)
        print("[A]Battle, [B]Status, [C]Training Area, [D]Save Data, [E]Load Data, [QUIT]Quit")
        loop = True
        while loop == True:
            
            main_input = input("input: ").lower()
            
            if main_input == "a":
                print(difficulty_list)
                difficulty_selection = input("Difficulty: ").lower()
                if difficulty_selection == "easy":
                    main.battle(player, enemy_easy)
                if difficulty_selection == "normal":
                    main.battle(player, enemy_normal)
                if difficulty_selection == "hard":
                    main.battle(player, enemy_hard)
                
            if main_input == "b":
                print("")
                print(short_header)
                print(f"Level: {player.level}")
                print(f"Balance: {player.balance}")
                print(f"Potion of Healing: {main.potion_token}")
                print(f"Defense Shield: {main.defense_token}")
                print(f"Training Token: {main.train_token}")
                print(f"Current Power: {player.power}")
                print("")
                print(f"Win: {main.win}")
                print(f"Lose: {main.lose}")
                print(f"Winrate(%): {main.win / (main.win+main.lose)}%")
                print(short_header)
                print("")

            if main_input == "c":
                print(header)
                print("[A]Train, [B]Buy Healing Potion, [C]Buy Defense Token, [BACK]Back")
                loop = True
                while loop == True:
                    training_input = input("training-input: ").lower()
                    if training_input == "a":
                        main.train(player)
                    if training_input == "b":
                        if player.balance > main.shop_potion_price or player.balance == main.shop_potion_price:
                            player.balance -= main.shop_potion_price
                            main.potion_token += int(1)
                            print("Bought 1 Potion of Healing!")
                        elif player.balance < main.shop_potion_price:
                            print(f"Your Balance must have at least {main.shop_potion_price} to buy!")
                    if training_input == "c":
                        if player.balance > main.shop_defense_price or player.balance == main.shop_defense_price:
                            player.balance -= main.shop_defense_price
                            main.potion_token += int(1)
                            print("Bought 1 Defense Shield")
                        elif player.balance < main.shop_defense_price:
                            print(f"Your Balance must have at least {main.shop_defense_price} to buy!")
                    if training_input == "back":
                        main.main()

            if main_input == "d":
                pickle.dump(player.level, open(sv_folder + "level.dat", "wb"))
                pickle.dump(player.balance, open(sv_folder + "balance.dat", "wb"))
                pickle.dump(player.power, open(sv_folder + "power.dat", "wb"))
                pickle.dump(main.potion_token, open(sv_folder + "potion_token.dat", "wb"))
                pickle.dump(main.defense_token, open(sv_folder + "defense_token.dat", "wb"))
                pickle.dump(main.train_token, open(sv_folder + "train_token.dat", "wb"))
                pickle.dump(main.win, open(sv_folder + "win.dat", "wb"))
                pickle.dump(main.lose, open(sv_folder + "lose.dat", "wb"))
                print("Progress saved")

            if main_input == "e":
                try:
                    player.level = pickle.load(open(sv_folder + "level.dat", "rb"))
                    player.balance = pickle.load(open(sv_folder + "balance.dat", "rb"))
                    player.power = pickle.load(open(sv_folder + "power.dat", "rb"))
                    main.potion_token = pickle.load(open(sv_folder + "potion_token.dat", "rb"))
                    main.defense_token = pickle.load(open(sv_folder + "defense_token.dat", "rb"))
                    main.train_token = pickle.load(open(sv_folder + "train_token.dat", "rb"))
                    main.win = pickle.load(open(sv_folder + "win.dat", "rb"))
                    main.lose = pickle.load(open(sv_folder + "lose.dat", "rb"))
                    print("Progress loaded")
                except FileNotFoundError:
                    print("No savedata detected")

            if main_input == "devmode":
                loop = True
                while loop == True:
                    dev_input = input("dev-input: ").lower()
                    if dev_input == "build":
                        print(f"version: {build}")
                    if dev_input == "back":
                        loop = False
                        main.main()
                    if dev_input == "toggle_t_time":
                        if main.t_time == int(0):
                            main.t_time = int(1)
                        elif main.t_time == int(1):
                            main.t_time = int(0)
                        print(f"t_time: {main.t_time}")
                    if dev_input == "cmdls":
                        print("build, back, toggle_t_time, +level, +balance, +power, +traintoken, +potiontoken, +defensetoken")
                    if dev_input == "+level":
                        player.level += int(1)
                    if dev_input == "+balance":
                        player.balance += int(100)
                    if dev_input == "+power":
                        player.power += int(10)
                    if dev_input == "+traintoken":
                        main.train_token += int(1)
                    if dev_input == "+potiontoken":
                        main.potion_token += int(1)
                    if dev_input == "+defensetoken":
                        main.defense_token += int(1)

            if main_input == "quit":
                quit()

    def train(player):
        opp_1 = [True, True, False]
        opp_2 = [True, False]
        if main.train_token > 0 and player.power < 50:
            success_opp = choice(opp_1)
            main.train_token -= int(1)
            if success_opp == True:
                player.power += int(10)
                print(f"Training Successfull!, Current Power: {player.power}")
            if success_opp == False:
                print(f"Training Failed!, Current Power: {player.power}")
        elif main.train_token > 0 and (player.power > 50 or player.power == 50):
            success_opp = choice(opp_2)
            main.train_token -= int(1)
            if success_opp == True:
                player.power += int(10)
                print(f"Training Successfull!, Current Power: {player.power}")
            if success_opp == False:
                print(f"Training Failed!, Current Power: {player.power}")    
        else:
            print("No Tokens Left")


    def battle(player, enemy):
        
        # ─── CHECK IF THE PLAYER POWER IS BALANCED WITH THE ENEMY HEALTH ─
        if player.power > int(300):
            enemy.health = int(500)
            enemy.level += int(3)
        elif player.power > int(200):
            enemy.health = int(350)
            enemy.level += int(2)
        elif player.power > int(100):
            enemy.health = int(250)
            enemy.level += int(1)
        # ─────────────────────────────────────────────────────────────────

        print(header)
        print("[A]Attack, [B]Defend, [C]Healing Potion")
        loop = True
        while loop == True:
            print("")
            
            if enemy.health < 0 or enemy.health == 0:
                player.health = int(0)
                enemy.health = int(0)
                player.balance += enemy.balance
                player.level += enemy.level
                player.health = int(100)
                enemy.health = int(100)
                main.potion_token += main.potion_token_add
                main.defense_token += main.defense_token_add
                main.train_token += main.train_token_add
                main.win += int(1)
                print("You Win")
                main.main()
                loop = False
            elif player.health < 0 or player.health == 0:
                player.health = int(0)
                enemy.health = int(0)
                player.balance -= (enemy.balance / 2)
                player.level -= enemy.level
                player.health = int(100)
                enemy.health = int(100)
                main.train_token += main.train_token_add
                main.lose += int(1)
                print("You Lose")
                main.main()
                loop = False

            opp = (True, False)
            success_opp = choice(opp)
            random_opp = choice(opp)

            battle_input = input(">Your Turn< : ").lower()
            
            if battle_input == "a" or battle_input == "attack":
                time.sleep(main.t_time)
                if success_opp == True:
                    enemy.health -= player.power
                    print(f"dmg:{player.power}, Attack Landed Successfully!")
                elif success_opp == False:
                    print(f"Failed To Attack!")                
                print(">Enemy Turn<")
                time.sleep(main.t_time)
                if random_opp == True:
                    player.health -= enemy.power
                    print(f"Received Damage from Enemy {enemy.power}")
                elif random_opp == False:
                    print(f"Avoided Enemy Attack")
                print(f"Player HP: {player.health}, Enemy HP: {enemy.health}")

            if battle_input == "b" or battle_input == "defend":
                time.sleep(main.t_time)
                if random_opp == True:
                    if main.defense_token > 0:
                        enemy.health -= (enemy.power/2)
                        main.defense_token -= 1
                        print(f"defense remaining: {main.defense_token}")
                        print(f"50% Damage Returned to Enemy!")
                    else:
                        print("No Tokens Left")
                elif random_opp == False:
                    if main.defense_token > 0:
                        main.defense_token -=1
                        print(f"defense remaining: {main.defense_token}")
                        print(f"Avoided Enemy Attack")
                    else:
                        print("No Tokens Left")
                print(f"Player HP: {player.health}, Enemy HP: {enemy.health}")

            if battle_input == "c" or battle_input == "heal":
                time.sleep(main.t_time)
                if main.potion_token > 0:
                    main.potion_token -= 1
                    player.health += main.potion_healing
                    print(f"Wounds healed {main.potion_healing}HP")
                    print(f"Potion Remaining {main.potion_token}")
                    print(f"Player HP: {player.health}, Enemy HP: {enemy.health}")
                else:
                    print("No Potion Left")



if __name__ == "__main__":
    start()