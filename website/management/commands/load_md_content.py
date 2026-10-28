import os

import frontmatter
from django.conf import settings
from django.core.management.base import BaseCommand

from wafer.pages.models import Page

MD_BASE_DIR = settings.BASE_DIR / "pages_md"


def create_or_update_page_from_file(md_path, slug=None, parent=None):
    md = frontmatter.load(md_path)
    slug = slug or md_path.stem
    page, _created = Page.objects.get_or_create(slug=slug, parent=parent)
    for key in md.keys():
        if key == "slug":
            continue
        setattr(page, key, md[key])
    page.parent = parent
    page.content = md.content
    page.save()
    return page


def load_md_pages(parent, path):
    if path.stem.startswith("__") or path.stem == "_page" or path.name.startswith("."):
        return
    if path.is_dir():
        details_path = path / "_page.md"
        next_parent = parent
        if details_path.exists():
            next_parent = create_or_update_page_from_file(
                slug=path.stem,
                md_path=details_path,
                parent=parent,
            )
        for child in sorted(os.listdir(path)):
            load_md_pages(parent=next_parent, path=path / child)
        return
    if path.suffix.lower() != ".md":
        return
    create_or_update_page_from_file(md_path=path, parent=parent)


class Command(BaseCommand):
    help = "Load markdown files from pages_md into wafer pages."

    def handle(self, *args, **options):
        load_md_pages(parent=None, path=MD_BASE_DIR)
        self.stdout.write(self.style.SUCCESS("Loaded pages from pages_md."))
