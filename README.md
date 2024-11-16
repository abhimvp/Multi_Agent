# Multi_Agent

- ### ADVANCED Python AI Multi-Agent Tutorial (RAG, Streamlit, Langflow & More!) - From TechWithTim YT

- Build an advanced multi-agent AI app through Python, Langflow, Astra DB, Streamlit, and more. This app will use multiple LLMs that to handle different tasks, routing those tasks to different LLMs, and will even have a full frontend that allows you to interact with the completed application.
- python for coding
- Streamlit for handling the front-end and interacting with our LLMs (Python UI library)
- LangFlow - low-code visual editor that allows us to build out advanced AI flows
- AstraDB for vector database as we're going to be implementing some retrieval augmented generation features inside of this app.

### Video Resources 🎞

- Get started with DataStax: https://dtsx.io/techwithtim-astradb
- Langflow Github Rep: https://dtsx.io/techwithtim-langflow
- Check out DataStax AI PaaS: https://dtsx.io/techwithtim-aipaas
- Code in this video (prompts/code/flows): https://github.com/techwithtim/Advanced-Multi-Agent-Workout-App

### LangFlow Setup

- It is a low code editor for building AI applications & we can interact with langflow by running the flow locally or we can use an API that's hosted by langFLow , provided by datastax also provided astraDB - which is a vector capable database, which means we can actually perform the vector search operations.
- Go to https://www.langflow.org/ and create an account & click on build with langflow , click on New Flow ( AI Project) -> Blank FLow
- let's build a `Simple flow` -> That recommends the macros like the protiens the calories , the fat and the carbs based on a user's profile & give it a name = `Macro Flow` & endpoint name = `macros` -> endpoint is what you'll be calling when you want to use this flow , as all of these flows will actually be accesible via a public API & you need a token in order to use them
  - From our python code , we can just send a simple request to this `/macros` endpoint which will be hosted by LangFlow & we provide our token and start using it.
- A FLow always begins with some kind of input that can be a text input(coming from the api) or chat input(coming from chat window from the playground tab (where we can mess with out flows))
  - We start with Two Text Inputs - one is Goals & other is Profile
    - first thing i want to pass to my model is the various goals that we have ( like gain muscle or lose fat) so that we can recommend the different macros for this particular user.
    - second is how much do u weigh , what is your gender & what's your activity level - we need to know that in order to generate the correct macros
- Now we have our goals and profile info & next we need to do is we're going to funnel this into a prompt ( drag and drop and click on prompt window - where we can put in any prompt we want - to generate some result from the AI from LLM) - Inside of prompt if you want to have some kind of variables , some dynamic information , you can put those inside of curly braces - prompt Variables - something like {profile} , {goals} - looks something like this :
  ![alt text](Images/image.png)
- now i have two new inputs to my prompt - goals and profile & just connect the goals & profile text inputs to prompt & now whatever i put into these inputs will be passed into this prompt templates as goals and profile variable & obviously we need to tell the prompt what to do - let's paste in the prompt available from the resources macro.txt

````
Based on the following user profile, please calculate the recommended daily intake of protein (in grams), calories, fat (in grams), and carbohydrates (in grams) to achieve their goals. Ensure that the response is in JSON format with no additional explanations or text.

User Profile: {profile}

Goals: {goals}

Output Format:
Return the result in JSON format only, with the keys: "protein", "calories", "fat", and "carbs". Each key should have a numerical value. Do not include any additional text or explanations, only the JSON object.

Output Format
    "protein": ,
    "calories": ,
    "fat": ,
    "carbs":

Notes:
Ensure you do not include ```json ``` in the response, simply give me a valid json string with no formatting or display options
````

- now next step is to pass this into a llm -> go to models - iam going to use google generative AI model & connect prompt to model input & provided my GOOGLE_API_KEY & model - gemini-1.5-pro
- next is to provide some output - we use a text output & overall flow looks like this :
  ![alt text](Images/image_1.png)
- we can test this by running the play buttons & want to run it as a whole - go to playground - pass it info and run flow
  - Goals : fat loss , Profile : weight : 120kg , height: 183cm , gender:male - then run all the components
  - output : {"protein": 180, "calories": 2200, "fat": 60, "carbs": 150}
    ![alt text](Images/image_2.png)
