from flask import Flask,request,jsonify
import cohere
import os 
from dotenv import load_dotenv

app =  Flask(__name__)
cohere_api_key = os.environ.get("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

load_dotenv()

@app.route("/generate-idea",methods=["POST"])
def generate_idea():
    data = request.get_json()
    startup_industry = data.get("startup_industry")
    creativity =data.get("creativity")
    idea_prompt = f"""
        Industry: {startup_industry}
        Startup Idea: 
    """
    response = co.generate(model="command-nightly",prompt=idea_prompt,temperature=creativity, num_generations=1,k=0,stop_sequences=["--"],max_tokens=100)
    startup_idea = response.generations[0].text
    startup_idea = startup_idea.replace("\n\n--", "").replace("\n--", "").strip()
    return jsonify({"generated idea":startup_idea})

@app.route("/generate-name",methods=["POST"])
def generate_name():
    data = request.get_json()
    startup_idea = data.get("startup_idea")
    creativity = data.get("creativity")

    name_prompt = f"""
        Startup Idea: {startup_idea}
        Startup Name:"""
    response = co.generate(model="command-nightly",prompt=name_prompt,max_tokens=100,temperature=creativity,k=0,stop_sequences=["---"])
    startup_name = response.generations[0].text
    startup_name = startup_name.replace("\n\n--", "")
    return jsonify({"generated name":startup_name})


if __name__ == "__main__":
    app.run(debug=True) 