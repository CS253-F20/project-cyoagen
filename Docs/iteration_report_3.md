# Iteration Report 3

## Assigned Responsibilities

- Linking Choices Together (Front-End)
    - Create Jinja code to prompt the user to select saved decision and link them together
        - Assigned To: Drew
 
- Linking Choices Together (Back-End)
    - Create Flask code to allow for linking saved choices together into a game, which is stored in the DB
        - Assigned To: Evan
        
 - Game Search
    - Write Flask code to allow for users to search for a game on the browse games page
        - Assigned To: Aaron
        
 - Game Titles
    - Write Python code to allow users to save titles for their linked choices into the database
        - Assigned To: Evan & Drew
 
	
## Tasks Completed

- Created frontend code for linking choices together
    - Wrote Jinja and HTML code to include a form on the create page that allows the user to link choices to other
    situations
        - Completed By: Drew
        
- Created backend code for linking choices together
    - Reworked database schema to better fit the needs of the application
    - Wrote Python code to link a choice to a situation in the database
        - Completed By: Evan
        
- Created frontend and backend code for searching games
    - Wrote HTML code for a page where the user can search games
    - Wrote Python code to search the database for games based on user input
        - Completed By: Aaron
        
- Reformatted HTML and CSS code to better utilize the layout page
    - Moved the code for the Navbar to the layout file and used Jinja to change the page title based on what page is
    displayed.
    - Rewrote some of the CSS code to be less brittle (it uses less absolute positioning).
        - Completed By: Drew

- Created frontend code for creating a title and description for a game
    - Wrote HTML and CSS code for a page where the user can input a title and description for their game
        - Completed By: Drew
        
- Created backend code for creating a title and description for a game
    - Reworked database schema to allow storage of titles and descriptions for games
    - Wrote Python code for creating a title and description for a game from user input
        - Completed By: Evan
    
## Tasks Not Completed

## Issues

- Brainstorming a way to link choices that would make it easy on the user as well as the developers
    - This was a difficult task, however we were able to think through it and reach a solution through collaboration
    with each other, as well as Professor Liffiton
    
- We have two failing tests at the moment due to being in th middle of finishing up a feature
    - The application works as intended right now, the tests are just failing
        - Should be fixed by finishing up the feature that allows for storing a title with its linked choice
    
## Adjustments to Overall Design

- No changes made thus far

## Helpful Tools/Processes

- Open communication was imperative for this iteration as we had multiple people working on a complex story

## Plan for Iteration 3

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
        
            

 