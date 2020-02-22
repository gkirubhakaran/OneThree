# OneThree
TakeHome Challenge Webscrapping

This Python script was created on version 3.7 (and works on 2.7 as well)
It performs webscrapping on Drugbank website 

There are two ways to run this script

1. For the Predefined list of Drug IDs (10 of those from the PDF) you can just run the following command on your terminal 

            python WebscrapingOneThree.py 
            
Please make sure you're on the right directory
This command runs the script and displays the output on the terminal itself. Feel free to comment out the output display and uncomment the last line to store the output in an excel file

2. For a specific drug that you're looking for, add the Drug ID at the end of the script. For example,

            python WebscrapingOneThree.py DB00274
            python WebscrapingOneThree.py DB00274,DB01053

Please avoid spaces or other characters on the argument section where you provide the Drug IDs
