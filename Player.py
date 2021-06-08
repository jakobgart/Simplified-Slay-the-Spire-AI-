
import itertools
import sys
sys.path.append(".")


    # Action list holds actions
    # Flat action list holds tuples of (attack, defense)
class Player:
    actionList = list()
    macroActionList = list()
    actions = 0
    maxhp = 0
    hp = 0
    attackBuff = 0
    blockBuff = 0

    # Initialization
    def __init__(self):
        self.actionList = list()
        self.macroActionList = list()
        self.actions = 0
        self.maxhp = 0
        self.hp = 0
        self.upgrade1 = -1
        self.upgrade2 = -1
        self.attackBuff = 0
        self.blockBuff = 0

    # ----------------------------------------
    # Initi: initialization functions
    def setActionList(self, n):
        self.actionList=n
    
    def setMaxhp(self, n):
        self.maxhp=n
    
    def setHp(self, n):
        self.hp=n

    def setActions(self, n):
        self.actions=n

    def resetUpgrade(self):
        self.upgrade1 = -1
        self.upgrade2 = -2
        
    # ----------------------------------------
    # Combat: getting functions
    def getMacroAttack(self, n):
        return self.macroActionList[n]["Attack"]
    
    def getMacroBlock(self, n):
        return self.macroActionList[n]["Block"]

    # Get the macro action list
    def getMacroAction(self):
        return self.macroActionList

    def getMacroActionSize(self):
        return len(self.macroActionList)
    
    def getHp(self):
        return self.hp
    
    def getMaxHp(self):
        return self.maxhp

    def getUpgrade1(self):
        return self.upgrade1

    def getUpgrade2(self):
        return self.upgrade2

    # ----------------------------------------
    # Combat: update health
    def lowerHealth(self, n):
        self.hp = self.hp - n

    def fullHeal(self):
        self.hp = self.maxhp
    
    def heal(self, n):
        if self.hp + n >= self.maxhp:
            self.hp = self.maxhp
        else:
            self.hp = self.hp + n
    
    # ----------------------------------------
    # Upgrades: Apply upgrades functions
    # Increase attack upgrade
    def increaseAttack(self, n):
        self.attackBuff = self.attackBuff + n
        self.updateMacroActionList()
        self.addUpgrade(0)

    # Increase block upgrade
    def increaseBlock(self, n):
        self.blockBuff = self.blockBuff + n
        self.updateMacroActionList()
        self.addUpgrade(1)
    
    # Increase attack upgrade
    def increaseActions(self, n):
        self.actions = self.actions + n
        self.updateMacroActionList()
        self.addUpgrade(2)

    def addUpgrade(self, n):
        if self.upgrade1==-1:
            self.upgrade1=n
        else:
            self.upgrade2=n
    # ----------------------------------------
    # Update macro list
    # Updates the current list of attacks (at the start and with upgrades)
    def updateMacroActionList(self):
        # Reset
        self.macroActionList = list()
        tmp = list(itertools.combinations_with_replacement(self.actionList, self.actions))
        for i in tmp:
            cAtt = 0
            cBl = 0
            for j in i:
                if "Attack" in j:
                    cAtt = cAtt + j["Attack"] + self.attackBuff
                if "Block" in j:
                    cBl = cBl + j["Block"] + self.blockBuff
            # Add current action to list
            self.macroActionList.append({"Attack": cAtt, "Block": cBl})
        

    # ----------------------------------------
    # Check if player dead
    def isDead(self):
        return self.hp <= 0

                
