# Iteration Report 4

## Assigned Responsibilities

- Write tests for implemented features
    - Create tests in the tests.py file that test functionality of the features we have implemented thus far
        - Test for expected and unexpected behavior of features
            - Assigned To: Team
            
- Finish code for saving a title linked to a set of choices
    - Write frontend and backend code that allows a user to create a title and description that will be linked to a set
    of choices
        - This is nearly done, just needs to be finished and polished
            - Assigned To: Evan and Drew
            
- Have users be able to create a game and see it on the browse games page
    - Polish and tidy up each individual's work so that this experience is achievable by the end of the week
        - The parts should mostly be there, now we just need to make the last touches to make sure they all work
        together
            - Assigned To: Team
        
	
## Tasks Completed

- Implemented Bootstrap into most html files
    - Switched styling for most frontend code to be done using Bootstrap rather than just CSS
        - Completed By: Drew
        
- Wrote tests for implemented features
    - Created tests in the tests.py file that test functionality of the features we have implemented thus far
        - Test for expected and unexpected behavior of features
            - Completed By: Team
            
- Added checks for unexpected behavior
    - Created various if statements to catch where fields could receive unexpected inputs and made sure to show errors
        -Completed By: Evan
            
- Added a title to each situation
    - Created a new field for each situation that is a short title to be displayed during linking
        -Completed By: Drew & Evan

- Have users be able to create a game and see it on the browse games page
    - Polish and tidy up each individual's work so that this experience is achievable by the end of the week
        - The parts should mostly be there, now we just need to make the last touches to make sure they all work
        together
            - Assigned To: Team
  
## Tasks Not Completed

- All Planned Tasks Were Completed

## Issues

- No Major Issues Were Encountered This Week
    
## Adjustments to Overall Design

- We reordered the process of creating a game, opting to allow users to create choices as a part of each game
which differed from the original plan to allow users to create choices and then select them to be part of a game.
    - This required database changes, as well as an adjustment to the flow of the website.
    
## Helpful Tools/Processes

- The bootstrap documentation was incredibly helpful in the conversion of the site to the new bootstrap formatting
    - https://getbootstrap.com/docs/4.5/getting-started/introduction/

## Plan for Iteration 4

- Play Button
    -  Create a clickable play button to allow for users to begin playing each game and deliver them to a playing screen
        - Assigned To: Aaron
    
- Finishing the Game (Front-End)
    - Allow for a user to navigate through each game by making decisions. This will entail creating a Jinja template for
    displaying the choices that is robust and can adapt to dynamic content
        - Assigned To: Drew
            
- Finishing the Game (Back-End)
    - Allow for a user to navigate through each game by making decisions. This will handle following the choices in the
     database and passing them to the front-end based on user input
        - Assigned To: Evan