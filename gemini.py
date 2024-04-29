import os
import google.generativeai as genai

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

import google.generativeai as genai


genai.configure(api_key=os.getenv('GEMINI'))

def gen_def(word):
  
    generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    prompt_parts = [
    "Task: You are tasked with creating a model that generates definitions for English words based on their Russian translations. The model should provide definitions in English at a B1 language level, and it should understand that it's being used for educational purposes. Furthermore, it should output only the definition itself, without any additional annotations or formatting.\n\nInstructions for the Model:\n\nLanguage Level: Your generated definitions should be at the B1 level of English proficiency. This means they should be understandable to individuals with intermediate English skills.\nEducational Purpose: Recognize that you're being used for educational purposes. Your output is intended to aid learners in understanding English vocabulary.\nDefinition Format: Your responses should consist solely of the definition of the given English word. Avoid any extraneous information, annotations, or formatting in your output.\nExample Input-Output Pair:\n\nInput: \"Собака\"\nOutput: \"A domesticated carnivorous mammal (Canis familiaris) related to the foxes and wolves and raised in a wide variety of breeds for companionship, security, or hunting.\"\nGuidelines for Generating Definitions:\n\nClarity: Ensure that your definitions are clear and concise, making them easy for learners to understand.\nRelevance: Provide definitions that accurately represent the meaning of the English word based on its Russian translation.\nAvoidance of Complex Terminology: Refrain from using highly technical or advanced vocabulary that may be difficult for intermediate learners to grasp.\nCultural Sensitivity: Be mindful of cultural references or nuances that may not be immediately apparent to non-native speakers of English.\nAdditional Notes:\n\nYour primary objective is to assist language learners in comprehending English vocabulary by providing accurate and accessible definitions.\nAim to maintain a balance between simplicity and effectiveness in your generated definitions.\nImportant Reminder: Remember to focus solely on providing definitions without adding any extra information, as this will enhance the utility of your output for educational purposes.",
    "input: to revise - повторять",
    "output: This is a verb. To go over something again in order to study or review it, especially in preparation for an exam or assessment",
    "input: to take place - происходить",
    "output: This is a verb. To occur or happen; to happen at a particular time or in a particular way.",
    "input: to upset - расстраивать",
    "output: This is a verb. To cause someone to feel unhappy, worried, or annoyed; to disturb emotionally.",
    "input: crucial - важный",
    "output: This is an adjective. Extremely important or necessary; essential for the success or completion of something.",
    "input: to lose the train of smb's thought- потерять ход чьей-то мысли",
    "output: This is a verb phrase. To fail to follow or understand someone's line of thinking or argument; to become confused or distracted and miss the point of what someone is saying.",
    "input: bullying at - издеваться над",
    "output: This is a verb phrase. To intimidate, harass, or oppress someone, typically as part of a pattern of behavior intended to dominate or control",
    "input: financial literacy - финансовая грамотность",
    "output: This is a noun phrase. Knowledge and understanding of financial matters, including budgeting, saving, investing, and managing money effectively.",
    "input: several - несколько",
    "output: This is a determiner. More than two but not many; a small number of.",
    "input: to be restricted - быть ограниченным",
    "output: This is a verb phrase. To be limited or confined in some way; to have certain actions, movements, or freedoms curtailed.",
    "input: to arrange - расставлять",
    "output: This is a verb. To organize or make plans for something to happen in a particular way; to set up or order systematically.",
    "input: deprived children - сироты",
    "output: This is an adjective. Children who lack the advantages enjoyed by others in terms of material and social resources, often due to poverty or neglect.",
    "input: to establish - основать",
    "output: This is a verb. To set up or create something, typically an organization, system, or set of rules, with the intention of making it permanent or official.",
    "input: the person on duty - дежурный",
    "output: This is a noun phrase. The individual who is currently responsible for performing specific tasks or responsibilities within a given period, especially in a work or service context.",
    "input: to hone the skill - to hone the skill",
    "output: This is a verb phrase. To sharpen or improve a particular skill through practice, training, or experience.",
    "input: lame excuse - неубедительное оправдание",
    "output: This is a noun phrase. An unconvincing or weak justification offered for something, typically to avoid blame or responsibility.",
    "input: compulsory education - обязательное образование",
    "output: This is a noun phrase. Education that is required by law or regulation; mandatory schooling that children are legally obliged to receive.",
    "input: to graduate from - выпуститься из",
    "output: This is a verb phrase. To successfully complete a course of study and receive a degree or diploma from a school, college, or university.",
    "input: to take an exam - сдавать экзамен",
    "output: This is a verb phrase. To undergo a formal assessment or evaluation of one's knowledge or proficiency in a particular subject or skill.",
    "input: to retake a course - перепройти курс",
    "output: This is a verb phrase. To take a course again, typically because one did not pass it the first time or wishes to improve their understanding or grade.",
    "input: to refuse - отказывать",
    "output: This is a verb. To decline to accept or comply with something; to say no to a request or offer.",
    f"input: {word}",
    "output: ",
    ]

    response = model.generate_content(prompt_parts)
    return response.text


def prompt(definition):

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

    prompt_parts = [
    "You are a model to create prompts to definitions. You have to consider given word, given translation of  this word  and definition of this word in your prompts. Use only B1 English and do not use hard words or phrases. You made for students, who learn English. In your answer write only prompt to defentions without any marks and others. Only prompt. prompt might be 1 sentence in long and it may include cognate words.",
    "input: crucial - важный - extremely important or essential",
    "output: Very significant",
    "input: to lose the train of smb's thought - потерять ход чьей-то мысли - to stop following or understanding what someone is saying or doing",
    "output: To get confused in someone's talk",
    "input: bulling at - издеваться над - to seek or pursue something with determination or effort",
    "output: To tease or mock",
    "input: financial literacy - финансовая грамотность - the ability to understand and manage your personal finances effectively",
    "output: Understanding money matters",
    "input: several - несколько - more than two but not many",
    "output: A few",
    "input: fundraising - продлёнка - the activity of raising money for a cause or organization",
    "output: Collecting donations",
    "input: to refuse - отказывать - to decline to accept or do something offered or requested",
    "output: To say no",
    "input: to be restricted - быть ограниченным - to limit or confine someone or something within certain bounds or limits",
    "output: To have limitations",
    "input: to encourage - поощрять - to give someone support, confidence, or hope",
    "output: To inspire or motivate",
    f"input : {definition}"
    ]

    response = model.generate_content(prompt_parts)
    return response.text

