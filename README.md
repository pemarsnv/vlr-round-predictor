_warning: this project and this README are both WIPs_

# Valorant Round Predictor

`vlr-round-predictor` is a machine learning project, aiming to predict Valorant Champions Tour results, aka the official Valorant e-sports circuit. 
This model's training will be divided in two phases: **learning how the game works**, and **predicting based on recent results**.

## phase 1 : teach the model how the game works 🧮

The point of this first phase is to train the model into understanding what to expect from a typical Valorant round. Here, there is no point taking into account who is playing against who and their past performance. The model simply needs to be able to identify patterns such as: 
- The **economy**
- The **different maps** and their advantageous side
- The concept of **momentum**

For now, it doesn't matter if FUT is good at landing economies, or if FNATIC somehow have a better attack side on Ascent. What does is how the economy usually impacts a round outcome, and how the maps advantages generally play out.
To do so, we first need to...

### p1 step 1 : data retrieval 📑 [DONE]

The model is going to be trained on all past VCT matches. In order to do so, I am going to use [vlrggapi](https://github.com/axsddlr/vlrggapi).

### p1 step 2 : data formatting 🧹

### p1 step 3 : data vizualisation 📊
step 1-2: data formatting (current step)
step 1-3: data vizualisation interface
step 1-4: training

step 2 : train on specific data
coming soon
