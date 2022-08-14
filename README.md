# Project 2 | A 'Numbers Guy' Playing Wordle

A couple months back, 
a good mate of mine tried convincing me and another friend to start playing this game, 
he was claiming it would be a great addition to our morning coffee.
Little did he know how much joy it would bring to our morning routine.

## Files uploaded

- Uploaded 2 files:
	- "PDF - A Numbers Guy Playing Wordle": PDF, full documentation of the thought process solving the challenge.
	- "wordle_solver": py file, code for public use, implements the final strategy presented in the PDF.
				
## 'How To' (.py file)
- set-up: download the .py file, open using terminal or any IDE.
	- terminal: (windows) save the file on DESKTOP, open CMD, type: 'cd Desktop' press Enter, type 'py wordle_solver.py' press Enter (must have python installed on computer).

- run & play:
	- 0. open "https://www.nytimes.com/games/wordle", This is where you'll play Wordle and get the feedback from the guessed words.  
	- 1. At the start of every round, your required to type your 5 letter "Input guess" (the word you guessed in the real game). Type the 5 letter word and press Enter. 
	- 2. Input information - input the feedback received from the official game. 
		- Green letters - type the green tile letters, seperate with ', ' and press Enter. Example: if you chose the word 'alone' and the first 3 letters came back green, your input would be: "a, l, o" + Enter.
		- Yellow letters - type the yellow tile letters, seperate with ', ' and press Enter.
		- Black letters - type the black tile letters, seperate with ', ' and press Enter.

	* If there's a color which didnt appear - press enter to continue.* 

	- 3. The program will present the top 3 ranked words by the calculated metrics and as well as the 'Recommended word'. (The recommended word wont always be the top ranked word shown, due to the strategy used. For instance, first 3 rounds the recommended word is usually a word without repeated letters, while the top ranked word is biased towards 'strong letters' which repeat themselve)
	- 4. New round, return to point 1 until youve guessed right.

	* You dont have to choose the recommended word, feel free to try any word you'd like* 

- winning/losing: The program will only know youve won if the recommended word was the last in the archive of words. Otherwise, you'll just need to close the terminal. In the case of losing, well, the program knows you only have 6 attempts and it'll know you've lost. 
