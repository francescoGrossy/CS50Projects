from ast import And, Not, Or
import imp
from re import A
from symtable import Symbol
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnave, AKnight),
    Or(And(AKnight, AKnave), And(AKnave, Not(AKnight)))  #I must consider both options: both A is a Knight and a Knave in his sentence
)



# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(AKnave, And(AKnave, BKnight)),
    Or(AKnight, And(AKnave, BKnave))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(And(AKnight, BKnight), And(AKnave, BKnave)),
    Or(And(BKnight, AKnave), And(BKnave, AKnight)),
    Or(And(AKnight, BKnight), And(AKnave, BKnight)),
    Or(And(BKnight, AKnave), And(BKnave, AKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    # Basic knowledge
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    
    # First A sentence
    Or(
        And(AKnight, Implication(AKnight, AKnight)),
        And(AKnave, Not(Implication(AKnight, AKnight)))
    ),
    
    # First B sentence
    Or(
        And(BKnight, Implication(AKnight, AKnave)),
        And(BKnave, Not(Implication(AKnight, AKnave)))
    ),
    
    # Second B sentence
    Or(
        And(BKnight, CKnave),
        And(BKnave, Not(CKnave))
    ),
    
    # C sentence
    Or(
        And(CKnight, AKnight),
        And(CKnave, Not(AKnight))
    )
)

    



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
    
