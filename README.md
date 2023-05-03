# OpenAI Telegram Bots
Implementations using different OpenAI models: davinci, Dall-E, gpt-3.5-turbo.


### Set Up
Set the environment variables **OPENAI_API_KEY** and **TG_TOKEN**. <br>
Also there is a restriction for the user, so for any of these implementations **USER1_TG_ID** should be also added as an environment variable.

Add these variables and your values into ~/.profile file:
```sh
export OPENAI_API_KEY=YOUR_PERSONAL_API_KEY_INSTED_OF_THIS
export TG_TOKEN=YOUR_PERSONAL_TELEGRAM_BOT_TOKEN
export USER1_TG_ID=YOUR_TELEGRAM_USER_ID
```


#### Install dependencies
```sh
pip3 install -r requirements.txt
```

## To run in background
```sh
python3 davinci.py &
```

## To run after reboot
Copy file to bin folder:
```sh
sudo cp -i /path_to/davinci.py /bin/davinci.py
```

Open crontab editor
```sh
sudo crontab -e
```

Add:
```sh
@reboot python3 davinci.py &
```
