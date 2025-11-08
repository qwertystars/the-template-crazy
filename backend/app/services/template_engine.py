import yaml
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.template import Template, TemplateCategory


class TemplateEngine:
    def __init__(self, db: Session, templates_dir: str = "templates"):
        self.db = db
        self.templates_dir = Path(templates_dir)

    def load_template_from_file(self, template_path: str) -> Dict[str, Any]:
        """Load template configuration from YAML or JSON file"""
        template_file = Path(template_path)
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        with open(template_file, 'r') as f:
            if template_file.suffix.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif template_file.suffix.lower() == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported template file format: {template_file.suffix}")

    def validate_template_config(self, config: Dict[str, Any]) -> bool:
        """Validate template configuration structure"""
        required_fields = ['name', 'slug', 'category', 'config']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")

        # Validate category
        if config['category'] not in [c.value for c in TemplateCategory]:
            raise ValueError(f"Invalid category: {config['category']}")

        return True

    def register_template(self, template_config: Dict[str, Any]) -> Template:
        """Register a template from configuration"""
        self.validate_template_config(template_config)

        # Check if template already exists
        existing = self.db.query(Template).filter(
            Template.slug == template_config['slug']
        ).first()
        if existing:
            raise ValueError(f"Template with slug '{template_config['slug']}' already exists")

        # Create template
        db_template = Template(
            name=template_config['name'],
            slug=template_config['slug'],
            description=template_config.get('description'),
            category=TemplateCategory(template_config['category']),
            version=template_config.get('version', '1.0.0'),
            author=template_config.get('author'),
            preview_image=template_config.get('preview_image'),
            tags=template_config.get('tags', []),
            is_premium=template_config.get('is_premium', False),
            config=template_config['config'],
            layout_config=template_config.get('layout_config'),
            theme_config=template_config.get('theme_config'),
            content_schema=template_config.get('content_schema'),
            plugin_hooks=template_config.get('plugin_hooks', {})
        )

        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        return db_template

    def get_templates_by_category(self, category: TemplateCategory) -> List[Template]:
        """Get all active templates in a category"""
        return self.db.query(Template).filter(
            Template.category == category,
            Template.is_active == True
        ).all()

    def render_template_config(self, template: Template, site_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Render template with site-specific configuration"""
        rendered_config = template.config.copy()

        if site_config:
            # Merge site configuration with template defaults
            for key, value in site_config.items():
                if key in rendered_config:
                    if isinstance(rendered_config[key], dict) and isinstance(value, dict):
                        rendered_config[key].update(value)
                    else:
                        rendered_config[key] = value

        return rendered_config

    def validate_content_against_schema(self, content: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate page content against template's content schema"""
        # This is a simplified validation - in production, you'd use a proper JSON schema validator
        if not schema:
            return True

        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in content:
                raise ValueError(f"Missing required content field: {field}")

        return True