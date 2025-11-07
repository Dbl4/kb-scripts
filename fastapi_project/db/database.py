async def get_db():
    print("Creating database connection")
    bd = []
    try:
        yield bd
    finally:
        print("Clocing connection")
