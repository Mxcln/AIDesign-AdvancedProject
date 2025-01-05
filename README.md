# AiDesign-AdvancedProject

- [Introduction](#introduction)
- [Team members](#team-members)
- [Project Structure](#project-structure)
- [Detailed Description](#detailed-description)
    - [TCG Design Agent](#tcg-design-agent)
    - [Prompt](#prompt)
    - [Fine Tuning](#fine-tuning)
    - [Dataset](#dataset)
    - [Summarizer](#summarizer)
- [How to Use](#how-to-use)
    - [Installation](#installation)
    - [Running the Agent](#running-the-agent)
    - [Fine-Tuning](#fine-tuning-1)
    - [Generating Dataset](#generating-dataset)
- [Test Results](#test-results)
    - [Archetype Design](#archetype-design)
    - [Single Card Design](#single-card-design)
    - [Archetype/Card Modification](#archetypecard-modification)
    - [Lua Script Generation](#lua-script-generation)

This is the repository for the advanced project of the course AI Design 2H2024. 

## Introduction
Trading Card Game (TCG) design is crucial for delivering engaging gameplay experiences, as it involves balancing card mechanics, themes, and artwork to keep players invested. The TCG Design Agent presented here streamlines this creative process by leveraging AI-driven approaches to ideate, refine, and execute card concepts for Yu-Gi-Oh! and other TCGs. By integrating fine-tuning and summarization utilities, this tool provides context-aware recommendations and helps produce consistent, high-quality card designs at scale.

## Team members

- [Yang Yuanda/杨远达](21307140079@m.fudan.edu.cn); Student ID: 21307140079
- [Li Xinran/李欣然](21307140025@m.fudan.edu.cn); Student ID: 21307140025


## Project Structure
In this repository, you will find the following files:
1. `dataset/` - a folder containing the dataset of the agent for fine-tuning, and the Python script to make the dataset.
2. `fine-tuning/` - a folder containing the fine-tuning script.
3. `summarizer/` - a folder containing the class summarizer, which is used to generate the historic summary as prompt for the agent.
4. `prompt.txt` - a file containing the prompt for the agent.
5. `tcg-design-agent.py` - the main Python script for the agent.
6. `requirements.txt` - a file containing the required libraries for the agent.
7. `README.md` - a file containing the detailed information about the agent and how to use it.

## Detailed Description

### TCG Design Agent
The TCG Design Agent is a Python-based AI agent designed to assist with the design of trading card games, especially Yu-Gi-Oh. The agent uses OpenAI's GPT-4 model to generate responses based on user input and a predefined prompt. It maintains a summary of the conversation history to provide context for ongoing interactions.

The agent is capable of **designing new archetypes**, **creating single cards**, and **modifying existing cards or archetypes**. More significantly, it can **generating Lua scripts** for card effects in YGOPro (a popular Yu-Gi-Oh! simulator) style, which can be directly used in the simulator for people to play with the card. 

The main class `TCGDesignAgent` in the `tcg-design-agent.py` script is the core component of the agent. It handles the interaction with the GPT-4 model, manages the conversation history, and generates responses based on user input. A typical conversation code snippet is as follows:

```python
def chat_with_model(self, prompt, user_input, model="gpt-4"):
    try:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
```

### Prompt
The `prompt.txt` file defines specific tasks for the TCG Design Agent:
- [archetype design]: Creates a new archetype, listing each card with details like type, attribute, stats, and effect.
- [single card design]: Designs a single, fully described card when the user specifies key attributes (name, type, etc.).
- [lua script]: Generates Lua scripts for a card's effects in YGOPro, a popular Yu-Gi-Oh! simulator.
- [change]: Modifies an existing card or archetype, preserving the defined output format.

### Fine Tuning

The fine-tuning process involves training the model on a specific dataset to improve its performance for the TCG design task. Because the available TCG data on the internet can be relatively limited or unfocused, fine-tuning on a curated dataset ensures the model learns from directly relevant examples. This specialized approach boosts accuracy and reliability when designing new cards or archetypes. The dataset is generated and processed using scripts provided in the `dataset/` and `fine-tuning/` folders.

A typical fine-tuning process involves the following steps, according to the OpenAI documentation:
1. Create a dataset of examples relevant to the task.
2. Submit the dataset to the OpenAI API for fine-tuning.
3. Start the fine-tuning process and monitor the model's progress.
4. Finish fine-tuning and get the fine-tuning model's ID.

After the fine-tuning process is complete, the model is ready to generate responses based on the TCG design prompt. In our case, the fine-tuned model's ID is `ft:gpt-4o-mini-2024-07-18:noobility::AlX20DFH`.

You can check the `fine-tuning/fine-tuning.py` script for more details on the fine-tuning process.

### Dataset
Fine-tuning the agent requires a dataset of TCG design examples. And the dataset should follow some specific formats to ensure the model learns effectively, like:
```json
{
    "messages": [
        {
            "role": "system", 
            "content": "You are a happy assistant that puts a positive spin on everything."
        }, 
        {
            "role": "user", "content": "I fell off my bike today."
        }, 
        {
            "role": "assistant", "content": "It's great that you're getting exercise outdoors!"
        }
    ]
}
```

The dataset for fine-tuning the agent is stored in the `dataset/` folder. It includes JSONL files that contain the training data. The `ft-dataset.py` script is used to create and manage the dataset.

For our TCG Design Agent, we decide to enhance the dataset with more examples of lua scripts, because we find that the agent is not very good at generating lua scripts due to the lack of training data. So we find the [YGOPro GitHub repository](https://github.com/Fluorohydride/ygopro-scripts) and extract the data from it to enrich the dataset.
The dataset should contain two parts: user input and assistant response.
* User input: The user asks the agent to generate a lua script for a specific card effect. Thankfully, a database file `card.cdb` is provided in the repository, which contains the card information and all the card effects. We can use this file to generate the user input. Considering it's in sqlite format, we can use the `sqlite3` library to read the data.
* Assistant response: The assistant generates the lua script for the card effect. So we can use the script in YGOPro repository to generate the assistant response.

Unfortunatly, we are not able to fine-tune with all the data we have, because of the limited time and high cost of the OpenAI API. So we only fine-tune the model with a small part of the dataset. `dataset/dataset-all.jsonl` contains all the data we have, and `dataset/dataset.jsonl` contains the data we use for fine-tuning.

You can check the `dataset/ft-dataset.py` script for more details on how to generate the dataset.


### Summarizer
The `Summarizer` class, located in the `summarizer/` folder, is responsible for generating a summary of the conversation history. 
The reason to do this is that OpenAI's api does not support the context-aware conversation, so we need to provide the context to the agent. Considering the conversation history can be very long, and will finally break the token limit of the api, we decide to use the summarizer to generate a summary of the conversation history. The summary will be used as part of the prompt to provide context for the agent's responses.

You can see how the summarizer works in the following code snippet:
```python
    # in tcg-design-agent.py
    def chat(self, user_input):
        prompt = self.prompt("prompt.txt")
        if self.history_summary:
            prompt += f"Historic message summary: {self.history_summary}"
        response = self.chat_with_model(prompt, user_input)
        new_context = f"Previous Summary: {self.history_summary}\nUser: {user_input}\nAssistant: {response}"
        self.history_summary = self.summarizer.summarize_text(new_context)
        return response
```

## How to Use

### Installation
To install the required libraries, run:
```sh
pip install -r requirements.txt
```

### Running the Agent
To run the agent, execute the `tcg-design-agent.py` script:
```sh
python tcg-design-agent.py
```
The agent will start a chat session where you can interact with it. Type 'exit' to quit the session.

### Fine-Tuning
To fine-tune the agent, use the scripts provided in the `fine-tuning/` folder. Follow the instructions in the `fine-tuning.py` script to start the fine-tuning process.

### Generating Dataset
To generate the dataset for the agent, use the `ft-dataset.py` script in the `dataset/` folder. This script will create the necessary JSONL files for training.

## Test Results

Here are some examples of the agent's responses to user input. If you know Yu-Gi-Oh! or other TCGs, you can see that the agent is capable of generating detailed and context-aware card designs, archetypes, and Lua scripts.

### Archetype Design
```
You: [archetype design] An archetype focus on battle phase. 2 monster, 1 normal spell, 1 continuous spell, no trap.

[1] Card name: Battlebound Guardian;
Type: Monster;
Attribute: Earth;
Level: 4;
ATK: 1800;
DEF: 1200;
Effect: If this card is Normal or Special Summoned to your field, you can add 1 "Battlebound" Spell Card from your Deck to your hand, except "Battlebound Guardian". During your Main Phase, you can activate one of these effects;
- This turn, if you battle an opponent's monster, your battling monster gains 600 ATK during the Damage Step only.
- You can make this card attack directly this turn.

[2] Card name: Battlebound Berserker;
Type: Monster;
Attribute: Fire;
Level: 5;
ATK: 2300;
DEF: 1500;
Effect: Once per turn, during your Battle Phase, you can make this card gain 300 ATK for each monster your opponent controls, until the end of the turn. If this card destroys an opponent's monster by battle, you can inflict 500 damage to your opponent.

[3] Card name: Battlebound Charge;
Type: Spell;
Sub-Type: Normal;
Effect: During your Battle Phase, increase the ATK of all monsters you currently control by 500 until the end of that turn.

[4] Card name: Battlebound Onslaught;
Type: Spell;
Sub-Type: Continuous;
Effect: All "Battlebound" monsters you control can attack an additional time during each Battle Phase. If a "Battlebound" monster you control destroys an opponent's monster by battle, you can draw 1 card. You can only activate one "Battlebound Onslaught" per turn.
```

### Single Card Design
```
You: [single card design] Design a normal trap for "Battlebound" archetype. two effect: when activated, boost 300 
atk of all archetype monster; banish from grave, all archetype monster can attack directly

AI: [1] Battlebound Fury: Normal Trap; Effect: When this card is activated, all "Battlebound" monsters currently on the field gain 300 ATK until the end of this turn. You can banish this card from your Graveyard; all "Battlebound" monsters you control can attack your opponent directly this turn.
```

### Archetype/Card Modification
```
You: [change] change the second effect of "Battlebound Fury" that : only one of the archetype monster can attack directly

AI: 1. [Battlebound Fury]: Normal Trap; Effect: Once per turn, when a "Battlebound" monster declares an attack: You can activate this effect; that monster gains 500 ATK for that battle. If that monster destroys an opponent's monster by battle, it can make a second attack in a row. If this card is sent from the field to the graveyard: You can banish this card from your graveyard; until the end of your next turn, one "Battlebound" monster you control can attack your opponent directly.
```

### Lua Script Generation
```
You: [lua script] make a lua script for "Battlebound Fury"

AI: --Battlebound Fury
local s,id,o=GetID()
function s.initial_effect(c)
        --draw
        local e1=Effect.CreateEffect(c)
        e1:SetDescription(aux.Stringid(id,0))    
        e1:SetCategory(CATEGORY_DRAW)
        e1:SetType(EFFECT_TYPE_ACTIVATE)
        e1:SetProperty(EFFECT_FLAG_PLAYER_TARGET)
        e1:SetCode(EVENT_FREE_CHAIN)
        e1:SetCountLimit(1,id+o)
        e1:SetTarget(s.drawtg)
        e1:SetOperation(s.drawop)
        c:RegisterEffect(e1)
        --direct attack
        local e2=Effect.CreateEffect(c)
        e2:SetDescription(aux.Stringid(id,1))
        e2:SetType(EFFECT_TYPE_SINGLE+EFFECT_TYPE_TRIGGER_O)
        e2:SetCode(EVENT_LEAVE_FIELD)
        e2:SetProperty(EFFECT_FLAG_DELAY)
        e2:SetCondition(s.directcon)
        e2:SetTarget(s.directtg)
        e2:SetOperation(s.directop)
        c:RegisterEffect(e2)
        --boost
        local e3=Effect.CreateEffect(c)
        e3:SetDescription(aux.Stringid(id,2))
        e3:SetType(EFFECT_TYPE_FIELD)
        e3:SetCode(EFFECT_UPDATE_ATTACK)
        e3:SetRange(LOCATION_SZONE)
        e3:SetTargetRange(LOCATION_MZONE,0)
        e3:SetTarget(aux.TargetBoolFunction(Card.IsSetCard,0xffd))
        e3:SetValue(500)
        c:RegisterEffect(e3)
end
function s.drawfilter(c)
        return c:IsFaceup() and c:IsSetCard(0xffd)
end
function s.drawtg(e,tp,eg,ep,ev,re,r,rp,chk)
        if chk==0 then return Duel.IsExistingMatchingCard(s.drawfilter,tp,LOCATION_MZONE,0,1,nil) end
        Duel.SetTargetPlayer(tp)
        Duel.SetTargetParam(1)
        Duel.SetOperationInfo(0,CATEGORY_DRAW,nil,0,tp,1)
end
function s.drawop(e,tp,eg,ep,ev,re,r,rp)
        local p,d=Duel.GetChainInfo(0,CHAININFO_TARGET_PLAYER,CHAININFO_TARGET_PARAM)
        Duel.Draw(p,d,REASON_EFFECT)
end
function s.directcon(e,tp,eg,ep,ev,re,r,rp)
        local c=e:GetHandler()
        return not c:IsReason(REASON_RETURN) and c:IsPreviousLocation(LOCATION_FZONE) and c:GetPreviousControler()==tp
end
function s.directfilter(c)
        return c:IsSetCard(0xffd) and c:IsType(TYPE_MONSTER) and c:IsFaceup()
end
function s.directtg(e,tp,eg,ep,ev,re,r,rp,chk)
        if chk==0 then return Duel.IsExistingMatchingCard(s.directfilter,tp,LOCATION_MZONE,0,1,nil) end
        Duel.SetOperationInfo(0,CATEGORY_DIRECT_ATTACK,nil,0,tp,1)
end
function s.directop(e,tp,eg,ep,ev,re,r,rp)
        local g=Duel.GetMatchingGroup(s.directfilter,tp,LOCATION_MZONE,0,nil)
        if g:GetCount()>0 then
                local tc=g:Select(tp,1,1,nil):GetFirst()
                if tc then
                        --direct attack
                        local e1=Effect.CreateEffect(e:GetHandler())
                        e1:SetType(EFFECT_TYPE_SINGLE)
                        e1:SetCode(EFFECT_DIRECT_ATTACK)
                        e1:SetProperty(EFFECT_FLAG_CANNOT_DISABLE)
                        e1:SetReset(RESET_EVENT+RESETS_STANDARD_DISABLE+RESET_PHASE+PHASE_END)
                        tc:RegisterEffect(e1)
                end
        end
end
```