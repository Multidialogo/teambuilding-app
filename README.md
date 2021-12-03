### Requirements ###

1. Make sure you have 'git' installed on your system/environment
2. Make sure your current directory is the project's root folder
3. From the terminal, run the following code:

```
git checkout -- *
```
4. Make sure your Python is installed on your system/environment
5. Rename the sample.env file to .env, and edit it with your variables
6. Run the following code to migrate:

```
python manage.py migrate
```

7. (Optional) Make sure your debug enviroment is setup. If you don't use 
   VSCode, you can delete the .vscode folder, and you can change/delete 
   the docker-compose.debug.yml file.