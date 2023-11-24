import json
import openai

INPUT = 'BBBP_random_500_s2l.json'
INPUT = 'BBBP_prediction_gpt4_random_s2l.json'
OUTPUT = 'BBBP_prediction_gpt4_random_s2l.json'
test_file = open(INPUT, 'r', encoding='utf-8')
test_data = json.load(test_file)
for idx, task_json in enumerate(test_data):
    if 'response' in task_json.keys():
        continue
    else:
        print(idx, len(test_data))
        prompt = "You are an expert chemist, your task is to predict the property of molecule using your experienced chemical property prediction knowledge. Given the SMILES string of a molecule, the task focuses on predicting molecular properties, specifically penetration/non-penetration to the brain-blood barrier, based on the SMILES string representation of each molecule. The task is to predict the binary label for a given molecule whether it has penetrative property (Yes) or not (No).\n"
        # prompt += f"SMILES: {task_json['smiles']}\nPenetration: "
        prompt += f"SMILES: {task_json['smiles']}\n{task_json['s2l-2'].strip()}\nPenetration: "
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