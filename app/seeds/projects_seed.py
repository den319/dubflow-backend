from app.models.project import Project


def seed_projects(db, users):
    projects = [
        Project(
            user_id=users[0].id,
            name="Money Heist Hindi",
            source_language="en",
            target_language="hi",
            status="processing",
        ),
        Project(
            user_id=users[1].id,
            name="Narcos Spanish",
            source_language="en",
            target_language="es",
            status="completed",
        ),
    ]

    db.add_all(projects)
    db.commit()

    return projects