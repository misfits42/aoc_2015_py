"""
Solutions for AOC 2015 Day 22.
"""


from copy import deepcopy
from enum import Enum, auto, unique


@unique
class Spell(Enum):
    """
    Represents the different spells that the player is able to cast, with some
    of the spells setting multi-turn effects on the player.
    """

    MAGIC_MISSILE = auto()
    DRAIN = auto()
    SHIELD = auto()
    POISON = auto()
    RECHARGE = auto()

    def mana(self):
        """
        Gets the mana cost required to cast the spell.
        """
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
        """
        Gets the number of turns that the effect generated by the spell lasts
        for.
        """
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
        """
        Returns a list containing each unique member of the Spell enum-class.
        """
        return list(map(lambda c: c, Spell))


class Entity:
    """
    Represents a basic entity that has HP, armour and can deal damage.
    """

    def __init__(self, health, damage, armour):
        """
        Creates a new Entity initialised with the given values.
        """
        self.health = health
        self.damage = damage
        self.armour = armour

    def deal_damage(self, damage, ignore_armour=False):
        """
        Deals damage to the Entity, taking into account its armour rating. If
        the armour would reduce the damage dealt to less than 1, the damage
        dealt is set to 1.
        """
        # Modify the damage to be dealt if not ignoring armour
        damage_to_deal = damage
        if not ignore_armour:
            damage_to_deal -= self.armour
        if damage_to_deal < 1:
            damage_to_deal = 1
        self.health -= damage_to_deal

    def heal(self, health):
        """
        Increases the HP of the Entity by the given amount.
        """
        self.health += health

    def is_dead(self):
        """
        Checks if the Entity is dead due to having no more HP left.
        """
        return self.health <= 0


class Player(Entity):
    """
    A Player represents an enhanced Entity that causes damage by casting magic
    spells.
    """

    def __init__(self, health, mana):
        """
        Creates a new Player with the given HP and mana as starting values.
        Damage rating and armour are set to 0, since a Player deals damage and
        modifies their armour rating through magic spells.
        """
        Entity.__init__(self, health, 0, 0)
        self.active_effects = {}   # Track active effect and remaining turns
        self.mana = mana
        self.total_mana_spent = 0   # Track total mana expended by player

    def can_cast_with_mana(self, spell):
        """
        Checks if the Player has enough mana to cast the specified spell.
        """
        return self.mana >= spell.mana()

    def is_effect_active(self, spell):
        """
        Checks if the Player currently has the given spell as an active effect.
        """
        return spell in self.active_effects

    def cast_spell(self, spell, enemy):
        """
        Allows the Player to cast the spell, targeting the given enemy Entity.
        """
        # Check if player has enough mana remaining
        if not self.can_cast_with_mana(spell) or self.is_effect_active(spell):
            return
        # Expend mana to cast spell
        self.total_mana_spent += spell.mana()
        self.mana -= spell.mana()
        match spell:
            case Spell.MAGIC_MISSILE:
                enemy.deal_damage(4)
            case Spell.DRAIN:
                enemy.deal_damage(2)
                self.heal(2)
            case Spell.SHIELD:
                self.active_effects[spell] = spell.get_effect_turns()
                self.armour += 7
            case Spell.POISON:
                self.active_effects[spell] = spell.get_effect_turns()
            case Spell.RECHARGE:
                self.active_effects[spell] = spell.get_effect_turns()

    def process_effects(self, enemy):
        """
        Processes any active effects on the Player (including those which may
        deal damage to the given enemy Entity), reducing active effect turn
        counters and removing any effects that expire (turn counter becomes 0).
        """
        effects_to_remove = []
        for effect in self.active_effects:
            # Reduce effect turns remaining by 1
            self.active_effects[effect] -= 1
            match effect:
                case Spell.SHIELD:
                    if self.active_effects[effect] <= 0:
                        self.armour -= 7
                        effects_to_remove.append(effect)
                case Spell.POISON:
                    enemy.deal_damage(3)
                    if self.active_effects[effect] <= 0:
                        effects_to_remove.append(effect)
                case Spell.RECHARGE:
                    self.mana += 101
                    if self.active_effects[effect] <= 0:
                        effects_to_remove.append(effect)
        for effect in effects_to_remove:
            self.active_effects.pop(effect)


def process_input_file():
    """
    Processes the AOC 2015 Day 22 input file into the input required by the
    solver functions. Returned data structure is a boss Entity with the specs
    given in the input file.
    """
    with open("./input/day_22.txt", encoding="utf-8") as file:
        enemy_stats = {}
        for line in file.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            stat_split = line.split(": ")
            enemy_stats[stat_split[0]] = int(stat_split[1])
        return Entity(enemy_stats["Hit Points"], enemy_stats["Damage"], 0)


def solve_part1(input_data):
    """
    Solves AOC 2015 Day 22 Part 1 // Conducts a fight between the player and the
    boss, returning the least amount of mana the player needs to spend to beat
    the boss.
    """
    boss = deepcopy(input_data)
    player = Player(50, 500)
    least_mana_for_win = conduct_fight(player, boss, False)
    return least_mana_for_win


def solve_part2(input_data):
    """
    Solves AOC 2015 Day 22 Part 2 // Conducts a fight between the player and the
    boss in hard mode (player loses 1 HP at start of each of their turns before
    any effects are processed), returning the least amount of mana the player
    needs to spend to beat the boss.
    """
    boss = deepcopy(input_data)
    player = Player(50, 500)
    least_mana_for_win = conduct_fight(player, boss, True)
    return least_mana_for_win


def conduct_fight(player, boss, hard_mode):
    """
    Conducts the fight between the player and boss, returning the least amount
    of mana the player needs to spend to still beat the boss.
    """
    min_mana = []
    conduct_fight_recursive(player, boss, min_mana, hard_mode)
    if len(min_mana) == 1:
        return min_mana[0]
    else:
        return -1


def conduct_fight_recursive(player, boss, min_mana, hard_mode):
    """
    Conduct one step in the fight between player and boss, making recursive
    function calls to proceed to the next step in a fight.
    """
    # Select player spell
    for spell in Spell.list():
        # Copy player and boss
        new_player = deepcopy(player)
        new_boss = deepcopy(boss)
        # Player turn
        # If in hard mode, apply damage to player before other effects
        if hard_mode:
            new_player.deal_damage(1, True)
        # Check if player is dead
        if new_player.is_dead():    # Player loses
            return
        # Process player effects and check if boss is dead
        new_player.process_effects(new_boss)
        if new_boss.is_dead():  # Player wins
            if len(min_mana) == 0:
                min_mana.append(new_player.total_mana_spent)
            elif min_mana[0] > new_player.total_mana_spent:
                min_mana[0] = new_player.total_mana_spent
            return
        # Player loses if they do not have enough mana to cast a spell
        can_cast = new_player.can_cast_with_mana(spell)
        if not can_cast:    # Player loses
            return
        # If spell cannot be cast due to active effect, continue to next spell
        if new_player.is_effect_active(spell):
            continue
        new_player.cast_spell(spell, new_boss)
        # - Check if boss is dead
        if new_boss.is_dead():  # Player wins
            if len(min_mana) == 0:
                min_mana.append(new_player.total_mana_spent)
            elif min_mana[0] > new_player.total_mana_spent:
                min_mana[0] = new_player.total_mana_spent
            return

        # Boss turn
        # - Process player effects and check if boss is dead
        new_player.process_effects(new_boss)
        if new_boss.is_dead():  # Player wins
            if len(min_mana) == 0:
                min_mana.append(new_player.total_mana_spent)
            elif min_mana[0] > new_player.total_mana_spent:
                min_mana[0] = new_player.total_mana_spent
            return
        # - Boss deal damage to player
        new_player.deal_damage(new_boss.damage)
        # - Check if player is dead
        if new_player.is_dead():    # Player loses
            return
        # Player and boss still alive, so go to next turn
        conduct_fight_recursive(new_player, new_boss, min_mana, hard_mode)
