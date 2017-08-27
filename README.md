# PyPokertools

## The project

This is a sample of Python code from a larger No-Limit Texas Hold'em (NLHE)
poker analysis project. It may be of interest to someone building their own
poker library.

You can find many other examples of poker programs online, most of which deal
with random dealing, ranking hands, keeping track of betting etc. This project
has a different focus. It is designed to solve more unusual analysis problems
that I encountered as a professional poker player such as finding
isomorphic/canonical representations of the flop, and finding nuanced hand
properties (e.g. having 'three-to-a-straight' and 'two overcards') rather than
'which hand ranks higher'.

## In this repository

- pokertools.py: building custom containers of cards and hands
- bluffing.py: finding nuanced flop hand properties for bluffing
- translation.py: parsing PokerStove-style card notation using a tokeniser
- isomorph.py: working with suit isomorphisms on the flop

## A Note on Terminology

The word 'hand' in poker is ambiguous. It could mean: the two hole cards I have
been dealt; the best 5-card poker hand I can make with any combination of my
hole cards and the board; the unit of a poker game starting with dealing hole
cards and ending with the winner collecting the pot.

In this library, the first two meanings are important to distinguish. I reserve
`holecards` for the former and `hand` for the latter.

## TODO

Some of the techniques in the above have been used to create an approximate
Nash Equilibrium strategy solver for a simplified version of NLHE. One day I
might release more code from that project, such as:

- a tool to construct simplified NLHE game trees recursively
- an iterative constraint-satisfaction algorithm using NumPy to split ranges
of holecards into e.g. betting and checking actions according to given criteria
such as equity and polarity
- a tool using the 'sklearn' machine learning framework to analyse hand
history data
