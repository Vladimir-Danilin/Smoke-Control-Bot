import asyncpg

TOKEN = "TOKEN"
admin_ids = [123456789]

async def connect():
    return await asyncpg.connect(host="localhost",
                                port='port',
                                user="postgres",
                                password="password",
                                database="SmokeControlBase")
