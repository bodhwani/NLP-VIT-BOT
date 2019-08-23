# Capstone Project - VITChatbot [English]
A Rasa based chatbot that uses a custom NLU pipeline and the standard RASA-core to create an informative chatbot for resources related to VIT University.

[Complete Project Report](https://drive.google.com/open?id=1QHwH1nPXLzOzjrHOYsYjBkJEEoaMx7uR)

![Workflow](https://github.com/karth2512/NLP-VIT-BOT/blob/master/images/ERD.PNG)
## Features
### NLU Pipeline
The pipelinbe consist of the following stages:
- Tokenization - Splitting into smaller lexical units
- Acronym replacement - factoring in the popular neologisms, slangs and acronyms
- Spelling correction - Correcting spelling to prevent loss of information/context
- Lemmatization - Reducing polymorphisms
- Vectorization - Word to Vector conversion
- Intent Classification - Convoluted Neural Nets to match the intent.

### Fallback/Sentimental Analysis
- In the case that the queried intent does not match any of the responses in the database then a Quora search is made and the best response is displayed.
- Sentimental Analysis of the responses are done to prevent displaying sensitive or highly negative sentences.

### User Interface
- Clean, Plain UI with minimal buttons.
![User Interface](https://github.com/karth2512/NLP-VIT-BOT/blob/master/images/UI.PNG)

### Feedback/Rating 
- A rating opiton in the UI enables the user to convey their level of satisfaction while using the product.
- The users also have an option to report bugs and unexpected erroneous scenarios by attaching a snapshot of the conversation.

### Misc. Features 
- Speech and Voice assist: As an optional mode of communication, we use Speech-toText and Text-to-Speech to provide a more lively and convenient interface. 
- Socket communication: The user inputs are relayed via sockets to the backend server running the core chatbot framework.
- Natural Language Processing: We use a power set of language processing tools to recognize and disambiguate the meaning of the user’s input. These processes include tokenization, lemmatization, POS tagging etc.
- Deep Learning: We use Convoluted neural networks to train our classifiers that help to discern the users motive and suggest suitable responses to make conversation.- Chatbot response: The chatbot replies to the input query either by providing relevant text and links or by asking further questions to clarify the context.
- Expandable scenarios: The conversational flows are created in such a way that it can be expanded to match modern scenarios. The processes of adding conversations by the developer is quick, easy and modularized.

### Dependencies
- Beautiful Soup: Beautiful Soup provides a few simple methods and Python idioms for navigating, searching, and modifying a parse tree using Python parsers like lxml and html5lib. It automatically converts incoming documents to Unicode and outgoing documents to UTF-8.    
- Text Blob: Text Blob is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as partof-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.    
- Pandas: pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with “relational” or “labelled” data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, real world data analysis in Python. 
- NumPy: NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.  
- Anaconda: — Anaconda is the world’s most popular Python data science platform. Anaconda, Inc. continues to lead open source projects like Anaconda, NumPy and SciPy that form the foundation of modern data science. Anaconda’s flagship product, Anaconda Enterprise, allows organizations to secure, govern, scale and extend Anaconda to deliver actionable insights that drive businesses and industries forward. 
- NLTK: NLTK is a leading platform for building Python programs to work with human language data. 


## Version Change Log
- v1.0.0 Added Academics and subbranches (UG,PG,Research,International/IR), Added intent for International Relations
- v1.1.0 file structure for nlu training data and stories under data/nlu/ and data/stories/ , Updated Make commands , Campus life(Fests,Clubs)
- v1.2.0 Added Academics section.
- v1.2.0 Campus Life(Chapters)
- v1.2.1 Stopword temp fix.
- v1.3.1 Dockerfile added and deployed successfuly.
- v1.4.0 Chatbot-UI
- v1.4.1 Campus life story fix.
- v1.5.0 Hyper Linking and New line formattion , respective UI changes
- v1.5.1 Bug fix [Remove common words in the dataset]
- v1.6.0 Search in quora added
- v1.6.1 Bug fix [Removed affirmations]
- v1.7.0 Added Sentimental Analysis. 
- v1.8.0 Custom NLU Pipeline added


### Note:
Run "make model_remove" after doing changes in the dataset. 
Run "make train-resetall" to remove exiting models, train new nlu and train new core models
