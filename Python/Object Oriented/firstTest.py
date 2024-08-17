class enemy:
    def __init__(self,name,life):
        self._name = name
        self._life = life
        
    
    def attack(self):
        self._life -= 1
        print(self._name,": ouch!",self._life)
        
enemiesList = []

enemy1 = enemy("bob", 10)
enemy2 = enemy("greg",6)




enemy1.attack()
enemy2.attack()
enemy2.attack()
enemy2.attack()
enemy2.attack()
enemy1.attack()