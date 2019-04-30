class UnitDecorator:
    def decrease_effects_time(self):
        if isinstance(self.unit, UnitDecorator):
            self.unit = self.unit.decrease_effects_time()
        if self.time == 0:
            return self.unit
        self.time -= 1
        return self
    def __setattr__(self, attr, value):
        if attr == 'unit' or attr == 'time' or attr == 'decrease_effects_time' or attr == 'is_positive':
            self.__dict__[attr] = value
        else:
            setattr(self.__dict__['unit'], attr, value)
        

class StrengthSpell(UnitDecorator):
    is_positive = True
    def __init__(self, unit, time):
        self.unit = unit
        self.time = time
        #self.is_positive = True
    def __getattr__(self, attr):
        res = getattr(self.unit, attr)
        if attr == 'min_damage':
            return getattr(self.unit, 'max_damage')
        if attr == 'attack':
            return res + 1
        return res


class SlowSpell(UnitDecorator):
    is_positive = False
    def __init__(self, unit, time):
        self.unit = unit
        self.time = time
        #self.is_positive = False
        if self.rest_speed > self.speed:
            self.rest_speed = self.speed
    def __getattr__(self, attr):
        res = getattr(self.unit, attr)
        if attr == 'speed':
            return max(1, res - 2)
        return res


def main():
    import units
    unit = units.Swordman()
    unit.amount = 5
    decorated = StrengthSpell(unit, 2)
    print(unit.amount)
    print(decorated.amount)
    decorated.amount = 7
    decorated = decorated.decrease_effects_time()
    print(unit.amount)
    print(decorated.amount)
    decorated = decorated.decrease_effects_time()
    print(unit.amount)
    print(decorated.amount)
    a = decorated.amount
    decorated = decorated.decrease_effects_time()
    print(unit.amount)
    print(decorated.amount)
    decorated = decorated.decrease_effects_time()
    print(unit.amount)
    print(decorated.amount)
    decorated = decorated.decrease_effects_time()


if __name__ == '__main__':
    main()
    decorated = decorated.decrease_effects_time()
    print(unit.amount)
    print(decorated.amount)
    decorated = decorated.decrease_effects_time()
