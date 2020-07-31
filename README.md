# Stock Exchange Simulator
### Table of Contents
##### 1. [Introduction](#Introduction)
##### 2. [Goals](#Goals)
##### 3. [Basic concepts,terms,definitions](#def)
##### 4. [Installation](#Installation)
##### 5. [Architecture](#Architecture)
##### 6. [Demonstration](#Demonstration)
##### 7. [Selection of Technologies and Instruments](#tech)
##### 8. [Conclusion ](#Conclusion )

<p></br></p>

## Introduction
An important role in the modern economy is played by the stock exchange. The stock exchange is the center of the economic life of the state; it is a place where transactions are made with securities, where various currency units are converted, where the prices of gold or oil change every second.

The main aim of the project is to build a software engine for a financial exchange. It accepts external connections from market participants and allows them to see the available orders as well as interact with them or leave their own.
<p></br></p>

## Goals:

*	Gain insight into the tasks solved by quants /quant developers at financial firms.
*	Learn about the functioning of an exchange such as order types, matching process, etc.
*	Create a working prototype potentially to be used for further student projects.

<p></br></p>

<a name="def"/>

## Basic concepts, terms, definitions
**Market Order** – an instruction to buy or sell on a trading venue such as a stock market.

**Limit order** – an order to buy an asset at no more than a specific price, or to sell a security at no less than a specific price (called "or better" for either direction).

**Fill or kill (FOK) order** – a limit order that must be executed or cancelled immediately.

**Bid** – an offer made by an investor, trader, or dealer to buy a security, commodity, or currency. 
A bid stipulates the price the potential buyer is willing to pay, as well as the quantity he or she will purchase, for that proposed price. A bid also refers to the price at which a Market Simulator is willing to buy a security. 

**Ask** – the price a seller is willing to accept for a security, which is often referred to as the offer price. 
Along with the price, the ask quote might also stipulate the amount of the security available to be sold at the stated price. The bid is the price a buyer is willing to pay for a security, and the ask will always be higher than the bid.


## Installation
The install procedure is the following:

Create a new folder.

Create and run the virtual environment:
```sh
$ virtualenv venv
$ source venv/Scripts/activate
```
If you have not used virtualenv before, consider the [guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Download the project:
```sh
$ git clone https://github.com/DKarz/Stock-Exchange-Simulator
```
Prepare the project folder:
```sh
$ mv Stock-exchange-simulation/* .
$ rm -r Stock-exchange-simulation/
```
Install the necessary modules using pip:
```sh
$ pip install -r requirements.txt
```
Launch the server using
```sh
$ cd Server/
$ python server.py
```

Here, you should either accept or reject the usage of the localhost.

Launch the graphical interface using another terminal:
```sh
$ cd GUI/
$ python GUI/main.py
```
Note that the databases are already filled with data. If you want to start with a clean market, delete all .db files from project and Server folders.

Installation via launcher: coming soon.

## Architecture
The Stock Exchange Simulator has the following architecture:
![](https://github.com/DKarz/readme-media/blob/master/guidiag1.png?raw=true)

## Demonstration
<p>
As a proper application, the simulator has a login window which allows to sign up a profile or sign in an existing profile:<br/><br/></p>
<p align="center">  <img width="450" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui1.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
As a user signs in, the following window appears.<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui2.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
  The main window has many interactive widgets that update every 3 seconds showing relevant market information. If we look at the left top corner, four buttons can be seen — the first two are BUY and SELL buttons that open corresponding dialog windows; CONFIGURING opens the settings window where the user can config the filters. The last element is the row is product Combobox – if a product is chosen in the Combobox all the data at the main window will switch to the relevant data corresponding to the product. Under the row, there is a graph area that contains the price dynamics for buy and sell orders respectively. If we look at the middle of the main window, we can see two stacks that are called “Available Bids” and “Available Asks”. Two remarks about the stacks: firstly, the orders in the stacks are merged with respect to the price i.e. if two orders have the same cost, they will be combined with the summed up amount. The second remark is that the orders in the stacks are sorted, this means that there is the best order in the market on the top of each stack. If we move to the right, we see two separate stacks that are the user order’s stack (for user’s orders that are currently in the system) and history stack (for orders that were executed). The upper bar contains essential to user information such as the time, the date, user’s name, and the balance.<br/><br/></p>
 <p align="center"> 
  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui3.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
  Let us try to buy something – we open the BUY dialog window by clicking the BUY button. The window has an edit line where the user can type the product name, however, the edit line is autocompleted with the product chosen in the Combobox. Then the user chooses the order type (Limit or FOK), amount, and price per unit. Note that the price is already autocompleted with the best price in the market. The GUI says that it is success, so the order appears in the Order’s history stack.<br/><br/></p>
 <p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui4.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
If we tried to buy something for a very low price, our order would not be executed but would go to the system orders stack:<br/><br/></p>
  <p align="center"><img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui5.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
We are able to cancel our order if we click on the order. After confirming that we, indeed want to cancel the order, it vanishes from the system. Remark, when a user has created the order, the price was subtracted from the user’s balance. If an order is canceled, the money is returned.<br/><br/></p>
<p align="center">
  <p align="center"><img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui6.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
To sell something, we need to have something. Let us look at our assets by clicking the username or the upper bar – the assets window opens that contains the relevant information about the user's assets.<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui7.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
If there are enough assets, the user is able to make sell FoK order:<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui8.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
Let us open the config window. The first tab: delete-history button, color scheme button, the checkbox that allows to join the buy and sell graphs for products; a user can inform developers about bugs occurring in the program and send it to the server which will save them to the bug_log.txt file.
The second tab consists of the user’s preferable products.
<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui9.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
Preferable products are the products the user wants to see in the Combobox, in the config he/she can add new products and delete old ones. <br/><br/></p>
<p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui10.gif?raw=true">
  <br/><br/><br/>
</p>


<p >
Apart from switching between products using Combobox, we can use shortcuts on the keyboard (1 for the first product, 2 for the second, etc.). Note that all the windows in the GUI have their shortcuts either. <br/><br/></p>
<p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui11.gif?raw=true">
  <br/><br/><br/>
</p>
The shortcuts:

Button|	Action
| ------ | ------ |
B|	BUY order window will be opened
S|	SELL order window will be opened
C|	Configuring window will be opened
A|	User assets window will be opened
0|	Chooses “No filter” in the Combobox of preferable products
1-10|	Chooses corresponding product in the Combobox



<p>
If we want to delete a product from the Combobox we can do it in the config.<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui12.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
DELETE HISTORY button clears orders in the Orders’ history stack as well orders stored by the server.<br/><br/></p>
<p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui13.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
The developers can be informant about the bugs. The message sent from config to the server will be stored in the special file. Apart from the user’s message the server receives other information. It allows us to track the last actions of the user and find out what could cause the issues.<br/><br/></p>
<p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui14-1.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
The graphs have a slider that narrows down the period of the observation. The leftist position shows the price dynamics throughout the whole period of observation. <br/><br/></p>
<p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui16.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
If you hover over at a point on the plots, the point’s precise coordinate will be shown.<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui17.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
Sometimes, it so happens that it difficult to compare the price fluctuations using two separate graphs, hence, to make the graphs’ information more readable, a user can join the buy and sell graphs. As a bonus, we have bar charts of the data distribution (Best_Ask/2 + Best_Bid/2) for the last 24 hours of observation.<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui18.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
Studying the analogues made us notice that modern graphical interfaces have dark mode feature. To be up-to-date we have added such a feature, so the color scheme of the GUI can be changed to the dark one in the config.<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui19.gif?raw=true">
  <br/><br/><br/>
</p>


<p>
Now, we are going to demonstrate two important scenarios.
The first is GUI + GUI.
If one GUI makes an order, it appears in the corresponding stack in the other GUI so it can interact with new orders. If one GUI cancels an order, it vanishes from the system, consequently in the other GUI.
<br/><br/></p>
 <p align="center"> <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui20.gif?raw=true">
  <br/><br/><br/>
</p>



<p>
The second scenario is GUI + Market Maker. As MM is launched, the GUI immediately represents the situation in the changing market. <br/><br/></p>
<p align="center">  <img width="750" src="https://github.com/DKarz/media-lfs/blob/master/GUI/gui21-1.gif?raw=true">
  <br/><br/><br/>
</p>









<a name="tech"/>

## Selection of Technologies and Instruments

The main instrument is used in the project is python and PyQt5 library for the graphical interface.
Code written in python has several benefits:
* Easy to write.
* Has extensive documentation.
* Supported by the range of different tutorials on the internet.
* Easy to read (especially important for future project participants).

After reading the project description, we understood this is a desktop application, not a website as it is connected by the localhost, so we can avoid using markup languages such as HTML. Since GUI requires importing several different libraries, python fits perfectly here.
To create modern-looking GUI we will use widgets from PyQt5 framework which has a variety of them. Another vital component of our GUI is the graph area. Here we have several good libraries, but we choose matplotlib due to the following reasons: 
* I used to work with this library in the first year of my studies.
* The library interacts well with PyQt5, unlike other graphical libraries.
* This is the most popular python graphical library; therefore, many useful materials can be found on the internet.

Note that, candlestick chart has been recently removed from matplotlib, and now it is in a separate module called mpl_finance. Additionally, some small libraries were imported – examples: “time” library to obtain relevant time, “random” library to choose randomly color of line on the graph or news from an array of news, etc. 
In general, apart from the modules mentioned above, everything was built from scratch.



##### The list of most used and important methods in GUI
|Method/Function name |	Module |	Brief description:|
| ------ | ------ | ------ |
|**startApp**|	main.py|	Imports libraries from all modules, opens the login window.
**runGUI**|	mainWindow.py|	Runs Main Window.
**reloadData**|	mainWindow.py|	Updates the orders’ stacks with the orders. Gets user's orders in the system.
**prdChanged**|	mainWindow.py|	Manages if a product in the “preferable products” Combobox is changed.
**updateGraphs**|	mainWindow.py|	Replots the matplotlib graphs with new data.
**sliderChanged1**|	mainWindow.py|	Manages if upper slider position is changed.
**sliderChanged2**|	mainWindow.py|	Manages if lower slider position is changed.
**reloading**|	mainWindow.py|	Changes the period of observation corresponding to the sliders.
**removeOrder**|	mainWindow.py|	Cancels user’s order.
**reloadSystemOrders**|	mainWindow.py|	Updates user’s orders stack.
**switchDark**|	mainWindow.py|	Switch to dark mode.
**switchLight**	|mainWindow.py|	Switch to light mode.
**setProgressVal**|	mainWindow.py|	Updates the upper bar’s data such as username balance and time.
**change_prd_keyboard**|	mainWindow.py|	Changes product in the Combobox from the keyboard.
**callConfigWindow**|	mainWindow.py|	Opens configuring window.
**call_my_assets**|	mainWindow.py|	Opens user’s assets window.
**callOrderWindow**|	mainWindow.py|	Opens order window with autocompleted data.
**addPrd**|	configWindow.py|	Adds new products to the Combobox. 
**remove_prd**|	configWindow.py|	Removes the chosen product from the Combobox.
**send_bug**|	configWindow.py|	Sends text written in edit space to the server.
**switchToDark**|	configWindow.py|	Changes mode flag to dark.
**deleteHis**|configWindow.py|	Clears order’s history and orders history stack.
**joinGraphs**	|configWindow.py|	Changes flag to join buy and sell statistics and plot box graph.
**signingIn**	|entrance.py|	Calls mainWindow if the user’s profile data is relevant.
**signingUp**	|entrance.py|	Creates a new user profile and calls mainWindow.
**buyOrder**	|functions.py|	Returns string in format:  "Buy {product name}\n {order type}    Amount: {#}    Cost: {#}".
**sellOrder**|	functions.py|	Returns string in format: "Sell {product name}\n {order type}    Amount: {#}    Cost: {#}".
**barInfo**|	functions.py|	Return string for upper bar.
**getId**|	functions.py|	Gets id of an order from string.
**getPrice**|	functions.py|	Gets the price of an order from string.
**getTime**|	functions.py|	Return time in readable string format.
**getNews**|	functions.py|	Parses msn.com/en-us/money/markets and saves news into array.
**resOut**|	functions.py|	Returns transaction data in the formatted string.
**merger**|	functions.py|	Merges stack orders at an identical price.
**upd**|	graphs.py|	CanvasUp method used to update graph.
**plot_joint**|	graphs.py|	CanvasUp method which plots buy and sell graphs together.
**no_data**|	graphs.py|	Shows NO DATA watermark if there is nothing no plot.
**reloading**|	graphs.py|	Shows RELOADING watermark if it is a process of obtaining data.
**plot**|	graphs.py|	CanvasUp method which plots buy graph.
**plot**|	graphs.py|	CanvasLow method which plots sell graph.
**candels**|	graphs.py|	CanvasLow method which plots a candlestick graph (box plot).
**runEngine**|	orderWindow.py|	Process new orders data and runs the matching process.

Some words about how GUI interacts with the server. With the help of python “socket” library, two computers connected to the localhost can exchange data. More carefully the procedure is described by my teammate who is responsible for this component. For now, let us study the following table containing a description of some important functions which are used for communication between server and GUI. All of them can be found in ```client.py``` module.

Function name|	Description
| ------ | ------ |
**get_balance**|	Returns the current user’s balance.
**known_user**|	Returns True if a user with such a login and password exists. False otherwise.
**get_history**|Returns list of user orders’ history.
**get_id**|	Returns the user’s id.
**process**|Runs the matching process.
**register**|	Creates a new user.
**stats**|	Returns data required for the graph area.
**bug_log**|Reports about bugs.
**update**|Gets orders’ stack updates.
**box_graph**|	Returns data needed in the graph area in the boxplot.
**my_assets**|	Returns list of user’s assets.

 A couple of words about multithreading: our GUI runs several processes simultaneously – apart from the main process which is the main functionality of the graphical interface such as the ability to click buttons, there are other functions launched no mater user’s actions:
*	**getUpdate** – every two seconds asks server about changes in the chosen product, asks about the user’s order status.
*	**setProgressVal** – sets relevant upper bar data such as time and balance.
*	**printNews** – sets news in the lower bar.
*	**updateGraphs** – gets information about product prices from the server, replots the graphs.

Now, let us study how ```mainWindow.py``` is connected with the range of all other files. Again, their interaction is much more complex, however, the following diagram provides an essential understanding of the application composition:


![](https://github.com/DKarz/readme-media/blob/master/arc.jpg?raw=true)

Brief description of the files shown in the diagram:
* ```mainWindow.py``` – file containing the class mainWindow and its methods.
* ```orderWindow.py``` – file containing the class Ui_DialogOrder.
* ```function.py``` – file containing auxiliary functions that are not methods of classes.
* ```graphs.py``` – file containing two canvas classes and their methods.
* ```configWindow.py``` – file containing class Ui_DialogConfig.
* ```assets.py``` – file containing the implementation of assets window showing assets of the users.
* ```data.py``` – file containing variables used in all other files.
* ```styles.py``` – file containing different stylesheets used in the project in string format.
* ```client.py``` – file containing the implementation of methods for communication with the server part.


## Conclusion
In order to invest successfully, you need to organize the process properly. Technically it can be done by software that helps to search for and buy assets, as well as monitor the status of the portfolio.

To be profitable, the trader needs to be aware of all the latest events and conduct qualitative analysis. Well-organized information allows you to predict further changes in the exchange rate more accurately and speculate on it.

If earlier you had to make requests to the company to receive financial reports or study various magazines, today, to get up-to-date data, it is enough to have a computer and "know where to look".
