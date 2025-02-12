# AI-Chat-Bot
![Screenshot (53)](https://github.com/culexculex/AI-Chat-Bot/assets/45868768/8bedc9d9-8c59-4bcb-b542-e7209a17d672)
The task is to develop an AI chat bot tailored specifically for assisting users navigating an ed-tech website with the intention to purchase courses using pre trained model for NLP(Natural language processing) from hugging face. The chat bot should efficiently address user queries, provide relevant information about courses, and offer personalized recommendations to enhance user experience and increase course sales.

To create an AI Chat Bot based on the provided problem statement with the specified features and FAQ database, you would typically follow these steps. This assumes you have a Python environment set up on your system:

Requirements to install

Python (3.6 or higher)

pip (Python package installer)

Pandas

Transformers

Data set from hugging face

streamlit

Installation:

```pip install transformer```

```pip install python```

```pip install pandas```

```pip install streamlit```

Data set link:

https://huggingface.co/datasets/rajpurkar/squad_v2

In Transformers

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"

# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
QA_input = {
    'question': 'Why is model conversion important?',
    'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
}
res = nlp(QA_input)

# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

Demo video

https://github.com/culexculex/AI-Chat-Bot/assets/45868768/f708ba67-a212-4952-b7da-839b6c6c9a4e


The More You Analyze, More You Get Insights from the Data.



