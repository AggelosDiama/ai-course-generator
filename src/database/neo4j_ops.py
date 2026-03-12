import os
from langchain_neo4j import Neo4jGraph
import json

class Neo4jManager:
    def __init__(self):
        self.graph = Neo4jGraph(
            url=os.getenv("NEO4J_URI", "neo4j://localhost:7687"),
            username=os.getenv("NEO4J_USERNAME", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", "P@ssword1234")
        )
    
    def get_all_course_metadata(self):
        query = """
        MATCH (c:Course)
        RETURN c.title AS title, 
            c.generated_title AS gen_title, 
            c.expertise AS expertise, 
            c.duration AS duration, 
            c.interests AS interests
        """
        return self.graph.query(query)

    def save_course_structure(self, data, original_topic, expertise, duration, interests):
        self.graph.query("""
            MERGE (c:Course {title: $original_topic})
            SET c.expertise = $expertise, 
                c.duration = $duration, 
                c.interests = $interests,
                c.generated_title = $gen_title
            WITH c 
            OPTIONAL MATCH (c)-[:HAS_MODULE]->(m)-[:HAS_LESSON]->(l)
            DETACH DELETE m, l
            WITH c 
            UNWIND $modules AS mod
            CREATE (m:Module {title: mod.title})
            CREATE (c)-[:HAS_MODULE]->(m)
            WITH m, mod UNWIND mod.lessons AS less
            CREATE (l:Lesson {
                title: less.title, 
                duration_min: less.estimated_duration_minutes,
                module_parent: mod.title
            })
            CREATE (m)-[:HAS_LESSON]->(l)
        """, params={
            "original_topic": original_topic,
            "gen_title": data["course_title"],
            "expertise": expertise,
            "duration": duration,
            "interests": interests,
            "modules": data["modules"]
        })

    def save_final_json(self, original_topic, json_data):
        # Store the full JSON content for the UI to parse
        self.graph.query("""
            MATCH (c:Course)
            WHERE c.title = $old_t OR c.generated_title = $old_t
            SET c.final_content = $json_str,
                c.generated_title = $new_t
        """, params={
            "old_t": original_topic,
            "json_str": json.dumps(json_data),
            "new_t": json_data['course_title']
        })

    def get_course_by_title(self, title):
        # This is the "Smart Search" that prevents the view-error
        result = self.graph.query("""
            MATCH (c:Course)
            WHERE c.title = $t OR c.generated_title = $t
            RETURN c.title as title, 
                   c.generated_title as gen_title,
                   c.expertise as diff, 
                   c.duration as h, 
                   c.final_content as content
        """, params={"t": title})
        return result[0] if result else None

    def get_history(self):
        # Updated to return the pretty generated_title for the sidebar
        return self.graph.query("""
            MATCH (c:Course) 
            RETURN coalesce(c.generated_title, c.title) as title, 
                   c.duration as h, 
                   c.expertise as diff, 
                   c.interests as i, 
                   c.final_content as content
        """)
    def get_course_structure(self, title):
        # We search by EITHER original title OR generated title 
        # to ensure the Roadmap always populates correctly
        return self.graph.query("""
            MATCH (c:Course)
            WHERE c.title = $t OR c.generated_title = $t
            MATCH (c)-[:HAS_MODULE]->(m:Module)
            OPTIONAL MATCH (m)-[:HAS_LESSON]->(l:Lesson)
            RETURN m.title as module, collect(l.title) as lessons
        """, params={"t": title})
    
    def reset_course_progress(self, title):
        # This removes the 'score' and 'passed' properties from Quiz/Lesson nodes 
        # linked to this specific course.
        query = """
        MATCH (c:Course)-[:HAS_MODULE]->(m)-[:HAS_LESSON]->(l)
        WHERE c.title = $t OR c.generated_title = $t
        SET m.quiz_score = 0,
            m.quiz_passed = false,
            l.completed = false
        """
        self.graph.query(query, params={"t": title})


    def delete_course(self, title):
        # This query finds the course by either title, 
        # then finds all connected modules and lessons, 
        # then deletes everything in one go.
        query = """
        MATCH (c:Course)
        WHERE c.title = $t OR c.generated_title = $t
        OPTIONAL MATCH (c)-[:HAS_MODULE]->(m)
        OPTIONAL MATCH (m)-[:HAS_LESSON]->(l)
        DETACH DELETE c, m, l
        """
        self.graph.query(query, params={"t": title})

    def clear_all(self):
        self.graph.query("MATCH (n) DETACH DELETE n")


                