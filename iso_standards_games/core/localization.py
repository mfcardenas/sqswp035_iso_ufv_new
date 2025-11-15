"""Localization utilities."""

import os
import json
from typing import Dict, Optional

import i18n

from iso_standards_games.core.config import settings


def setup_localization():
    """Set up i18n configuration."""
    # Configure i18n
    locales_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "locales"
    )
    
    i18n.load_path.append(locales_path)
    i18n.set("fallback", "en")
    i18n.set("locale", settings.DEFAULT_LOCALE)
    i18n.set("enable_memoization", True)


def translate(key: str, locale: Optional[str] = None, **kwargs) -> str:
    """Translate a key to the specified locale.
    
    Args:
        key: Translation key
        locale: Optional locale override
        **kwargs: Format parameters
        
    Returns:
        Translated string
    """
    current_locale = locale or i18n.get("locale")
    return i18n.t(key, locale=current_locale, **kwargs)


def get_translations(locale: str) -> Dict:
    """Get all translations for a locale.
    
    Args:
        locale: Locale code
        
    Returns:
        Dictionary of translations
    """
    locales_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "locales",
        locale,
        "translation.json"
    )
    
    try:
        with open(locales_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to default locale
        if locale != settings.DEFAULT_LOCALE:
            return get_translations(settings.DEFAULT_LOCALE)
        return {}