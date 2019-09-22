# Reinforcement Learning for Wonder Boy (Sega Master System)

[Overview](#overview)  
[Testing preview](#testing-preview)  
[What is LUA](#lua)  
[Bizhawk](#bizhawk)  
[Setup](#setup)  
&nbsp;&nbsp;&nbsp;[Get the sources](#get-sources)  
&nbsp;&nbsp;&nbsp;[Install and configure Bizhawk](#setup-bizhawk)  
&nbsp;&nbsp;&nbsp;[Install and configure Python](#setup-python)  
[How to train the agents](#how-to-train)  
&nbsp;&nbsp;&nbsp;[Start the agent (python)](#how-to-train-python)  
&nbsp;&nbsp;&nbsp;[Launch the ROM in the emulator and start the LUA script](#how-to-train-lua)      
[Environment](#environment)  
&nbsp;&nbsp;&nbsp;[State](#state)  
&nbsp;&nbsp;&nbsp;[Action Space](#action-space)  
&nbsp;&nbsp;&nbsp;[Reward Function](#reward-function)  
[Result](#result)  
&nbsp;&nbsp;&nbsp;[Random state to action policy](#result-random-policy)  
&nbsp;&nbsp;&nbsp;[Deep Q learning](#deep-q-learning)  


<a id="overview"></a>
## Overview
I started this project because I had no time to play games anymore.  
Its ultimate goal is to set up an agent that will be able to finish the Wonder Boy game on the Sega Master System at my place.  
Here are the main parts of the chosen technical solution:
  * an emulator (Bizhawk) that will run the game
  * a LUA script that will
    * init a socket client
    * grab, preprocess and send observations
    * take actions
    * control the emulator
  * a python script with socket server and different learning reinforcement methods will
    * receive observations
    * train the models (dynamic programming, deep neural networks, evolutive neural network with genetic algorithms...)
    * return action(s)

<a id="testing-preview"></a>
## Testing preview
Once trained, the python agent will be able to play the game by itself:  
![](https://github.com/guerinsylvain/bot-wonder-boy/blob/master/images/preview.gif)

<a id="lua"></a>
## What is LUA
[Lua](https://www.lua.org/about.html) is a powerful, efficient, lightweight, embeddable scripting language.   
It supports procedural programming, object-oriented programming, functional programming, data-driven programming, and data description.  

<a id="bizhawk"></a>
## Bizhawk
[BizHawk](https://github.com/TASVideos/BizHawk) is a multi-system emulator written in C#.  
BizHawk provides nice features for casual gamers such as full screen, and joypad support in addition to full rerecording and debugging tools for all system cores.  
LUA Functions available inside Bizhawk are documented [here](http://tasvideos.org/Bizhawk/LuaFunctions.html).

<a id="setup"></a>
## Setup
<a id="get-sources"></a>
### Get the sources
You may
* close this github repository 
* or download a zip containing the latest version or a given release of the code
<a id="setup-bizhawk"></a>
### Install and configure Bizhawk
1.  Run the PowerShell script bizhawk.ps1 located in the folder "setup".  
    To install it, right-click it and select "Run with PowerShell".  
    This will download & install a fresh copy of BizHawk with all the required files in their correct locations.  
    Special thanks to [TestRunnerSRL](https://github.com/TestRunnerSRL) for this script !  

    Start Bizhawk and go to Config -> Customize... -> Advanced and set Lua Core to Lua+LuaInterface.  
    NLua does not support LuaSockets properly.  
    After changing this setting, you need to close and restart the emulator for the setting to properly update.  
2.  Download the Sega Master System Bios Version 1.3 (Usa, Europe) from this [link](http://www.planetemu.net/rom/sega-master-system/bios-sega-master-system-usa-europe-v1-3-1)
    Unzip the content of the file in the "Firmware" folder located below "BizHaw-2.3".
3.  Download the ROM of the Wonder Boy game from this [link](https://wowroms.com/en/roms/sega-master-system/download-wonder-boy-usa/58110.html).
    Create a new folder "SMS" below the "BizHaw-2.3".
    Copy the zip in it.
<a id="setup-python"></a>
### Install and configure Python 
1.  Install [Python 3.7 or later](https://www.python.org/downloads/).
2.	From the root folder of the project, type 
    ```
    pip install virtualenv
    ```
3.	Then type
    ```
    virtualenv --python="C:\Users\[YOUR USER NAME]\AppData\Local\Programs\Python\Python37\python.exe" venv      
    ```
    This will create a venv subfolder.   
    Note that the path to the python.exe (v3.7) may vary on your machine.
    If python has been installed with visual studio, you may have something similar to this:
    ```
    virtualenv --python="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" venv
    ```
4.	From the root folder of the project, activate the virtual environment by typing:
    ```
    .\venv\Scripts\activate.bat
    ```
5. Install packages:
    ```
    cd scripts\client
    pip install -r requirements.txt   
    ```
<a id="how-to-train"></a>
## How to train the agents
The following steps have to be done in the described sequence:
<a id="how-to-train-python"></a>
### Start the agent (python)
1.	From the root folder of the project, activate the virtual environment by typing:
    ```
    .\venv\Scripts\activate.bat
    ```
2.  Launch the training script:
    ```
    cd scripts\client
    python train.py
    ```
<a id="how-to-train-lua"></a>
### Launch the ROM in the emulator and start the LUA script    
1.  Start BizHawk
2.  In the "File" menu, chose "Open ROM".  
    Select the file "Wonder Boy (USA, Europe).zip" that you have previously copied in the "SMS" folder below "BizHawk-2.3".
3.  Select "Lua Console" in the "Tools" menu.  
    The "Lua Console" window opens.
4.  In the "Script" menu of the "Lua Console" window, select "Open Script...".   
    Select the file "train.lua" located in scrips/bizhawk

The training should start.
If anything goes wrong, please review the [Setup section](#setup)

<a id="environment"></a>
## Environment

<a id="state"></a>
### State
The state is observed at each frame and is composed of the following informations:  
* a screenshot (will be sent to clipboard by Lua script)  
* the wonderboy vitality/health (memory address 0x0C36 in Main RAM that varies from 0 to 12)  

Bizhawk offers RAM search and RAM watch tools to help you find the memory address of a specific value or move.  
Here is a great [tutorial](https://www.youtube.com/watch?v=zsPLCIAJE5o&t=2064s) by The8bitbeast.

<a id="action-space"></a>
### Action Space

BUTTON 1 = LEFT  
BUTTON 2 = RIGHT  
BUTTON 3 = ACCELERATE/FIRE  
BUTTON 4 = JUMP  

| Values        | BUTTONS              |
| ------------- | -------------------- |
| 0             | LEFT                 |
| 1             | LEFT + FIRE          |
| 2             | LEFT + JUMP          |
| 3             | LEFT + FIRE + JUMP   |
| 4             | RIGHT                |
| 5             | RIGHT + FIRE         |
| 6             | RIGHT + JUMP         |
| 7             | RIGHT + FIRE + JUMP  |
| 8             | FIRE                 |
| 9             | JUMP                 |
| 10            | FIRE + JUMP          |
| 11            | NONE                 |

<a id="reward"></a>
### Reward Function
The difference of vitality/health after each action and extra bonus at the end of a level.

<a id="result"></a>
## Result
<a id="result-random-policy"></a>
### Random state to action policy
As expected an agent with a random state to action policy is not able to finish the first level of the game.
<a id="deep-q-learning"></a>
### Deep Q learning (yet to be implemented...)

1. Init <em>replay memory</em> capacity
2. Init the <em>policy network</em> with random weights
3. Clone the policy network and call it the <em>target network</em>
4. For each <em>episode</em>
   1. Init the starting state
   2. For each <em>time step</em>
      1. Select action (via exploration or exploitation)
      2. Execute selected action in an emulator
      3. Observe reward and next state
      4. Store experience in replay memory
      5. Sample random batch from replay memory
      6. Preprocess states from batch
      7. Pass batch of preprocessed states to policy network
      8. Calculate <em>loss</em> between output Q-values and target Q-values
         * Requires a pass to the target network for the next state
      9. Gradient descent updates weights in the policy network to minimize loss
         * After some time steps, weights in the target network are updated to the weights in the policy network
      

