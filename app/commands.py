from flask import Blueprint
import click
from app.database import db, set_job_catalog, set_skill_catalog

# 1. Init blueprint
db_cli_bp = Blueprint('db_cli', __name__)

@db_cli_bp.cli.command("init")
def init_db():
    db.create_all()
    set_job_catalog()
    set_skill_catalog()
    click.echo("[+] Database and catalogs initialized successfully.")
