**WIP**

# python-gpt

## Getting Started
Clone Repository (or use the template to create your own repository)
```
git clone https://github.com/engageintellect/python-gpt.git
```

### Setup Environment

Create a config file for your OpenAI API key
```
sudo nvim /etc/python-gpt.json
```
It should look something like this:
```
{
	"OPENAI_API_KEY": "<your key here>"
}
```

Now, create a virtual environment and install the requirements
```
cd python-gpt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
Start your server
```
uvircorn main:app --reload
```

### Test
Test your api in your terminal with curl
```
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, ChatGPT!"}' http://localhost:8000/chat
```

