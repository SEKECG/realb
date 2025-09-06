```python
# risk.py

from models import RiskLevel, ChromePermission, RiskReport

permissions_risk_map = {
    "activeTab": RiskLevel.LOW,
    "alarms": RiskLevel.NONE,
    "bookmarks": RiskLevel.MEDIUM,
    "clipboardRead": RiskLevel.HIGH,
    "cookies": RiskLevel.CRITICAL,
    # Add other permissions as needed
}

risk_score_map = {
    RiskLevel.NONE: 0,
    RiskLevel.LOW: 20,
    RiskLevel.MEDIUM: 50,
    RiskLevel.HIGH: 75,
    RiskLevel.CRITICAL: 100,
}

def get_risk_level(permission):
    return permissions_risk_map.get(permission, RiskLevel.NONE)

def get_risk_score(risk_level):
    return risk_score_map.get(risk_level, 0)

def get_risk_report(extension):
    permissions = extension.permissions
    risk_levels = [get_risk_level(permission) for permission in permissions]
    risk_scores = [get_risk_score(risk_level) for risk_level in risk_levels]
    overall_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0

    return RiskReport(
        name=extension.name,
        version=extension.version,
        author=extension.author,
        permissions=permissions,
        risk_levels=risk_levels,
        risk_scores=risk_scores,
        overall_risk_score=overall_risk_score,
        javascript_files=extension.javascript_files,
        urls=extension.urls,
    )
```