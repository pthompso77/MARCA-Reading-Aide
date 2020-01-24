#!/usr/bin/env python3

import cgi, cgitb; cgitb.enable()
import os

form = cgi.FieldStorage()
try:
	userInput = form.getvalue('userInput')
except:
	userInput = '[error getting userInput]'

""" ---------------------------------------------------
HTML
"""

print('Content-type: text/html\r\n\r\n')
print('''

<!doctype html>
<head>
	<title>Summarize!</title>
	<script src="js/xhr.js"></script>
	<meta charset="utf-8">
  <meta name="description" content="Summarize any length of text">
  <meta name="keywords" content="Summary, Abstract, NLP, Computer science, artificial intelligence">
  <meta name="author" content="Peter T">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<style>
		* {
			box-sizing: border-box;
  background-color: #f1f1f1;
		}
/*
justify-content		align the flex items horizontal (side to side in container)
						(default: flex-start)
align-items			Vertically aligns the flex items when the items do not use all available 
					space on the cross-axis
						(default: stretch) stretches the space
align-content		Modifies the behavior of the flex-wrap property. It is similar to align-
					items, but instead of aligning flex items, it aligns flex lines
						(default: stretch) stretches items
*/
		
.flex-container {
	min-height: 500px;
  display: flex;
/*	flex-direction: row;*/
/*	flex-wrap: wrap;*/
	flex-flow: row wrap;
/*	justify-content: space-between;*/
/*	align-items: center;*/
	align-content: center;
}

/*
The flex item properties are:
order
flex-grow
flex-shrink
flex-basis
flex
align-self
*/
#input-section {
/*	order: 2;*/
	flex-grow: 2;/* default is 0
/*	flex-shrink: 0; default is 1*/
	flex-basis: 320px;
/*	align-self: center; (overrides anything defined in the flex container) */ 
}
		
/*		this is a flex item*/
.flex-container > section {
  background-color: #f1f1f1;
  margin: 10px;
  padding: 20px;
  font-size: 30px;
/*  min-width: 300px;*/
	flex: 1 0 300px;
}
		h1{
			font-family: "PT Sans";
    font-size: 32px;
    font-weight: 400;
    font-style: normal;
    text-decoration: none;
    text-transform: none;
    color: #000;
/*    background-color: initial;*/
    line-height: 42px;
    letter-spacing: normal;
    text-shadow: none;
		}
		h2 {
			    font-family: "PT Sans";
    font-size: 32px;
    font-weight: 400;
    font-style: italic;
    color: #808080;
    line-height: 62px;
		}
		h3 {
			    font-family: "PT Sans";
    font-size: 26px;
    font-weight: 400;
    font-style: normal;
    text-decoration: none;
    text-transform: none;
    color: #000;
    background-color: initial;
    line-height: 33px;
    letter-spacing: normal;
    text-shadow: none;
			    padding-top: 0;
    text-indent: 0;
    padding-bottom: 0;
    padding-right: 0;
    text-align: left;
		}
		p, p *{
			    font-family: Lato;
    font-size: 20px;
/*    text-align: left;*/
		}
		
/*		FOR LEFT SIDE: TEXT CONTAINER*/
		
		#text-container, .container {
			min-width: 200px;
			min-height: 100px;
			display: flex;
/*			flex-direction: row;*/
			flex-flow: row wrap;
/*			justify-content: flex-end;*/
			align-content: space-between;
		}
		#text-input {
/*
			flex-basis: 400px;
			flex-basis: 100%;
*/
			flex: 1 0 100%;
			min-height: 200px;
		}
		#submit-text {
			flex: 0 0 100px;
			align-self: flex-end;
			font-family: "Helvetica Neue", sans-serif;
    font-size: 20px;
			
    text-align: center;
			margin-top: 20px;
    padding: 15px; 
    border: 1px solid #52646f;
    border-radius: 24px;
    background-color: #82939e;
		}
		
		
		.arg {
/*			todo*/
/*			align-self: flex-start;*/
		}
		
/*		FOR GENERATED TEXT (only visible after generation)*/
		.generated p {
/*			visibility: hidden;*/
		}
		
</style>
</head>

<!--A Flexible Layout must have a parent element with the display property set to flex. Direct child elements(s) of the flexible container automatically becomes flexible items.-->

<body>
	<div class="flex-container">
		<section id="input-section">
			<h1>Insert Text to Summarize Below</h1>
			<div id="text-container">
				<textarea id="text-input" name="userInput" form="text-form" required>'''
	  + userInput +
				'''</textarea>
			</div>
			<form id="text-form" action="results.py" method="post">
<!--			<form id="text-form" onsubmit="tryXHR()" action="ajax.py" method="post"> -->
			<input type="submit" id="submit-text" value="Summarize"/>
				</form>
		</section>
<!--		end of input-section-->
		
		<section id="summary-section">
			<h2>Summary</h2>
			<div id="summary-container" class="generated">
				<article id="keywords">
				<h3>Key words and phrases</h3>
				<p  class="container">
					Key, word, phrase, empty, lonely, 
					'''+ userInput[0:10] +'''
				</p>
					</article>
				<article id="arguments" >
				<h3>Arguments</h3>
				<p  class="container">
				<span class="arg">Text must be full for processing.</span>
					<span class="arg">Emptiness means nothing.</span>
				</p>
					</article>
			</div>
<!--			end summary container-->
		</section>
<!--		end of summary-section-->
		
	</div>
</body>


''')
