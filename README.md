# Project 2 | A 'Numbers Guy' Playing Wordle

A few months ago, a good mate of mine tried convincing me and another friend to start playing this game; he was claiming it would be a great addition to our morning coffee. Little did he know how much joy it would bring to our morning routine. 

## Files uploaded 📁

- Uploaded 2 files:
	- "PDF - A Numbers Guy Playing Wordle": PDF, full documentation of the thought process solving the challenge.
	- "wordle_solver": py file, code for public use, implements the final strategy presented in the PDF.
				
## 'How To' (.py file) 📚
- set-up: download the .py file, open using terminal or any IDE.
	- Terminal: (windows) save the file on DESKTOP, open CMD, type: 'cd Desktop' press Enter, type 'py wordle_solver.py' press Enter (must have python installed on computer).

- run & play:
	1. open https://www.nytimes.com/games/wordle, This is where you'll play Wordle and get the feedback from the guessed words.  
	2. At the start of every round, your required to type your 5 letter "Input guess" (the word you guessed in the real game). Type the 5 letter word and press Enter. 
	3. Input information - input the feedback received from the official game. 
		1. Green letters - type the green tile letters, seperate with ', ' and press Enter. Example: if you chose the word 'alone' and the first 3 letters came back green, your input would be: "a, l, o" + Enter.
		2. Yellow letters - type the yellow tile letters, seperate with ', ' and press Enter.
		3. Black letters - type the black tile letters, seperate with ', ' and press Enter.

		**If there is a color which didnt appear - press enter to continue.** 👍

	4. The program will present the top 3 ranked words by the calculated metrics and as well as the 'Recommended word'. The recommended word wont always be the top ranked word shown, due to the strategy used.
	5. New round, return to stage ii until you have guessed the right word. 👆

		**You dont have to choose the recommended word, feel free to try any word you'd like.** 👍


