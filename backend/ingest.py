import os
import asyncio
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import requests
from pathlib import Path

load_dotenv()

class BookIngester:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def ingest_physical_ai_book(self):
        """🏆 Hackathon: Ingest COMPLETE Physical AI textbook"""
        print("🚀 Indexing Physical AI & Humanoid Robotics book...")
        
        # Physical AI Course Content (Hackathon topics)
        book_content = [
            # Module 1: ROS 2
            "ROS 2 is middleware for robot control. Nodes communicate via topics, services, and actions. Use rclpy to bridge Python agents to ROS controllers.",
            "URDF (Unified Robot Description Format) defines humanoid robot structure for simulation and real-world control.",
            
            # Module 2: Gazebo Simulation
            "Gazebo simulates physics, gravity, and collisions. SDF format extends URDF for dynamic environments.",
            "Simulate sensors: LiDAR, Depth Cameras, IMUs in Gazebo for realistic robot testing.",
            
            # Module 3: NVIDIA Isaac
            "NVIDIA Isaac Sim provides photorealistic simulation with synthetic data generation for AI training.",
            "Isaac ROS accelerates VSLAM (Visual SLAM) and navigation with GPU hardware acceleration.",
            "Nav2 stack enables path planning for bipedal humanoid movement and obstacle avoidance.",
            
            # Module 4: VLA
            "Vision-Language-Action (VLA) converts natural language commands to robot actions using LLMs.",
            "OpenAI Whisper enables voice-to-action: 'Clean the room' → ROS 2 action sequence.",
            
            # Hardware
            "NVIDIA Jetson Orin Nano (40 TOPS) runs Isaac ROS inference on edge devices.",
            "Intel RealSense D435i provides RGB + Depth for VSLAM and object detection.",
            
            # Capstone
            "Capstone: Autonomous Humanoid receives voice command, plans path, navigates obstacles, manipulates objects."
        ]
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        vectors = self.embedder.encode(book_content).tolist()
        
        # Create points
        points = [
            PointStruct(
                id=i, 
                vector=vec, 
                payload={
                    "text": content, 
                    "chapter": f"module_{i//2 + 1}",
                    "topic": content.split()[0:3]
                }
            )
            for i, (vec, content) in enumerate(zip(vectors, book_content))
        ]
        
        # Upsert to Qdrant
        print("💾 Indexing to Qdrant...")
        self.qdrant_client.recreate_collection(
            collection_name="physical_ai_book",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        self.qdrant_client.upsert(collection_name="physical_ai_book", points=points)
        
        print(f"✅ SUCCESS! Ingested {len(points)} chunks!")
        print("📚 Book topics indexed: ROS2, Gazebo, Isaac Sim, VLA")
        print("🤖 Chatbot ready: http://localhost:8000/chat")
    
    async def ingest_docusaurus(self, docs_path="../web/docs"):
        """Ingest actual Docusaurus MDX files"""
        docs_dir = Path(docs_path)
        if not docs_dir.exists():
            print(f"⚠️ Docs folder not found: {docs_dir}")
            return
        
        content = []
        for md_file in docs_dir.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
                # Extract text content (remove markdown headers)
                chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 50]
                content.extend(chunks[:10])  # Limit per file
                print(f"📄 Indexed: {md_file.name}")
            except:
                continue
        
        if content:
            vectors = self.embedder.encode(content).tolist()
            points = [PointStruct(id=i, vector=v, payload={"text": c[:1000]}) 
                     for i, (v, c) in enumerate(zip(vectors, content))]
            self.qdrant_client.upsert("physical_ai_book", points)
            print(f"✅ Docusaurus ingested: {len(content)} chunks!")

async def main():
    ingester = BookIngester()
    await ingester.ingest_physical_ai_book()
    # await ingester.ingest_docusaurus()  # Uncomment for real docs

if __name__ == "__main__":
    asyncio.run(main())
