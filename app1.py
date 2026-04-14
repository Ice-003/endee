import os
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI   # NEW

# -------------------------------
# 1. Load Code Files
# -------------------------------
def load_code_files(folder_path):
    code_data = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    code_data.append((path, f.read()))
    return code_data


# -------------------------------
# 2. Chunk Code
# -------------------------------
def chunk_code(code, chunk_size=300):
    return [code[i:i+chunk_size] for i in range(0, len(code), chunk_size)]


# -------------------------------
# 3. Simple Vector DB (Endee-like)
# -------------------------------
class SimpleVectorDB:
    def __init__(self):
        self.data = []

    def add(self, vector, metadata):
        self.data.append({"vector": vector, "metadata": metadata})

    def search(self, query_vec, top_k=3):
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        scored = []
        for item in self.data:
            score = cosine_similarity(query_vec, item["vector"])
            scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored[:top_k]]


# -------------------------------
# 4. Ingestion
# -------------------------------
def ingest_code(folder="sample_code"):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    db = SimpleVectorDB()

    files = load_code_files(folder)

    for path, code in files:
        chunks = chunk_code(code)

        for chunk in chunks:
            embedding = model.encode(chunk)

            db.add(
                vector=embedding,
                metadata={
                    "file": path,
                    "code": chunk
                }
            )

    print("✅ Code ingestion completed.")
    return db, model


# -------------------------------
# 5. AI Explanation Function (NEW)
# -------------------------------
def generate_answer(context, query):
    try:
        #client = OpenAI(api_key="YOUR_API_KEY")  # 🔴 REPLACE THIS
        client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxx")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Explain the given code clearly in simple terms."},
                {"role": "user", "content": f"{context}\n\nQuestion: {query}"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error generating AI response: {e}"


# -------------------------------
# 6. Main RAG Flow
# -------------------------------
def main():
    # Ensure sample folder exists
    if not os.path.exists("sample_code"):
        os.makedirs("sample_code")

        with open("sample_code/app.py", "w") as f:
            f.write("""
def login(username, password):
    if username == "admin" and password == "1234":
        return "Login successful"
    return "Invalid credentials"

def logout():
    return "User logged out"
""")

    db, model = ingest_code()

    print("\n💡 Ask questions about your code (type 'exit' to quit)\n")

    while True:
        query = input("🔎 Your Question: ")

        if query.lower() == "exit":
            break

        query_vec = model.encode(query)
        results = db.search(query_vec)

        print("\n📂 Retrieved Code Context:\n")

        context = ""
        for r in results:
            print(f"File: {r['metadata']['file']}")
            print(r["metadata"]["code"])
            print("-" * 50)

            context += r["metadata"]["code"] + "\n"

        # -------------------------------
        # AI Generated Answer
        # -------------------------------
        print("\n🧠 AI Explanation:\n")
        answer = generate_answer(context, query)
        print(answer)


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    main()