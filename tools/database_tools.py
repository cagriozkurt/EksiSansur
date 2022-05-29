import psycopg
from eksisozluk.EksiSozluk import EksiApi
from tqdm import tqdm

client = EksiApi()
DATABASE_URL = ""


def update_database():
    with psycopg.connect(DATABASE_URL, sslmode="require") as conn:
        with conn.cursor() as cur:
            for entry in client.get_user_entries(
                "ekşisözlük", page=1
            ).user_entries.entries:
                if "sulh ceza" in entry.entry.content:
                    topic_id = entry.topic_id.id
                    topic_title = entry.topic_id.topic_title.title
                    created = entry.entry.created
                    cur.execute(
                        f"""
                        INSERT INTO topics(id, title, created) 
                        SELECT 
                        $${topic_id}$$, 
                        $${topic_title}$$, 
                        $${created}$$ 
                        WHERE 
                        NOT EXISTS (
                            SELECT 
                            * 
                            FROM 
                            topics 
                            WHERE 
                            id = $${topic_id}$$
                            AND title = $${topic_title}$$
                            AND created = $${created}$$
                        );
                        """
                    )
            conn.commit()
