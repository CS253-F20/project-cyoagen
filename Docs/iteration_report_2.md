# Iteration Report 1

## Assigned Responsibilities

- Finish log in and log out features
    - Link already existing log in and log out code to database.
        - Assigned to: Evan
    
- Create New Choices (Display)
    - Html, CSS, and Javascript for the UI for creating a new choice for a game.
        - Assigned to: Drew
    
- Create New Choices (Backend)
    - Python backend code for created a new choice for a game and inserting it into a database.
        - Assigned to: Evan
    
- Browse Games
    - Create page for browsing games. Will not be able to actually browse yet but will have the page ready for when it
      is possible.
        - Assigned to: Aaron
	
## Tasks Completed

- Implemented Storage of Credentials
    - Finished Credential Storing
    - Implemented a salted and hashed password storage using werkzeug.

- Completed Log In and Log Out Feature
    - Allowed for calls to database comparing credentials, with notifications about errors.
   
- Created a new page for Create New Choice
    - Provided a template for displaying the page for creating and storing new pages.
    - Wrote new CSS to modify the page and increase the usability
    
- Integrated the Create New Choice template with back-end scripts for database
    - Added code to pull data from the Create Page
    - Pioneered new data storage format for tracking decisions
    
- Created Browse Games Template
    - Wrote a Jinja template to display a browse games page
    
- Resolved issues with Git and .idea files
    - Removed unneeded files from Git repository
    - Update Git Ignore file to include extra and local files
    
## Tasks Not Completed

- None. We greatly exceeded our expected productivity

## Issues

- Project Configuration Files
    - In the process of removing the .idea files, some local files were lost that 
    allowed the project to run
    - We resolved this by utilizing Git's log of what the files looked like and recreating them.

## Adjustments to Overall Design

- No changes made thus far.

## Helpful Tools/Processes


## Plan for Iteration 3

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
    - Write Python code to allow users to save titles for their linked choices into the databse
        - Assigned To: Evan & Drew
 
