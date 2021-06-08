import random
import sys
import time
sys.path.append(".")

# Local imports
from Player import Player
from Monster import Monster

bestM = [0]*12
"""
Start:
    - Init player
How to know next states:
Will need an extra function
    - Get monster attack, defense and buff
    - Get all possible actions for player
    - Evaluate them.
    - Return evaluation

Combat system:
    Player does actions first, then monster.
    If monster dies it has no actions.
    Monster block goes into next round

"""
class State:
    stringOfMoves = ""


    def __init__(self, k):
        self.stringOfMoves = "" # how we learn, we need this
        self.player = Player() # info about player
        self.monster = Monster() # info about monster
        self.monsterID = 1 # which monster
        self.learn = dict() # learning from LRTA
        self.k=k # for the heuristic
        self.run=False # whenever the run is currently happening
        self.visitedStates = list() # list of visited states
        self.playerHpMonsterStart = 0 # with how much hp does the battle start with
        self.resets = 0 # How many resets happened
        self.maxResets = 0 # What is the max amount of attempts
        self.u1 = -1 # Upgrade 1
        self.u2 = -1 # Upgrade 2
        self.killedByMonster = dict() # Where was the player killed
        self.successfullRuns = dict() # Hold info for successful runs
        self.bestM = dict() # Holds info for how much hp it had for a given monster at best

    # ----------------------------------------
    # Get monster function
    def getMonster(self, n):
        monster = Monster()
        # Monster 1.1
        if n==1:            
            actions=[
                {"Attack": 9}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(40)
            monster.setHp(40)
            monster.setActionID(0)
        # Monster 1.2
        elif n==2:
            actions=[
                {"Attack": 6,
                "Block": 6},
                {"Attack": 17},
                {"Block": 14}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(50)
            monster.setHp(50)
            monster.setActionID(0)
        # Monster 1.3
        elif n==3:
            actions=[
                {"Attack": 5,
                "Block": 6},
                {"Buff": 4,
                "Block": 8},
            ]
            monster.setActionList(actions)
            monster.setMaxhp(70)
            monster.setHp(70)
            monster.setActionID(0)
        # Monster 1.B
        elif n==4:
            actions=[
                {"Block": 13},
                {},
                {"Attack": 21},
                {}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(150)
            monster.setHp(150)
            monster.setActionID(0)
        # Monster 2.1
        elif n==5:
            actions=[                
                {"Attack": 17,
                "Block": 4}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(40)
            monster.setHp(40)
            monster.setActionID(0)
        # Monster 2.2
        elif n==6:
            actions=[
                {"Block": 20},
                {"Buff": 3},
                {"Block": 23},
                {"Attack": 10}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(120)
            monster.setHp(120)
            monster.setActionID(0)
        # Monster 2.3
        elif n==7:
            actions=[
                {"Attack": 6,
                "Buff": 2}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(70)
            monster.setHp(70)
            monster.setActionID(0)
        # Monster 2.B
        elif n==8:
            actions=[
                {"Attack": 5,
                "Block": 2},
                {"Buff": 2}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(200)
            monster.setHp(200)
            monster.setActionID(0)
        # Monster 3.1
        elif n==9:
            actions=[
                {"Attack": 13,
                "Block": 7}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(90)
            monster.setHp(90)
            monster.setActionID(0)
        # Monster 3.2
        elif n==10:
            actions=[
                {"Attack": 8},
                {"Buff": 4,
                "Block": 3},
                {"Block": 11}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(110)
            monster.setHp(110)
            monster.setActionID(0)
        # Monster 3.3
        elif n==11:
            actions=[
                {"Attack": 29,
                "Buff": -3}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(45)
            monster.setHp(45)
            monster.setActionID(0)
        # Monster 3.B
        elif n==12:
            actions=[
                {"Attack": 24,
                "Block": 3},
                {"Attack": 15,
                "Block": 7},
                {"Attack": 11,
                "Block": 12},
                {"Attack": 8,
                "Block": 15},
                {"Attack": 4,
                "Block": 19}
            ]
            monster.setActionList(actions)
            monster.setMaxhp(250)
            monster.setHp(250)
            monster.setActionID(0)
            # boss 2 = jumping from min to max
            # boss 3 = dealth after turns
        return monster



    # ----------------------------------------
    # Reset player
    def resetPlayer(self):
        self.player = Player()
        a1 = {"Attack": 5}
        a2 = {"Block": 5}
        # The two basic moves
        self.player.setActionList([a1, a2])
        # Set player basic stats
        self.player.setMaxhp(100)
        self.player.setHp(100)
        self.player.setActions(3)
        self.player.updateMacroActionList()

    # ----------------------------------------
    # Load new monster
    def loadNewMonster(self):
        self.monster = self.getMonster(self.monsterID)
        # If we just beat the 1st or 2nd boss get an upgrade
        if self.monsterID==5:
            self.makeUpgrade1()
            self.player.heal(30)
        if self.monsterID==9:
            self.makeUpgrade2()
            self.player.heal(30)
        self.playerHpMonsterStart = self.player.getHp()

    # ----------------------------------------
    # Make upgrade 1
    def makeUpgrade1(self):
        if self.u1==0:
            self.player.increaseAttack(3)
        elif self.u1==1:
            self.player.increaseBlock(3)
        else:
            self.player.increaseActions(1)
    
    # Make upgrade 2
    def makeUpgrade2(self):
        if self.u2==0:
            if self.u1==0:
                self.player.increaseAttack(5)
            else:
                self.player.increaseAttack(3)
        elif self.u2==1:
            if self.u1==1:
                self.player.increaseBlock(5)
            else:
                self.player.increaseBlock(3)
        else:
            self.player.increaseActions(1)
    

    def chooseUpgrade(self):
        up=random.choice(range(3))
        #if self.player.getUpgrade1() == -1:
        #    up=0
        #else:
        #    up=0
        if up==0:
            if self.player.getUpgrade1()==0:
                self.player.increaseAttack(5)
            else:
                self.player.increaseAttack(3)
        elif up==1:
            if self.player.getUpgrade1()==1:
                self.player.increaseBlock(5)
            else:
                self.player.increaseBlock(3)
        else:
            self.player.increaseActions(1)
    
    # ----------------------------------------
    # Reset run
    def resetRun(self):
        self.stringOfMoves = ""
        # Reset player 
        self.resetPlayer()
        # Reset monsterID
        self.monsterID = 1 # which monster
        # Load first monster
        self.loadNewMonster()
        # Reset run currently happening
        self.run = True
        # Reset visited states
        self.visitedStates = list()
        # Reset playing hp when starting a monster battle
        self.playerHpMonsterStart = self.player.getMaxHp()
        # Choose the two upgrades
        self.u1 = random.choice(range(3))
        self.u2 = random.choice(range(3))
        
    # ----------------------------------------
    # Combat related functions
    
    # Get the heuristic if player did <whichAttack> action
    def getHeuristicEval(self, whichAttack):
        # Get player info 
        Pattack = self.player.getMacroAttack(whichAttack)
        Pblock = self.player.getMacroBlock(whichAttack)
        Php = self.player.getHp()

        # Get monster info 
        Mattack = self.monster.getAttack()
        Mblock = self.monster.getCurrentBlock()
        Mbuff = self.monster.getBuff()
        Mhp = self.monster.getHp()

        # Calculate damage
        # To monster
        dmgToM = Pattack - Mblock
        if dmgToM < 0: dmgToM = 0 # (in case we dont go through block)
        if Mhp - dmgToM < 0: dmgToM = Mhp # (in case we kill our heuristic will not conut overkill)

        # To player
        dmgToP = Mattack - Pblock
        if dmgToP < 0 : dmgToP = 0 
        if Php - dmgToP < 0 : dmgToP = Php

        # Check if monster dies
        if Mhp - dmgToM <= 0:
           
            monster = self.getMonster(self.monsterID+1)
            # Check if we already been in this state (we are looping)
            if (Php, self.u1, self.u2, monster.getHp(), self.monsterID+1, 0, monster.getActionID()) in self.visitedStates:
                return -99999

             # Check if we already fought next monster with given HP on a previous run
            if (Php, self.u1, self.u2, monster.getHp(), self.monsterID+1, 0, monster.getActionID()) in self.learn:
                # Only return answer if we died attempting it with given hp
                if self.learn[(Php, self.u1, self.u2, monster.getHp(), self.monsterID+1, 0, monster.getActionID())] == -99999:
                    return -99999
                #return self.learn[(Php, self.player.getUpgrade1(), self.player.getUpgrade2(), monster.getHp(), self.monsterID+1, 0, monster.getActionID())]
            
            #if (Php, self.player.getUpgrade2(), self.player.getUpgrade1(), monster.getHp(), self.monsterID+1, 0, monster.getActionID()) in self.learn:
            #    if self.learn[(Php, self.player.getUpgrade2(), self.player.getUpgrade1(), monster.getHp(), self.monsterID+1, 0, monster.getActionID())] == -99999:
            #        return -99999
                #return self.learn[(Php, self.player.getUpgrade2(), self.player.getUpgrade1(), monster.getHp(), self.monsterID+1, 0, monster.getActionID())]
            
            # return the final one
            return ((1-self.k)*(self.monster.getMaxHp()-self.monster.getHp()+dmgToM)) - (self.k*(self.playerHpMonsterStart-self.player.getHp()))
        elif Php - dmgToP <= 0:
            # return big negative number
            return -99999
        else:
            # Check if we have already been in this state (we are looping)
            if (Php - dmgToP, self.u1, self.u2, Mhp - dmgToM, self.monsterID, self.monster.getBuffChange(Mbuff), self.monster.getNextActionID()) in self.visitedStates:
                return -99999


            # Check if learned before
            if (Php - dmgToP, self.u1, self.u2, Mhp - dmgToM, self.monsterID, self.monster.getBuffChange(Mbuff), self.monster.getNextActionID()) in self.learn:
                return self.learn[(Php - dmgToP, self.u1, self.u2, Mhp - dmgToM, self.monsterID, self.monster.getBuffChange(Mbuff), self.monster.getNextActionID())]
            
            # Order of upgrades does not matter therefor we have to checks
            #if (Php - dmgToP, self.player.getUpgrade2(), self.player.getUpgrade1(), Mhp - dmgToM, self.monsterID, self.monster.getBuffChange(Mbuff), self.monster.getNextActionID()) in self.learn:
            #    return self.learn[(Php - dmgToP, self.player.getUpgrade2(), self.player.getUpgrade1(), Mhp - dmgToM, self.monsterID, self.monster.getBuffChange(Mbuff), self.monster.getNextActionID())]
            
            #both player and monster are alive
            return ((1-self.k)*(self.monster.getMaxHp()-self.monster.getHp()+dmgToM)) - (self.k*(self.playerHpMonsterStart-self.player.getHp()+dmgToP))
            

    # Apply the action if player did <whichAttack> action and "learn" for next runs
    def simulateCombat(self, whichAttack, mEval):
        
        # Get player info
        Pattack = self.player.getMacroAttack(whichAttack)
        Pblock = self.player.getMacroBlock(whichAttack)
        Php = self.player.getHp()

        # Get monster info
        Mattack = self.monster.getAttack()
        Mblock = self.monster.getCurrentBlock()
        MBuff = self.monster.getBuff()
        Mhp = self.monster.getHp()
        
        self.stringOfMoves = self.stringOfMoves + str(whichAttack)
        # Learn for next run
        self.learn[(Php, self.u1, self.u2, Mhp, self.monsterID, self.monster.getCurrentBuff(), self.monster.getActionID())] = mEval

        # Add to visited states
        self.visitedStates.append((Php, self.u1, self.u2, Mhp, self.monsterID, self.monster.getCurrentBuff(), self.monster.getActionID()))

        # Calculate damage
        # To monster
        dmgToM = Pattack - Mblock
        if dmgToM < 0: dmgToM = 0 # (in case we dont go through block)
        if Mhp - dmgToM < 0: dmgToM = Mhp # (in case we kill our heuristic will not conut overkill)
        # To player
        dmgToP = Mattack - Pblock
        if dmgToP < 0 : dmgToP = 0 
        if Php - dmgToP < 0 : dmgToP = Php

        # Check if monster dies
        if Mhp - dmgToM <= 0:
            # To not repeat run we will set the learn to bad whenever we've killed the final boss (we overwrite the previous thing)
            if self.monsterID==12:
                self.learn[(Php, self.u1, self.u2, Mhp, self.monsterID, self.monster.getCurrentBuff(), self.monster.getActionID())] = -99999
            # apply it to monster
            self.monster.lowerHealth(dmgToM)
        else:
            # apply it to monster and to player (if player dies he still does the damage, even if it does not matter)
            self.monster.lowerHealth(dmgToM)
            self.player.lowerHealth(dmgToP)
            #Make monster ready for next battle
            self.monster.addBuff(MBuff) # Add buff if the monster buffed with the attack
            self.monster.setCurrentBlock() # Set up current block as the amount it blocks
            self.monster.nextAction() # Set up next action
            

    
    # ----------------------------------------
    # Make action. Includes:
    # One combat round
    # Load new monster (with potentially including picking an update)
    # Reset run
    def makeAction(self):
        # Reset run
        if not self.run:
            #print("Run reset!")
            self.resets=self.resets + 1
            self.resetRun()
            return
        # Load new monster
        if self.monster.isDead():
            if (self.u1, self.u2, self.monsterID) in self.bestM:
                if self.bestM[(self.u1, self.u2, self.monsterID)] < self.player.getHp():
                    self.bestM[(self.u1, self.u2, self.monsterID)] = self.player.getHp()
            else:
                self.bestM[(self.u1, self.u2, self.monsterID)] = self.player.getHp()
            #print("Monster %d killed with %d hp" % (self.monsterID, self.player.getHp()))
            self.monsterID = self.monsterID + 1 # Increase monster ID
            self.loadNewMonster()
            return
        
        # Combat round
        # Get action amount
        act = self.player.getMacroActionSize()

        # List which holds evals
        ev = list()

        # Get all the evaluations
        for i in range(0,act):
            ev.append(self.getHeuristicEval(i))

        # Get the highest eval and its index
        mEval = max(ev)
        mIndex = ev.index(mEval)
        
        # Execute it
        self.simulateCombat(mIndex, mEval)
        
        # Check if player dead, then set to run finished
        if self.player.isDead(): 
            #print("Player died!")
            # Increase the amount of deaths to a certian monster
            if (self.u1, self.u2, self.monsterID) in self.killedByMonster:
                self.killedByMonster[(self.u1, self.u2, self.monsterID)] = self.killedByMonster[(self.u1, self.u2, self.monsterID)] + 1
            else:
                self.killedByMonster[(self.u1, self.u2, self.monsterID)] = 1
            self.run=False
        # Check if final boss beaten, then set run to false
        if self.monster.isDead() and self.monsterID==12:
            #print("Run successful!")
            if (self.u1, self.u2, self.monsterID) in self.bestM:
                if self.bestM[(self.u1, self.u2, self.monsterID)] < self.player.getHp():
                    self.bestM[(self.u1, self.u2, self.monsterID)] = self.player.getHp()
            else:
                self.bestM[(self.u1, self.u2, self.monsterID)] = self.player.getHp()
            if not (self.u1, self.u2, self.stringOfMoves) in self.successfullRuns:
                self.successfullRuns[(self.u1, self.u2, self.stringOfMoves)] = self.resets
            self.run=False

    # ----------------------------------------
    # Macro move. Make actions untill a certian amount of resets happened
    def doRuns(self, howMany):
        self.maxResets = howMany
        while self.resets<=self.maxResets:
            self.makeAction()

    # ----------------------------------------
    # Analyze data
    # Allows us to read bestM in a better way
    def bestMlist(self, u1, u2):
        li = [0]*12
        for i in self.bestM:
            if i[0]==u1 and i[1] == u2:
                li[i[2]-1]=self.bestM[i]
        return li
    
    # Read how many times an upgrade died at a specific mob
    def killList(self, u1, u2):
        li = [0]*12
        for i in self.killedByMonster:
            if i[0]==u1 and i[1] == u2:
                li[i[2]-1]=self.killedByMonster[i]
        return li
    
    # How many sucessful runes an upgrade had
    def succRuns(self, u1, u2):
        howMany = 0
        for i in self.successfullRuns:
            if i[0]==u1 and i[1] == u2:
                howMany = howMany + 1
        return howMany
    
    # First sucessful runs given upgrades
    def firstSucc(self, u1, u2):
        m = self.maxResets+1
        for i in self.successfullRuns:
            if i[0]==u1 and i[1] == u2:
                if self.successfullRuns[i]<m:
                    m=self.successfullRuns[i]
        if m==self.maxResets+1:
            return 0
        return m
        


def printRes(s):
    print("--0 0--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(0,0), s.succRuns(0,0), s.firstSucc(0,0), s.maxResets))
    print("--0 1--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(0,1), s.succRuns(0,1), s.firstSucc(0,1), s.maxResets))
    print("--0 2--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(0,2), s.succRuns(0,2), s.firstSucc(0,2), s.maxResets))

    print("--1 0--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(1,0), s.succRuns(1,0), s.firstSucc(1,0), s.maxResets))
    print("--1 1--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(1,1), s.succRuns(1,1), s.firstSucc(1,1), s.maxResets))
    print("--1 2--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(1,2), s.succRuns(1,2), s.firstSucc(1,2), s.maxResets))

    print("--2 0--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(2,0), s.succRuns(2,0), s.firstSucc(2,0), s.maxResets))
    print("--2 1--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(2,1), s.succRuns(2,1), s.firstSucc(2,1), s.maxResets))
    print("--2 2--\n%s\nFinished runs: %d\nFirst: %d/%d" % (s.bestMlist(2,2), s.succRuns(2,2), s.firstSucc(2,2), s.maxResets))

    print("----Deaths----")

    print("0 0: %s" % s.killList(0,0))
    print("0 1: %s" % s.killList(0,1))
    print("0 2: %s" % s.killList(0,2))

    print("1 0: %s" % s.killList(1,0))
    print("1 1: %s" % s.killList(1,1))
    print("1 2: %s" % s.killList(1,2))

    print("2 0: %s" % s.killList(2,0))
    print("2 1: %s" % s.killList(2,1))
    print("2 2: %s" % s.killList(2,2))

# A run
#s = State(1/2)
#s.doRuns(50000)

