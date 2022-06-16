from copy import deepcopy
from enum import Enum, auto, unique


@unique
class Spell(Enum):
    MAGIC_MISSILE = auto()
    DRAIN = auto()
    SHIELD = auto()
    POISON = auto()
    RECHARGE = auto()

    def get_mana_cost(self):
        match self:
            case Spell.MAGIC_MISSILE:
                return 53
            case Spell.DRAIN:
                return 73
            case Spell.SHIELD:
                return 113
            case Spell.POISON:
                return 173
            case Spell.RECHARGE:
                return 229

    def get_effect_turns(self):
        match self:
            case Spell.MAGIC_MISSILE:
                return 0
            case Spell.DRAIN:
                return 0
            case Spell.SHIELD:
                return 6
            case Spell.POISON:
                return 6
            case Spell.RECHARGE:
                return 5

    @staticmethod
    def list():
        return list(map(lambda c: c, Spell))


class Entity:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def deal_damage(self, damage):
        self.hp -= damage

    def is_dead(self):
        return self.hp <= 0


class Player(Entity):
    def __init__(self, hp, mana):
        self.hp = hp
        self.damage = 0  # Damage is dealt by player via spells
        self.effects = {}   # Track active effect and remaining turns
        self.mana = mana
        self.total_mana_spent = 0   # Track total mana expended by player
        self.armour = 0  # Player armour rating can be modified by spells

    def deal_damage(self, damage):
        damage_to_deal = damage - self.armour
        if damage_to_deal < 1:
            damage_to_deal = 1
        self.hp -= damage_to_deal

    def can_cast_with_mana(self, spell):
        return self.mana >= spell.get_mana_cost()

    def cast_spell(self, spell, enemy):
        # Check if player has enough mana remaining
        if self.mana < spell.get_mana_cost() or spell in self.effects.keys():
            return False
        # Expend mana to cast spell
        self.total_mana_spent += spell.get_mana_cost()
        self.mana -= spell.get_mana_cost()
        match spell:
            case Spell.MAGIC_MISSILE:
                enemy.deal_damage(4)
            case Spell.DRAIN:
                enemy.deal_damage(4)
                self.heal(2)
            case Spell.SHIELD:
                self.effects[spell] = spell.get_effect_turns()
                self.armour += 7
            case Spell.POISON:
                self.effects[spell] = spell.get_effect_turns()
            case Spell.RECHARGE:
                self.effects[spell] = spell.get_effect_turns()
        return True

    def process_effects(self, enemy):
        effects_to_remove = []
        for (effect) in self.effects.keys():
            self.effects[effect] -= 1
            match effect:
                case Spell.SHIELD:
                    if self.effects[effect] == 0:
                        self.armour -= 7
                        effects_to_remove.append(effect)
                case Spell.POISON:
                    enemy.deal_damage(3)
                    if self.effects[effect] == 0:
                        effects_to_remove.append(effect)
                case Spell.RECHARGE:
                    self.mana += 101
                    if self.effects[effect] == 0:
                        effects_to_remove.append(effect)
        for effect in effects_to_remove:
            self.effects.pop(effect)

    def heal(self, hp):
        self.hp += hp


def main():
    input = process_input_file()
    p1_solution = solve_part1(input)
    print("P1 solution - {}".format(p1_solution))
    p2_solution = solve_part2(input)
    print("P2 solution - {}".format(p2_solution))


def process_input_file():
    with open("./inputs/day_22.txt") as file:
        enemy_stats = {}
        for line in file.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            sep = line.split(": ")
            enemy_stats[sep[0]] = int(sep[1])
        return Entity(enemy_stats["Hit Points"], enemy_stats["Damage"])


def solve_part1(input):
    boss = deepcopy(input)
    player = Player(50, 500)
    least_mana_for_win = conduct_fight(player, boss)
    return least_mana_for_win


def solve_part2(input):
    ()


def conduct_fight(player, boss):
    mana_observed = []
    conduct_fight_recursive(player, boss, mana_observed)
    return min(mana_observed)


def conduct_fight_recursive(player, boss, mana_observed):
    if len(mana_observed) > 0:
        print(min(mana_observed))
    # Select player spell
    for spell in Spell.list():
        # Copy player and boss
        new_player = deepcopy(player)
        new_boss = deepcopy(boss)
        # Player turn
        # - Process player effects and check if boss is dead
        new_player.process_effects(new_boss)
        if new_boss.is_dead():
            mana_observed.append(new_player.mana)
            return
        # - Cast spell
        mana_check = new_player.can_cast_with_mana(spell)
        if not mana_check:
            return
        _good_cast = new_player.cast_spell(spell, new_boss)
        # - Check if boss is dead
        if new_boss.is_dead():
            mana_observed.append(new_player.mana)
            return

        # Boss turn
        # - Process player effects and check if boss is dead
        new_player.process_effects(new_boss)
        if new_boss.is_dead():
            mana_observed.append(new_player.mana)
            return
        # - Boss deal damage to player
        new_player.deal_damage(new_boss.damage)
        # - Check if player is dead
        if new_player.is_dead():
            return
        # Player and boss still alive, so go to next turn
        conduct_fight_recursive(new_player, new_boss, mana_observed)


if __name__ == "__main__":
    main()
