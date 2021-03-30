
Aim: Given 2 sequences, T and P, find whether P occurs exactly wihtin T.
If it does, return the location of P in T.

# string_matcher.py

string_matcher is a program that performs exact string matching by using the following algorithms:

- Brute-force search
- Knuth-Morris-Pratt
- Boyer-Moore
- Rabin-Karb

## Installation

string_matcher uses Python 3 standard libraries.
If you have installed Python 3 before, no additional package is needed.
If not, you may install Python 3 from "https://www.python.org/downloads/".
Make sure you have selected the appropriate distribution for your operating system.

## Usage

You can run the program using terminal.

The syntax:

"python string_matcher.py 'text.fa' 'pattern.fa' 'algorithm'"

'text.fa' 		: File in the FASTA format, containing the text T in which the pattern will be searched
'pattern.fa'	: File in the FASTA format, containing the pattern P to be searched in T
'algorithm" 	: The name of the algorithm to be used during search
					Appropriate names are:
					- 'brute-force' for Brute-force search
					- 'kmp' for Knuth-Morris-Pratt
					- 'boyer-moore' for Boyer-Moore
					- 'rabin-karb' for Rabin-Karb
					
Example:

Input >>> python string_matcher.py "hw1example.fa" "hw1patternT.fa" "rabin-karb"

Output >>>
Using  rabin-karb algorithm ...
Total number of comparisons: 308
Matching done in 0.00 microseconds.
The pattern is matched at position starting from  230 .


