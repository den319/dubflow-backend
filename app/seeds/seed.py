from app.core.database import SessionLocal

from app.seeds.users_seed import seed_users
from app.seeds.projects_seed import seed_projects
from app.seeds.subtitle_files_seed import seed_subtitle_files
from app.seeds.subtitle_entries_seed import seed_subtitle_entries
from app.seeds.home_seed import seed_home_data
from app.seeds.explore_seed import seed_explore_data


def run_seed():
    db = SessionLocal()

    try:
        print("Seeding users...")
        users = seed_users(db)

        print("Seeding projects...")
        projects = seed_projects(db, users)

        print("Seeding subtitle files...")
        subtitle_files = seed_subtitle_files(db, projects)

        print("Seeding subtitle entries...")
        seed_subtitle_entries(db, subtitle_files)

        print("Seeding home data...")
        seed_home_data(db)

        print("Seeding explore data...")
        seed_explore_data(db)

        print("Database seeded successfully.")

    except Exception as e:
        print(f"Seed failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()