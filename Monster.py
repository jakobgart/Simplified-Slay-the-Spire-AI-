
from Action import Action


class Monster:
    actionList = list()
    actionID = list()
    maxhp = 0
    hp = 0    
    block = 0
    buff = 0
    maxAttack = -1 # This is implemented for negative debuffs

    # Initialisation function
    def __init__(self):
        self.actionList = list()
        self.maxhp = 0
        self.hp = 0
        self.actionID = 0
        self.buff = 0
        self.block = 0
        self.maxAttack = -1

    # ----------------------------------------
    # Setting functions
    def setActionList(self, n):
        self.actionList=n
        # Set the max attack
        for j in n:
            if "Attack" in j:
                if j["Attack"] > self.maxAttack:
                    self.maxAttack = j["Attack"]
    
    def setMaxhp(self, n):
        self.maxhp=n
    
    def setHp(self, n):
        self.hp=n
    
    def setActionID(self, n):
        self.actionID=n

    def setBuff(self, n):
        self.buff=n
    
    
    # ----------------------------------------
    # Combat: get info
    # Get attack of action
    def getAttack(self):
        # Check if we even attack
        if "Attack" in self.actionList[self.actionID]:
            # In case of negative buff we will not be healing the player
            if self.actionList[self.actionID]["Attack"] + self.buff < 0:
                return 0
            else:
                return self.actionList[self.actionID]["Attack"] + self.buff
        return 0

    # Set current block
    def setCurrentBlock(self):
        self.block=self.getBlock()

    # Block of action
    def getBlock(self):
        # Check if we even block
        if "Block" in self.actionList[self.actionID]:
            return self.actionList[self.actionID]["Block"]
        return 0


    # Buff of action
    def getBuff(self):
        if "Buff" in self.actionList[self.actionID]:
            return self.actionList[self.actionID]["Buff"]
        return 0

    # Current block
    def getCurrentBlock(self):
        return self.block

    # Get current hp of monster
    def getHp(self):
        return self.hp
    
    # Get actionID of monster
    def getActionID(self):
        return self.actionID

    # Get max hp of monster
    def getMaxHp(self):
        return self.maxhp

    # Get current buff of monster
    def getCurrentBuff(self):
        return self.buff
    
    # Returns the change that happens if we apply n buff to monster
    def getBuffChange(self, n):
        # If buff is positive then ok
        if n>=0:
            return self.buff + n
        else:
            # Buff is negative. Check if all its attacks are already null due to debuffing
            if self.maxAttack + self.buff <= 0:
                return self.buff
            else: # It is not yet null, so return debuff
                return self.buff + n

    # ----------------------------------------
    # Combat: change info
    # Set actionID to next action
    def nextAction(self):
        self.actionID = (self.actionID + 1) % len(self.actionList)
    
    # Get next actionID (for state space search)
    def getNextActionID(self):
        return (self.actionID + 1) % len(self.actionList)

    # Change stats functions
    def lowerHealth(self, n):
        self.hp = self.hp - n
    
    def addBuff(self, n):
        if self.maxAttack + self.buff > 0:
            self.buff = self.buff + n
    
    # ----------------------------------------
    # Check if dead
    def isDead(self):
        return self.hp <= 0
