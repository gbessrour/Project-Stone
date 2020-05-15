# project-stone
This is a Discord bot inspired by Mecha Senku from the anime Dr. Stone
To run locally, just use the command ```python3 mechaSenku.py```

# Scripts
This project contains two scripts:
1) ```.upload.sh```:  This script will take care of pulling the code, adding code, committing code, and pushing code. First, to edit it, I recommend using ```dos2unix``` so it can have the correct formatting. Then to compile it, run ```source [directory]/.upload.sh``` in the correct directory. Once that is done, just run it by calling ```upload```. It will prompt you to enter the commit message and to select the branch that you want to push to.

2) ```.heroku_logs.sh```: This script will show you the Heroku logs for your app (if it is hosted on Heroku). Just like the previous script, I recommend using ```dos2unix``` for editing it. To compile it, run ```source [directory]/.heroku_logs.sh``` in the correct directory. Once that is done, just run it by calling ```heroku_logs```. It will prompt you to login to Heroku and then enter the app name.

# Commands
```!help``` will show you all the commands that you can ask MechaSenku to do for you.
```!help [command]``` will show you the description of the specific command selected.