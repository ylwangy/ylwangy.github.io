import json
import openai

INPUT = 'BACE_random_500.json'
INPUT = 'BACE_prediction_gpt4_random.json'
OUTPUT = 'BACE_prediction_gpt4_random.json'
test_file = open(INPUT, 'r', encoding='utf-8')
test_data = json.load(test_file)
for idx, task_json in enumerate(test_data):
    if 'response' in task_json.keys():
        continue
    else:
        print(idx, len(test_data))

        prompt = "You are an expert chemist, your task is to predict the property of molecule using your experienced chemical property prediction knowledge. Given the SMILES string of a molecule, predict the molecular properties of a given chemical compound based on its structure, by analyzing wether it can inhibit(Yes) the Beta-site Amyloid Precursor Protein Cleaving Enzyme 1 (BACE1) or cannot inhibit(No) BACE1. Consider factors such as molecular weight, atom count, bond types, and functional groups in order to assess the compound's drug-likeness and its potential to serve as an effective therapeutic agent for Alzheimer's disease.\n"

        prompt += f"SMILES: {task_json['mol']}\nBACE-1 Inhibit: "
        prompt += "\n\nPlease answer with only Yes or No in the final. Let's think step by step.\n"
        print(prompt)
        try:
            responses = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0
            )
            print(responses['choices'][0]['message']['content'])
            task_json['response'] = responses['choices'][0]['message']['content']
        except:
            pass
        print('---'*10)
with open(OUTPUT, 'w') as f:
    json.dump(test_data, f, indent=4)