# ONU

## How to Run
Ensure you have all of the perquisites, then
```
python ONU.py
```

## How To Build
```
pip install pyinstaller
pyinstaller ONU.spec
```
An executable will be generated at `dist/ONU.exe`.


## Features
### Current features
* Clickable cards  
* Draw a card button - add random card to hand  
* Discard pile  
* Card validation - is card playable  
* AI player 
* Player turn indicator, player names
* When rendering hand, there might be more than 1 row of cards. Must specify the amount of cards in each row
* Change wild card to random color selection  
* End of game detection  
* Functionality of special cards: draw 2, skip, etc.  
* Only show card back for AI Player. Have the game enter debug mode when the user presses 'D' on keyboard.
In debug mode, the UI shows the cards in the AI player's hand.  

### Features to implement

### Canceled features
* Announce ONU  
* For wild cards, must have UI element for player to select the color  
